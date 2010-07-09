
from civicboom.model.meta import Base
from civicboom.model.member import Member
import civicboom.lib.warehouse as wh

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean
from geoalchemy import GeometryColumn, Point, GeometryDDL
from sqlalchemy.orm import relationship, backref

import magic
import Image
import tempfile
import os
import logging
import subprocess

log = logging.getLogger(__name__)


# many-to-many mappings need to be at the top, so that other classes can
# say "I am joined to other table X using mapping Y as defined above"

class ContentTagMapping(Base):
    __tablename__ = "map_content_to_tag"
    content_id    = Column(Integer(),    ForeignKey('content.id'), nullable=False, primary_key=True)
    tag_id        = Column(Integer(),    ForeignKey('tag.id'), nullable=False, primary_key=True)

class Boom(Base):
    __tablename__ = "map_booms"
    content_id    = Column(Integer(),    ForeignKey('content_user_visible.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id'), nullable=False, primary_key=True)

class Rating(Base):
    __tablename__ = "map_ratings"
    content_id    = Column(Integer(),    ForeignKey('content_user_visible.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id'), nullable=False, primary_key=True)
    rating        = Column(Integer(),    nullable=False, default=0)


class Content(Base):
    """
    Abstract class

    "private" means different things depending on which child table extends it:

    ContentComment
      only visible to the user and the user/group who wrote the content being replied to

    ContentDraft
      only visible to the user writing it (otherwise group visible)

    ContentArticle
      only visible to creator and requester

    ContentAssignment
      only visible to creator and creator-specificed users/groups

    (FIXME: is this correct?)
    """
    __tablename__   = "content"
    # FIXME: is this list complete?
    __type__        = Column(Enum("comment", "draft", "article", "assignment", name="content_type"), nullable=False)
    __mapper_args__ = {'polymorphic_on': __type__}
    # FIXME: "etc"?
    _content_status = Enum("show", "pending", "locked", name="content_status")
    id              = Column(Integer(),        primary_key=True)
    title           = Column(Unicode(250),     nullable=False  )
    content         = Column(UnicodeText(),    nullable=False, doc="The body of text")
    creator_id      = Column(Integer(),        ForeignKey('member.id'), nullable=False)
    parent_id       = Column(Integer(),        ForeignKey('content.id'), nullable=True)
    # FIXME: area rather than point?
    location        = GeometryColumn(Point(2), nullable=True   )
    creation_date   = Column(DateTime(),       nullable=False, default="now()")
    update_date     = Column(DateTime(),       nullable=False, default="now()")
    status          = Column(_content_status,  nullable=False, default="show")
    private         = Column(Boolean(),        nullable=False, default=False, doc="see class doc")
    # FIXME: default license? People just making comments probably don't want to pick one every time
    license_id      = Column(Integer(),        ForeignKey('license.id'), nullable=False)
    # FIXME: remote_side is confusing, and do we want to cascade to delete replies?
    responses       = relationship("Content",            backref=backref('parent', remote_side=id), cascade="all")
    attachments     = relationship("Media",              backref=backref('attached_to'), cascade="all,delete-orphan")
    edits           = relationship("ContentEditHistory", backref=backref('content', order_by=id), cascade="all,delete-orphan")
    tags            = relationship("Tag",                secondary=ContentTagMapping.__table__)

    def __unicode__(self):
        return self.title + u" (" + self.__type__ + u")"


class CommentContent(Content):
    __tablename__   = "content_comment"
    __mapper_args__ = {'polymorphic_identity': 'comment'}
    id              = Column(Integer(), ForeignKey('content.id'), primary_key=True)


class DraftContent(Content):
    __tablename__   = "content_draft"
    __mapper_args__ = {'polymorphic_identity': 'draft'}
    id              = Column(Integer(), ForeignKey('content.id'), primary_key=True)


class UserVisibleContent(Content):
    "Abstract class"
    __tablename__ = "content_user_visible"
    id            = Column(Integer(), ForeignKey('content.id'), primary_key=True)
    views         = Column(Integer(), nullable=False, default=0)
    boom_count    = Column(Integer(), nullable=False, default=0) # FIXME: derived


