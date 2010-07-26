
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean

from civicboom.model.meta import Base
import civicboom.lib.warehouse as wh

import magic
import Image
import tempfile
import os
import logging
import subprocess

log = logging.getLogger(__name__)


class Media(Base):
    __tablename__ = "media"
    _media_types  = Enum("application", "audio", "example", "image", "message", "model", "multipart", "text", "video", name="media_types")
    id            = Column(Integer(),        primary_key=True)
    content_id    = Column(Integer(),        ForeignKey('content.id'), nullable=False)
    name          = Column(Unicode(250),     nullable=False)
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

        wh.copy_to_local_warehouse(tmp_file, "media-original", self.hash)

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
            wh.copy_to_local_warehouse(processed.name, "media-thumbnail", self.hash)
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
            wh.copy_to_local_warehouse(processed.name, "media-thumbnail", self.hash)
            processed.close()

        #log.debug("Created Media from file %s -> %s" % (self.name, self.hash))

        return self

    def sync(self):
        wh.copy_to_remote_warehouse("media-original", self.hash, self.name)
        wh.copy_to_remote_warehouse("media", self.hash, self.media_name)
        if self.type != "audio":
            wh.copy_to_remote_warehouse("media-thumbnail", self.hash, "thumb.jpg")
        return self

    def __unicode__(self):
        return self.name

    @property
    def mime_type(self):
        return self.type + "/" + self.subtype

    @property
    def media_name(self):
        exts = {
            "audio": "ogg",
            "image": self.subtype, # this just happens to work for PNG, GIF, JPEG
            "video": "flv"
        }
        return "%d.%s" % (self.id, exts[self.type])

    @property
    def original_url(self):
        "The URL of the original as-uploaded file"
        return "http://static.civicboom.com/media-originals/%s/%s" % (self.hash, self.name)

    @property
    def media_url(self):
        "The URL of the processed media, eg .flv file for video"
        return "http://static.civicboom.com/media/%s/%s" % (self.hash, self.media_filename)

    @property
    def thumbnail_url(self):
        "The URL of a JPEG-format thumbnail of this media"
        return "http://static.civicboom.com/media-thumbnails/%s/thumb.jpg" % (self.hash, )
