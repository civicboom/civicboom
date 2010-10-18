def overlay_errors(error, item_list, missing_list):
    """
    To be used in the form
    
        # Form validation
        try:
            schema = ?
            form   = schema.to_python(dict(request.params)) # Validate
        except formencode.Invalid, error:
            overlay_errors(error, settings_list(), missing_list) # Overlays error fields over the returned dict
            
            # Set error status
            edit_action['status']  = 'error'
            edit_action['message'] = error.msg #_('failed validation') # This is frustrating, if this a a decriptive error, then error.msg is fine, but normally this returns the whole dict with values and stuff, we need to tell users why the validation has failed
            return edit_action
    """
    # Form has failed validation
    form        = error.value
    form_errors = error.error_dict or {}
    
    # Set error property for each failed property

    for item in item_list:
        if 'name' in item:
            item_name = item['name']                            # For each setting
            if item_name in form:                                  #   If in form 
                item['value'] = form[item_name]                 #     populate value with form data
            if item_name in form_errors:                           #   If error
                e = form_errors[item_name]                         #     
                del form_errors[item_name]                         #     delete error object (so we can see if any are outstanding/missing at the end)
                if hasattr(e,'msg'): e = e.msg                             #     append error
                item['error'] = e                                       #
    
    # Report any missing fields (anything that is left in error.error_dict)
    if len(form_errors) > 0:
        #settings['missing'] = []
        for missing_name in form_errors.keys():
            e = form_errors[missing_name]
            if hasattr(e,'msg') : e = e.msg
            missing_list.append({'name':missing_name, 'description':missing_name, 'error':e, 'value':''})
    
    
    
    # Reference to validation code in settings
    """"
    # Form has failed validation
    form        = error.value
    form_errors = error.error_dict or {}
    
    # Set error property for each failed property
    for setting in settings_list():
        setting_fieldname = setting['name']                            # For each setting
        if setting_fieldname in form:                                  #   If in form 
            setting['value'] = form[setting_fieldname]                 #     populate value with form data
        if setting_fieldname in form_errors:                           #   If error
            e = form_errors[setting_fieldname]                         #     
            del form_errors[setting_fieldname]                         #     delete error object (so we can see if any are outstanding/missing at the end)
            if hasattr(e,'msg'): e = e.msg                             #     append error
            setting['error'] = e                                       #
    
    # Report any missing fields (anything that is left in error.error_dict)
    if len(form_errors) > 0:
        settings['missing'] = []
        for missing_fieldname in form_errors.keys():
            e = form_errors[missing_fieldname]
            if hasattr(e,'msg') : e = e.msg
            settings['missing'].append({'name':missing_fieldname, 'description':missing_fieldname, 'error':e, 'value':''})
    """