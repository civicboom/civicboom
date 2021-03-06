import sqlalchemy.orm.query
from sqlalchemy.util import NamedTuple

from cbutils.misc import str_to_int
from civicboom.lib.web import action_ok
from cbutils.cbtv import log as t_log

import logging
log  = logging.getLogger(__name__)

# lakdsjghaldfkgjsd.
# using config variables in the middle of the libraries may be a bad idea
from cbutils.worker import config as w_config
from pylons import config as p_config
limit_default = w_config.get('search.default.limit.contents') or p_config.get('search.default.limit.contents')

# Constants
valid_obj_types = ['contents', 'members', 'messages']
kwargs_to_exclude_in_api_output = ['limit','offset','obj_type','exclude_content','exclude_members','lists'] # AllanC - these are no longer needed as they are stripped in web_parms to kwargs - 'controller','sub_domain','action','format'


def __apilist(results, count=0, limit=0, offset=0, obj_type=None, source_kwargs={}):
    if obj_type:
        assert obj_type in valid_obj_types
    kwargs = {}
    for key, value in source_kwargs.iteritems():
        if not (key in kwargs_to_exclude_in_api_output or key.startswith('_')):
            try   : value = value.id # AllanC - get id's of any object types
            except: pass
            if isinstance(value, list):
                value = ','.join(value)
            # AllanC - it may be wise here to look to all objects that are ok .. like int, float, date ... but raise warnings on actual objects that arrive at this point
            value = unicode(value)
            if value:
                kwargs[key] = value

    return action_ok(
        data = {'list': {
            'items' : results   ,
            'count' : count     ,
            'limit' : limit     ,
            'offset': offset    ,
            'type'  : obj_type  ,
            'kwargs': kwargs    , # AllanC - we include the kwargs so that the source of this list can be reporduced by 3rd party clients if needed
            }
        }
    )


def __default_transform(results, **kwargs):
    r = []
    for row in results:
        if type(row) == NamedTuple:
            # we did query.add_column somewhere, so sqlalchemy gave us
            # [(object, extra_column), ...] rather than [object, ...]
            # here we turn
            #    [ ( Content, distance ), ... ]
            # into
            #    [ Content-with-distance-inserted, ... ]
            dic = None
            for column_id, column_name in enumerate(row.keys()):
                if column_id == 0:
                    # first column is the object
                    dic = row[column_id].to_dict(**kwargs)
                else:
                    # latter columns are calculated fields to insert
                    dic[column_name] = row[column_id]
            r.append(dic)
        else:
            r.append(row.to_dict(**kwargs))
    return r


def __list_to_dict(results, list_to_dict_transform=None, **kwargs):
    if not list_to_dict_transform:
        list_to_dict_transform = __default_transform
    try:
        return list_to_dict_transform(results, **kwargs)
    except:
        return results

def __to_idlist(results=[], **kwargs):
    if isinstance(results, sqlalchemy.orm.query.Query):
        # AllanC - this is making the asumption that the Query was created with Session.query(Member.id)...etc
        #return [id_tuple[0] for id_tuple in results.all()]
        # Alternate - it is possible to return a list of just values with Session.query(Member)....values(Member.id) but we have to know what type of object it is
        #from civicboom.model import Content
        #return [id_tuple[0] for id_tuple in results.values(Content.id)]
        
        # HACK - to get the functionality in place ive put this horribly inefficent rip of the id's. This can be replaced later by some simple direct querying
        results = results.all()
    
    if isinstance(results, list):
        try:
            results = [result.id for result in results]
        except:
            try:
                results = [result['id'] for result in results]
            except:
                raise Exception('unable to process results list')
    return action_ok(
        data = {
            'idlist': results
        }
    )
    

@t_log("to_apilist")
def to_apilist(results=[], list_to_dict_transform=None, **kwargs):
    """
    """
    # fixme: what else is there?
    #assert isinstance(results, list) or isinstance(results, sqlalchemy.orm.query.Query)

    if kwargs.get('list_type')=='id':
        return __to_idlist(results, **kwargs)
    
    if not results:
        return __apilist([], obj_type=kwargs.get('obj_type'))
        
    # OLD PLACE FOR limit_default defenition

    limit  = str_to_int(kwargs.get('limit' ), limit_default)
    offset = str_to_int(kwargs.get('offset')               )
    
    if isinstance(results, sqlalchemy.orm.query.Query):
        count   = results.count()
        results = results.limit(limit).offset(offset)
        return __apilist(
            __list_to_dict(results.all(), list_to_dict_transform, **kwargs),
            count=count, limit=limit, offset=offset, obj_type=kwargs.get('obj_type'), source_kwargs=kwargs
        )
    
    if isinstance(results, list):
        count = len(results)
        end_point = None
        if limit:
            end_point = offset + limit
        results = results[offset:end_point]
        return __apilist(
            __list_to_dict(results, list_to_dict_transform, **kwargs),
            count=count, limit=limit, offset=offset, obj_type=kwargs.get('obj_type'), source_kwargs=kwargs
        )
