from pylons import config
import sqlalchemy.orm.query
from sqlalchemy.util import NamedTuple

from cbutils.misc import str_to_int
from civicboom.lib.web import action_ok

__all__ = [
    "list_to_apilist",
]

limit_default = config['search.default.limit.contents']

#-------------------------------------------------------------------------------
# Public
#-------------------------------------------------------------------------------


def to_apilist(results=[], list_to_dict_transform=None, **kwargs):

    def apilist(results, count=0, limit=0, offset=0, obj_type=None):
        return action_ok(
            data = {'list': {
                'items' : results   ,
                'count' : count     ,
                'limit' : limit     ,
                'offset': offset    ,
                'type'  : obj_type  ,
                }
            }
        )
    
    def list_to_dict(results, list_to_dict_transform=None, **kwargs):
        def default_transform(results, **kwargs):
            r = []
            for i in results:
                if type(i) == NamedTuple:
                    # we did query.add_column somewhere, so sqlalchemy gave us [(object, extra_column), ...] rather than [object, ...]
                    r.append(i[0].to_dict(**kwargs))
                else:
                    r.append(i.to_dict(**kwargs))
            return r
        if not list_to_dict_transform:
            list_to_dict_transform = default_transform
        try:
            return list_to_dict_transform(results, **kwargs)
        except:
            return results
    
    if not results:
        return apilist([], obj_type=kwargs.get('obj_type'))
    
    limit  = str_to_int(kwargs.get('limit' ), limit_default)
    offset = str_to_int(kwargs.get('offset')               )
    
    if isinstance(results, sqlalchemy.orm.query.Query):
        count   = results.count()
        results = results.limit(limit).offset(offset)
        return apilist(
            list_to_dict(results.all(), list_to_dict_transform, **kwargs),
            count=count, limit=limit, offset=offset, obj_type=kwargs.get('obj_type')
        )
    
    if isinstance(results, list):
        count = len(results)
        end_point = None
        if limit:
            end_point = offset + limit
        results = results[offset:end_point]
        return apilist(
            list_to_dict(results, list_to_dict_transform, **kwargs),
            count=count, limit=limit, offset=offset, obj_type=kwargs.get('obj_type')
        )

    raise Exception('unsupported list type')
