
from civicboom.model.meta import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import DDL
from cbutils.misc import now
import copy


class Message(Base):
    __tablename__ = "message"
    id          = Column(Integer(),     primary_key=True)
    source_id   = Column(Integer(),     ForeignKey('member.id'), nullable=True)
    target_id   = Column(Integer(),     ForeignKey('member.id'), nullable=True, index=True)
    timestamp   = Column(DateTime(),    nullable=False, default=now)
    subject     = Column(Unicode(),     nullable=False)
    content     = Column(UnicodeText(), nullable=False)
    read        = Column(Boolean(),     nullable=False, default=False)

    target      = relationship("Member", primaryjoin="Message.target_id==Member.id", backref=backref('messages_to'  , cascade="all, delete-orphan"))
    source      = relationship("Member", primaryjoin="Message.source_id==Member.id", backref=backref('messages_from', cascade="all, delete-orphan"))


    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'           : None ,
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

    def delete(self):
        from civicboom.lib.database.actions import del_message
        return del_message(self)

DDL('DROP TRIGGER IF EXISTS update_num_unread ON message').execute_at('before-drop', Message.__table__)
DDL("""
CREATE OR REPLACE FUNCTION update_num_unread() RETURNS TRIGGER AS $$
    DECLARE
        tmp_target_id integer;
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
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_num_unread
    AFTER INSERT OR UPDATE OR DELETE ON message
    FOR EACH ROW
    EXECUTE PROCEDURE update_num_unread();
""").execute_at('after-create', Message.__table__)