class ArticleContent(UserVisibleContent):
    __tablename__   = "content_article"
    __mapper_args__ = {'polymorphic_identity': 'article'}
    id              = Column(Integer(), ForeignKey('content_user_visible.id'), primary_key=True)
    rating          = Column(Integer(), nullable=False, default=0) # FIXME: derived
    ratings         = relationship("Rating", backref=backref('content'), cascade="all,delete-orphan")
    # FIXME: type (news, feature, article, etc?)


class AssignmentContent(UserVisibleContent):
    __tablename__   = "content_assignment"
    __mapper_args__ = {'polymorphic_identity': 'assignment'}
    id              = Column(Integer(),        ForeignKey('content_user_visible.id'), primary_key=True)
    event_date      = Column(DateTime(),       nullable=True)
    due_date        = Column(DateTime(),       nullable=True)
    assigned_to     = relationship("MemberAssignment", backref=backref("content"), cascade="all,delete-orphan")
    #private D (if any AssignmentClosed records exist) # FIXME: "content" already has this?
    #private_response (bool) (already exisits? see content)

class MemberAssignment(Base):
    __tablename__ = "member_assignment"
    content_id    = Column(Integer(),    ForeignKey('content_assignment.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id'), nullable=False, primary_key=True)
    withdrawn     = Column(Boolean(),    nullable=False, default=False)



# FIXME: is this needed?
#class AssignmentClosed(Base):
#    contentAssignmentId
#    memberId


class License(Base):
    __tablename__ = "license"
    id            = Column(Integer(),     primary_key=True)
    code          = Column(Unicode(32),   nullable=False, unique=True)
    name          = Column(Unicode(250),  nullable=False, unique=True)
    description   = Column(UnicodeText(), nullable=False)
    url           = Column(UnicodeText(), nullable=False)
    #articles      = relationship("Content", backref=backref('license'))

    def __init__(self, code=None, name=None, description=None, url=None):
        self.code = code
        self.name = name
        self.description = description
        self.url = url

    def __unicode__(self):
        return self.code


# FIXME: do we need types *and* parents?
# "type" was added so that "artist_name:red_box" and "photo_of:red_box" could
# be separated, but we could have category->artists->red_box and
# article_contents->photo_of->red_box instead
# Shish - assuming we don't need types
class Tag(Base):
    """
    A topic for an article, eg "cakes", "printers"

    Tags can have parents, eg:
    Food > Cakes
    Science & Technology > Hardware > Printers

    Tags should normally be capitalised and plural
    """
    __tablename__ = "tag"
    id            = Column(Integer(),    primary_key=True)
    name          = Column(Unicode(250), nullable=False) # FIXME: should be unique within its category
    #type          = Column(Unicode(250), nullable=False, default=u"Topic")
    parent_id     = Column(Integer(),    ForeignKey('tag.id'), nullable=True)
    #children      = relationship("Tag", backref=backref('parent', remote_side=id))

    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent

    def __unicode__(self):
        return self.name


# FIXME: unseeded
class ContentEditHistory(Base):
    __tablename__ = "content_edit_history"
    id            = Column(Integer(),     primary_key=True)
    content_id    = Column(Integer(),     ForeignKey('content.id'), nullable=False)
    member_id     = Column(Integer(),     ForeignKey('member.id'), nullable=False)
    timestamp     = Column(DateTime(),    nullable=False, default="now()")
    source        = Column(Unicode(250),  nullable=False, default="other", doc="civicboom, mobile, another_webpage, other service")
    text_change   = Column(UnicodeText(), nullable=False)


