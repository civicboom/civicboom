from civicboom.model.member import User

from civicboom.model.meta   import Session


#-------------------------------------------------------------------------------
# Cashe Management - Part 1
#-------------------------------------------------------------------------------
# A collection of functions used to setup + assit with caching
# Part 2 contains all the functions for invalidating the cache and must be defined after the cached functions



#-------------------------------------------------------------------------------
# Database Object Gets - Cached - Get data from database that is cached
#-------------------------------------------------------------------------------
# Most methods will have a get_stuff and get_stuff_nocache. As the cache is a decorator we can bypass the cache by calling the _nocache variant
def get_user_nocache(user):
  try:
    return Session.query(User).filter_by(username=user).one()
  except:
    try:
      return Session.query(User).filter_by(email=user).one()
    except:
      try:
        return Session.query(User).filter_by(id=user).one()
      except:
        pass
  return None
#@cache_test.cache() #Cache decorator to go here
def get_user(user):
  if not user             : return None
  if isinstance(user,User): return user
  return get_user_nocache(user)


#-------------------------------------------------------------------------------
# Database List Gets - Cached - Get data lists from database that is cached
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Cache Management - Part 2 - Invalidating the Cache
#-------------------------------------------------------------------------------

