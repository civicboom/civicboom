"""
Set of helpers specificly to the Civicboom project
  (these are not part of misc because misc is more genereal functions that could be used in a range of projects)
"""


#-------------------------------------------------------------------------------
# Users in pending status are forced to complete the registration process.
#   some urls have to be made avalable to pending users (such as signout, etc)
def deny_pending_user(url_to_check):
    pending_user_allowed_list = ['register/new_user','account/signout']
    for url_safe in pending_user_allowed_list:
        if url_to_check.find(url_safe)>=0:
            return False
    return True


#-------------------------------------------------------------------------------
