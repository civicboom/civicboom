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
        self.assertIn('API Documentation: Response', response.body)
        
        
        # Test gradient widget
        response = get_widget(url('member_action', id='unittest', action='assignments_active', **{widget_var_prefix+'theme':'gradient'}))
        self.assertIn('CivicboomWidget-gradient', response.body)
        
        response = get_widget(url('member',        id='unittest',                              **{widget_var_prefix+'theme':'gradient'}))
        self.assertIn('CivicboomWidget-gradient', response.body)