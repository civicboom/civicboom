from civicboom.lib.base import *
from civicboom.model import Media

from civicboom.lib.database.get_cached import get_content, get_member, get_media

# Logging setup
log      = logging.getLogger(__name__)


class MediaController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('medium', 'media')

    def index(self, format='html'):
        """GET /media: All items in the collection"""
        # url('media')

    def create(self):
        """
        POST /media: Create a new item

        With javascript/flash additional media can be uploaded individually
        """
        #user_log.debug("User is attempting to upload media:" + pprint.pformat(request.POST))
        form = request.POST
        if 'file_data' in form and 'content_id' in form and 'member_id' in form and 'key' in form:
            form_file = form["file_data"]
            content = get_content(int(form['content_id']))
            member  = get_member(int(form['member_id']))
            if not member.check_action_key("attach to %d" % content.id, form['key']):
                return "invalid action key"
            if not content.editable_by(member):
                return "can't edit this article"
            media = Media()
            media.load_from_file(tmp_file=form_file, original_name=form_file.filename)
            content.attachments.append(media)
            Session.commit()
            user_log.info("Media #%d appended to Content #%d using a key from Member #%d" % (media.id, content.id, member.id))
            return "ok"
        else:
            return "missing file_data or content_id"

    def new(self, format='html'):
        """GET /media/new: Form to create a new item"""
        # url('new_medium')

    def update(self, id):
        """PUT /media/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('medium', id=ID),
        #           method='put')
        # url('medium', id=ID)

    @auth
    @web
    def delete(self, id):
        """DELETE /media/id: Delete an existing item"""
        m = None
        try:
            m = Session.query(Media).get(id)
        except:
            pass
        if not m:
            raise action_error(_("No such media"), code=404)
        if m.attached_to.creator != c.logged_in_persona:
            raise action_error(_("Not your media"), code=403)
        
        user_log.info("Deleting Media #%d" % (m.id, ))
        Session.delete(m)
        Session.commit()
        return action_ok(_("Media deleted"), code=200)

    @web
    def show(self, id):
        """
        GET /media/id: Show a specific item

        Javascript can poll this method to get progress updates on the media processing
        Currently only return a flag to state if processing it taking place, but could
        be improved to return aditional progress info.
        """
        media = get_media(hash=id)
        if media:
            return action_ok(data={"media": media.to_dict(list_type='full')})
        else:
            raise action_error(_('media item not found'), code=404)

    def edit(self, id, format='html'):
        """GET /media/id/edit: Form to edit an existing item"""
        # url('edit_medium', id=ID)
