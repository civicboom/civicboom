import sqlalchemy.orm.query
from sqlalchemy.util import NamedTuple

from cbutils.misc import str_to_int
from civicboom.lib.web import action_ok

import logging
log  = logging.getLogger(__name__)

kwargs_to_exclude_in_api_output = ['limit','offset','obj_type']


def __apilist(results, count=0, limit=0, offset=0, obj_type=None, source_kwargs={}):
    kwargs = {}
    for key, value in source_kwargs.iteritems():
        if key not in kwargs_to_exclude_in_api_output:
            try:
                value = value.__db_index__()
            except Exception as e:
                pass
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


def to_apilist(results=[], list_to_dict_transform=None, **kwargs):
    """
    """
    # fixme: what else is there?
    #assert isinstance(results, list) or isinstance(results, sqlalchemy.orm.query.Query)
    
    if not results:
        return __apilist([], obj_type=kwargs.get('obj_type'))

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