class Media(Base):
    __tablename__ = "media"
    _media_types  = Enum("application", "audio", "example", "image", "message", "model", "multipart", "text", "video", name="media_types")
    id            = Column(Integer(),        primary_key=True)
    content_id    = Column(Integer(),        ForeignKey('content.id'), nullable=False)
    name          = Column(UnicodeText(250), nullable=False)
    type          = Column(_media_types,     nullable=False, doc="MIME type, eg 'text', 'video'")
    subtype       = Column(String(32),       nullable=False, doc="MIME subtype, eg 'jpeg', '3gpp'")
    hash          = Column(String(40),       nullable=False, index=True)
    caption       = Column(UnicodeText(),    nullable=False)
    credit        = Column(UnicodeText(),    nullable=False)

    def _ffmpeg(self, args):
        """
        Convenience function to run ffmpeg and log the output
        """
        ffmpeg = "/usr/bin/ffmpeg" # FIXME: config variable?
        cmd = [ffmpeg, ] + args
        log.info(" ".join(cmd))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = proc.communicate()
        log.debug("stdout: "+output[0])
        log.debug("stderr: "+output[1])
        log.debug("return: "+str(proc.returncode))

    def load_from_file(self, tmp_file=None, original_name=None, caption=None, credit=None):
        "Create a Media object from a blob of data + upload form details"
        # Set up metadata
        self.name = original_name
        self.type, self.subtype = magic.from_file(tmp_file, mime=True).split("/")
        self.hash = wh.hash_file(tmp_file)
        self.caption = caption if caption else u""
        self.credit = credit if credit else u""

        wh.copy_to_local_warehouse(tmp_file, "originals", self.hash)

        # FIXME: turn tmp_file into something suitable for web viewing
        if self.type == "image":
            processed = tempfile.NamedTemporaryFile(suffix=".jpg")
            size = 480, 360
            im = Image.open(tmp_file)
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(processed.name, "JPEG")
            wh.copy_to_local_warehouse(processed.name, "media", self.hash)
            processed.close()
        elif self.type == "audio":
            processed = tempfile.NamedTemporaryFile(suffix=".ogg")
            self._ffmpeg(["-y", "-i", tmp_file, "-ab", "192k", processed.name])
            wh.copy_to_local_warehouse(processed.name, "media", self.hash)
            processed.close()
        elif self.type == "video":
            processed = tempfile.NamedTemporaryFile(suffix=".flv")
            size = 480, 360
            self._ffmpeg([
                "-y", "-i", tmp_file,
                "-ab", "56k", "-ar", "22050",
                "-qmin", "2", "-qmax", "16",
                "-b", "320k", "-r", "15",
                "-s", "%dx%d" % (size[0], size[1]),
                processed.name
            ])
            wh.copy_to_local_warehouse(processed.name, "media", self.hash)
            processed.close()

        # create a thumbnail
        if self.type == "image":
            processed = tempfile.NamedTemporaryFile(suffix=".jpg")
            size = 128, 128 # FIXME: config value?
            im = Image.open(tmp_file)
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(processed.name, "JPEG")
            wh.copy_to_local_warehouse(processed.name, "thumbnails", self.hash)
            processed.close()
        elif self.type == "audio":
            # audio has no thumb; what is displayed to the user is
            # a player plugin
            pass
        elif self.type == "video":
            processed = tempfile.NamedTemporaryFile(suffix=".jpg")
            size = 128, 128 # FIXME: config value?
            self._ffmpeg([
                "-y", "-i", tmp_file,
                "-an", "-vframes", "1", "-r", "1",
                "-s", "%dx%d" % (size[0], size[1]),
                "-f", "image2", processed.name
            ])
            wh.copy_to_local_warehouse(processed.name, "thumbnails", self.hash)
            processed.close()

        #log.debug("Created Media from file %s -> %s" % (self.name, self.hash))

        return self

    def sync(self):
        wh.copy_to_remote_warehouse("originals", self.hash)
        wh.copy_to_remote_warehouse("media", self.hash)
        if self.type != "audio":
            wh.copy_to_remote_warehouse("thumbnails", self.hash)
        return self

    def __unicode__(self):
        return self.name

    @property
    def mime_type(self):
        return self.type + "/" + self.subtype

    @property
    def original_url(self):
        "The URL of the original as-uploaded file"
        return "http://static.civicboom.com/originals/%s/%s" % (self.hash, self.name)

    @property
    def media_url(self):
        "The URL of the processed media, eg .flv file for video"
        exts = {
            "audio": "ogg",
            "image": "jpeg",
            "video": "flv"
        }
        return "http://static.civicboom.com/media/%s/data.%s" % (self.hash, exts[self.type])

    @property
    def thumbnail_url(self):
        "The URL of a JPEG-format thumbnail of this media"
        return "http://static.civicboom.com/thumbnails/%s/thumb.jpg" % (self.hash, )


GeometryDDL(Content.__table__)
