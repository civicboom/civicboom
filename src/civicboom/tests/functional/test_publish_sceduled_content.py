from civicboom.tests import *


class TestPublishSceduledContent(TestController):
    """
    Drafts can have the field 'auto_publish_trigger_datetime'
    If this is set the draft will be auto published on the closest hour
    
    Note this is a paid for feature and can only be set by plus users
    """
    pass