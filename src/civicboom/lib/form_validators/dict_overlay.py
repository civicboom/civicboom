from civicboom.lib.base import _, action_error
import formencode

def validate_dict(data, schema, dict_to_validate_key=None, template_error=None):
    # Prepare dict to validate
    if dict_to_validate_key==None and len(data.keys())==1: #If dict only contains 1 key then validate that one key
        dict_to_validate_key = data.keys()[0]
    if dict_to_validate_key:
        dict_to_validate = data[dict_to_validate_key]
    
    # Validate
    try:
        dict_validated = schema.to_python(dict_to_validate)
    
    # Validation Failed
    except formencode.Invalid, error:
        dict_validated        = error.value
        dict_validated_errors = error.error_dict or {}
        
        # Record errors in data['invalid']
        invalid_dict = {}
        data['invalid'] = invalid_dict
        
        #print dict_validated
        #print dict_validated_errors
        
        for key in dict_validated_errors.keys():
            e = dict_validated_errors[key]
            if hasattr(e,'msg'): e = e.msg
            invalid_dict[key] = e
            
        #print "ERROR validation"
        #print data
        
        # Raise Validation Error
        raise action_error(
            status   = 'invalid' ,
            code     = 400 ,
            message  = _('failed validation') ,
            data     = data ,
            template = template_error ,
        )
    
    # Overlay validated dict back over data and return
    if dict_to_validate_key:
        data[dict_to_validate_key] = dict_validated
    
    return data