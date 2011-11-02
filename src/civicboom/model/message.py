from civicboom.model.meta import Base, CacheChangeListener

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Unicode, UnicodeText
from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import DDL
from cbutils.misc import now
import copy


class Message(Base):
    __tablename__ = "message"
    __mapper_args__ = {'extension': CacheChangeListener()}
    id          = Column(Integer(),     primary_key=True)
    source_id   = Column(String(32),    ForeignKey('member.id', onupdate="cascade"), nullable=True)
    target_id   = Column(String(32),    ForeignKey('member.id', onupdate="cascade"), nullable=True, index=True)
    timestamp   = Column(DateTime(),    nullable=False, default=now)
    subject     = Column(Unicode(),     nullable=False)
    content     = Column(UnicodeText(), nullable=False)
    read        = Column(Boolean(),     nullable=False, default=False)

    target      = relationship("Member", primaryjoin="Message.target_id==Member.id", backref=backref('messages_to'  , cascade="all, delete-orphan"))
    source      = relationship("Member", primaryjoin="Message.source_id==Member.id", backref=backref('messages_from', cascade="all, delete-orphan"))

    flags       = relationship("FlaggedEntity" , backref=backref('offending_message'), cascade="all,delete-orphan")

    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'           : None ,
            #'type'         : lambda message: message.__type__(),  # AllanC - the message type is based on who is observing it, a message could be 'sent' or 'to' depending on the viewing user. This adds complications # Now added to messages index
            'source_id'    : None ,
            'target_id'    : None ,
            'timestamp'    : None ,
            'subject'      : None ,
            'content'      : None ,
            'read'         : None ,
        },
    })
    __to_dict__.update({
        'full'         : copy.deepcopy(__to_dict__['default']) ,
        #'full+actions': copy.deepcopy(__to_dict__['default']) ,
    })
    __to_dict__['full'].update({
            'source'       : lambda message: message.source.to_dict() if message.source!=None else None ,
            'source_name'  : lambda message: str(message.source),
            'target'       : lambda message: message.target.to_dict() if message.target!=None else None ,
            'target_name'  : lambda message: str(message.target),
    })

    def __unicode__(self):
        return "%s: %s" % (self.subject, self.content)

    def __link__(self):
        from civicboom.lib.web import url
        return url('message', id=self.id, sub_domain='www', qualified=True)

    def invalidate_cache(self, remove=False):
        from civicboom.lib.cache import invalidate_message
        invalidate_message(self, remove=remove)

    def __type__(self, member=None):
        """
         oh jesus, this is duplicated in the messages_index method as well as a post to_dict overlay
        """
        try:
            member = member.id
        except:
            pass
        if not member:
            return None
        if     self.source_id == member and     self.target_id          :
            return 'sent'
        if     self.source_id == member and not self.target_id          :
            return 'public'
        if     self.source_id           and     self.target_id == member:
            return 'to'
        if not self.source_id           and     self.target_id == member:
            return 'notification'


    def delete(self):
        from civicboom.lib.database.actions import del_message
        return del_message(self)

    def flag(self, **kargs):
        """
        Flag message
        """
        from civicboom.lib.database.actions import flag
        flag(self, **kargs)

DDL('DROP TRIGGER IF EXISTS update_num_unread ON message').execute_at('before-drop', Message.__table__)
DDL("""
CREATE OR REPLACE FUNCTION update_num_unread() RETURNS TRIGGER AS $$
    DECLARE
        tmp_target_id text;
    BEGIN
        -- UPDATE changing the target ID should never happen
        tmp_target_id := CASE WHEN TG_OP='DELETE' THEN OLD.target_id ELSE NEW.target_id END;

        UPDATE member SET num_unread_messages = (
            SELECT COUNT(message.id)
            FROM message
            WHERE
                message.target_id=member.id AND
                message.source_id IS NOT NULL AND
                NOT message.read
        ) WHERE member.id = tmp_target_id;
        UPDATE member SET num_unread_notifications = (
            SELECT COUNT(message.id)
            FROM message
            WHERE
                message.target_id=member.id AND
                message.source_id IS NULL AND
                NOT message.read
        ) WHERE member.id = tmp_target_id;
        UPDATE member SET last_message_timestamp = (
            SELECT timestamp
            FROM message
            WHERE
                message.target_id=member.id AND
                message.source_id IS NOT NULL
            ORDER BY message.id DESC
            LIMIT 1
        ) WHERE member.id = tmp_target_id;
        UPDATE member SET last_notification_timestamp = (
            SELECT timestamp
            FROM message
            WHERE
                message.target_id=member.id AND
                message.source_id IS NULL
            ORDER BY message.id DESC
            LIMIT 1
        ) WHERE member.id = tmp_target_id;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_num_unread
    AFTER INSERT OR UPDATE OR DELETE ON message
    FOR EACH ROW
    EXECUTE PROCEDURE update_num_unread();
""").execute_at('after-create', Message.__table__)
