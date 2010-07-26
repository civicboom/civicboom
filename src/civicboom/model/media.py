from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean

from civicboom.model.meta import Base
import civicboom.lib.warehouse as wh

from pylons import config # used in generation of URL's for media, in no warehouse url then look localy

import magic
import Image
import tempfile
import os
import logging
import subprocess

log = logging.getLogger(__name__)

def media_path():
    if 'warehouse_url' in config: return config['warehouse_url']
    else                        : return ""



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
        """
        Create a Media object from a blob of data + upload form details
        """

        # Generate Hash and move file locally
        self.hash               = wh.hash_file(tmp_file)
        tmp_file                = wh.copy_to_local_warehouse(tmp_file, "media-original", self.hash)

        # Set up metadata
        self.name               = original_name
        self.caption            = caption if caption else u""
        self.credit             = credit  if credit  else u""
        self.type, self.subtype = magic.from_file(tmp_file, mime=True).split("/")
        

        # FIXME: turn tmp_file into something suitable for web viewing
        # TODO: processing should he handled in a separte thead and not block
        #       video thumbnails could have a placeholder thumb uploaded to warehouse first and then replaced once video transcoding complete
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
        """
        copy localy processed files to warehouse
        this will processed in a separte thead to allow this call to return quickly
          the thumbnail should not be uploaded in a separte thread
        """
        # TODO - thread copy to warehouse
        wh.copy_to_remote_warehouse("media-original", self.hash, self.name      )
        wh.copy_to_remote_warehouse("media"         , self.hash, self.media_name)
        if self.type != "audio":
            wh.copy_to_remote_warehouse("media-thumbnail", self.hash, "thumb.jpg")
            
        # TODO: have the local file removed after all threads have finished processing the content

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
        return "%s.%s" % (self.name, exts[self.type])

    @property
    def original_url(self):
        "The URL of the original as-uploaded file"
        return "%s/media-original/%s"         % (media_path(), self.hash) #/%s , self.name

    @property
    def media_url(self):
        "The URL of the processed media, eg .flv file for video"
        return "%s/media/%s"                   % (media_path(), self.hash) #/%s need to add filename to end for saving , self.name

    @property
    def thumbnail_url(self):
        "The URL of a JPEG-format thumbnail of this media"
        return "%s/media-thumbnail/%s" % (media_path(), self.hash )
