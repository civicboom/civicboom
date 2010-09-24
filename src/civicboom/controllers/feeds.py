
from civicboom.lib.base   import *
from civicboom.lib.search import *
from civicboom.model      import Feed, Content

log = logging.getLogger(__name__)


def _post_to_query(params):
    if 'query' in params:
        query = AndFilter([
            OrFilter([
                TextFilter("terrorists"),
                AndFilter([
                    LocationFilter([1, 51], 10),
                    TagFilter("Science & Nature")
                ]),
                AuthorFilter("unittest")
            ]),
            NotFilter(OrFilter([
                TextFilter("waffles"),
                TagFilter("Business")
            ]))
        ])
    else: # default query to be edited
        query = AndFilter([
            OrFilter([
                LabelFilter("List the things you want to see here"),
            ]),
            NotFilter(OrFilter([
                LabelFilter("Filter out what you don't want to see here"),
            ]))
        ])
    return query


class FeedsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('feed', 'feeds')

    @auto_format_output()
    @authorize(is_valid_user)
    def index(self, format='html'):
        """GET /feeds: All items in the collection"""
        # url('feeds')
        c.viewing_user = c.logged_in_user
        return action_ok(
            data={"feeds": [
                {"id": f.id, "name": f.name, "query": str(f.query)}
                for f in c.viewing_user.feeds
            ]}
        )

    @auto_format_output()
    @authorize(is_valid_user)
    def create(self):
        """POST /feeds: Create a new item"""
        # url('feeds')
        try:
            f = Feed()
            f.name = request.POST['name']
            f.query = _post_to_query(request.POST)
            c.logged_in_user.feeds.append(f)
            Session.commit()
            return action_ok(_("Feed created"), code=201)
        except Exception, e:
            return action_error(_("Error creating feed"), code=500)

    @auto_format_output()
    @authorize(is_valid_user)
    def new(self, format='html'):
        """GET /feeds/new: Form to create a new item"""
        # url('new_feed')
        return action_ok()

    @auto_format_output()
    @authorize(is_valid_user)
    def update(self, id):
        """PUT /feeds/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('feed', id=ID),
        #           method='put')
        # url('feed', id=ID)
        f = Session.query(Feed).filter(Feed.id==id).first()
        if not f:
            return action_error(_("No such feed"), code=404)
        if f.member != c.logged_in_user:
            return action_error(_("Not your feed"), code=403)

        f.name = request.POST['name']
        f.query = _post_to_query(request.POST)
        return action_ok(_("Feed updated"), code=200)

    @auto_format_output()
    @authorize(is_valid_user)
    def delete(self, id):
        """DELETE /feeds/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('feed', id=ID),
        #           method='delete')
        # url('feed', id=ID)
        f = Session.query(Feed).filter(Feed.id==id).first()
        if not f:
            return action_error(_("No such feed"), code=404)
        if f.member != c.logged_in_user:
            return action_error(_("Not your feed"), code=403)

        Session.delete(f)
        Session.commit()
        return action_ok(_("Feed deleted"), code=200)

    @auto_format_output()
    def show(self, id, format='html'):
        """GET /feeds/id: Show a specific item"""
        # url('feed', id=ID)
        f = Session.query(Feed).filter(Feed.id==id).first()
        if not f:
            return action_error(_("No such feed"), code=404)

        results = Session.query(Content)
        results = results.filter(sql(f.query))
        results = filter(lambda content: content.viewable_by(c.logged_in_user), results)
        results = results[0:20]
        return action_ok(
            data={"name": f.name, "results": results}
        )

    @auto_format_output()
    @authorize(is_valid_user)
    def edit(self, id, format='html'):
        """GET /feeds/id/edit: Form to edit an existing item"""
        # url('edit_feed', id=ID)
        f = Session.query(Feed).filter(Feed.id==id).first()
        if not f:
            return action_error(_("No such feed"), code=404)
        if f.member != c.logged_in_user:
            return action_error(_("Not your feed"), code=403)

        # ...
        return action_ok(data={"feed": f})
