# vim: set fileencoding=utf8:

from civicboom.tests import *


class TestWidgetController(TestController):
    
    def test_widget(self):
        
        widget_var_prefix = self.config_var("setting.widget.var_prefix")
        
        def get_widget(*args, **kwargs):
            """
            Fake all get requests with the widget subdomain
            """
            if not kwargs:
                kwargs = {}
            if 'extra_environ' not in kwargs:
                kwargs['extra_environ'] = {'HTTP_HOST': 'widget.civicboom.com'}
            return self.app.get(*args, **kwargs)

        def widget_vars(*args, **kwargs):
            widget_var_kwargs = {}
            for key,value in kwargs.iteritems():
                widget_var_kwargs[widget_var_prefix+key] = value
            return widget_var_kwargs
        
        # Default widget page - no params
        response = get_widget('/')
        self.assertNotEquals(None, response)
        
        response = get_widget(url('member', id='unittest'))
        self.assertIn('CivicboomWidget-basic', response.body)
        self.assertIn('unittest', response.body)
        
        response = get_widget(url('member_action', id='unittest', action='content_and_boomed'))
        self.assertIn('CivicboomWidget-basic', response.body)
        self.assertIn('API Documentation', response.body)
        
        response = get_widget(url('content', id='1'))
        self.assertIn('unittest', response.body)
        self.assertIn('CivicboomWidget-basic', response.body)
        self.assertIn('API Documentation'          , response.body)
        self.assertNotIn('API Documentation: Response', response.body) # Responses are not included in widget by default anymore - this is a user option
        
        response = get_widget(url('content', id='1', **widget_vars(show_responses='True', button_respond='Bob') ))
        self.assertIn('API Documentation: Response', response.body)
        self.assertIn('Bob'                        , response.body)
        
        
        # Test gradient widget
        response = get_widget(url('member_action', id='unittest', action='assignments_active', **widget_vars(theme='gradient') ))
        self.assertIn('CivicboomWidget-gradient', response.body)
        
        response = get_widget(url('member',        id='unittest',                              **widget_vars(theme='gradient') ))
        self.assertIn('CivicboomWidget-gradient', response.body)
        
        
        # Test unicode widget vars/params
        response = get_widget(url('member',        id='unittest',                              **widget_vars(title='这', button_respond='ώ') ))
        self.assertIn('这', response.body)
