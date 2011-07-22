import sqlalchemy.orm.query
from sqlalchemy.util import NamedTuple

from cbutils.misc import str_to_int
from civicboom.lib.web import action_ok

__all__ = [
    "list_to_apilist",
]

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
        if not list_to_dict_transform:
            list_to_dict_transform = default_transform
        try:
            return list_to_dict_transform(results, **kwargs)
        except:
            return results
    
    if not results:
        return apilist([], obj_type=kwargs.get('obj_type'))
    
    # lakdsjghaldfkgjsd.
    # using config variables in the middle of the libraries may be a bad idea
    from cbutils.worker import config as w_config
    from pylons import config as p_config
    limit_default = w_config.get('search.default.limit.contents') or p_config.get('search.default.limit.contents')

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
