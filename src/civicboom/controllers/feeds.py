
from civicboom.lib.base   import *
from civicboom.lib.search import *

log = logging.getLogger(__name__)

class FeedsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('feed', 'feeds')

    def index(self, format='html'):
        """GET /feeds: All items in the collection"""
        # url('feeds')

    def create(self):
        """POST /feeds: Create a new item"""
        # url('feeds')

    def new(self, format='html'):
        """GET /feeds/new: Form to create a new item"""
        # url('new_feed')

    def update(self, id):
        """PUT /feeds/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('feed', id=ID),
        #           method='put')
        # url('feed', id=ID)

    def delete(self, id):
        """DELETE /feeds/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('feed', id=ID),
        #           method='delete')
        # url('feed', id=ID)

    def show(self, id, format='html'):
        """GET /feeds/id: Show a specific item"""
        # url('feed', id=ID)

    def edit(self, id, format='html'):
        """GET /feeds/id/edit: Form to edit an existing item"""
        # url('edit_feed', id=ID)
