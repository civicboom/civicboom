from civicboom.tests import *



class TestSigninActions(TestController):

    def get(self, *args, **kwargs):
        response = self.app.get(*args, **kwargs)
        if response.status >= 300 and response.status <= 399:
            response = response.follow(**kwargs)
        return response

    #---------------------------------------------------------------------------
    # Signin Actions
    #---------------------------------------------------------------------------
    def test_signin_actions(self):
        """
        There are a number of actions that a user can be directed to from external sites.
        We need to simulate the triggering of these to check that the correct messaging is being used
        
        This is done in 2 ways:
          as a logged in user comming from another site
          as a non logged in user, encouraging them to signup
        
        See
         - civicboom.lib.constants:get_action_objects_for_url():action_list
        """
        
        def run_get_actions(action_responses, **kwargs):
            for action_response in action_responses:
                response = self.get(action_response[0], **kwargs)
                self.assertIn(action_response[1], response.body)
        
        # Get when logged in - but directed from another website - test XsiteForgery messaage
        
        action_responses = [
            ('/members/unittest/follow'         ,'want to <b>follow '          ),
            ('/contents/1/boom'                 ,'want to <b>boom '            ),
            ('/contents/new?parent_id=1'        ,'want to <b>create a response'),
            ('/contents/new?target_type=article','want to <b>post a '          ),
            # comments needed
            #('/contents/new'                    ,'????????'          ),
        ]
        run_get_actions(action_responses, status=403)
        
        self.log_out()
        
        action_responses = [
            ('/members/unittest/follow'         ,'you will follow'  ), # AllanC - im annoyed that these all get replaced with a stock message rather than telling them what they are going to perform, will need to disscuss this
            ('/contents/1/boom'                 ,'you will Boom'    ),
            ('/contents/new?parent_id=1'        ,'you will respond' ),
            ('/contents/new?target_type=article','you will '        ),
            # comments needed
            ('/contents/new'                    ,'create new content'),
        ]
        run_get_actions(action_responses)


    #---------------------------------------------------------------------------
    # Signin Actions - on mobile
    #---------------------------------------------------------------------------

    def test_signin_actions_mobile(self):
        
        # When logged in - follow without authentication token - should trigger cross site check
        #response = self.get('/members/unittest/follow', extra_environ={'HTTP_HOST': 'm.c.localhost'}, status=403)
        #self.assertIn('want to <b>follow ', response.body)
        #self.assertIn('mobileinit'        , response.body) # Check for string ONLY in mobile_base - the mobileinit method
        
        self.log_out()
        
        # Logged out, should provide a customised signin page with description of the action to perform
        # AllanC - TODO - This test fails .. this test tests for the CORRECT behaviour! we need the mobile signin page to be view here
        response = self.get('/members/unittest/follow', extra_environ={'HTTP_HOST': 'm.c.localhost'})
        self.assertIn('you will follow', response.body)
        self.assertIn('mobileinit'     , response.body)
