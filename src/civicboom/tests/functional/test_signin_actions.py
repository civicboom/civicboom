from civicboom.tests import *

class TestSigninActions(TestController):

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
         - civicboom.lib.civicboom_lib:get_action_objects_for_url():action_list
        """
        def get(*args, **kwargs):
            response = self.app.get(*args, **kwargs)
            if response.status >= 300 and response.status <= 399:
                response = response.follow()
            return response
        
        def run_get_actions(action_responses, **kwargs):
            for action_response in action_responses:
                response = get(action_response[0], **kwargs)
                self.assertIn(action_response[1], response.body)
        
        # Get when logged in - but directed from another website - test XsiteForgery messaage
        
        action_responses = [
            ('/members/unittest/follow'         ,'want to <b>follow '        ),
            ('/contents/1/boom'                 ,'want to <b>boom '            ),
            ('/contents/new?parent_id=1'        ,'want to <b>create a response'),
            ('/contents/new?target_type=article','want to <b>post a '      ),
        ]
        run_get_actions(action_responses, status=403)
        
        self.log_out()
        
        action_responses = [
            ('/members/unittest/follow'         ,'you will follow'  ), # AllanC - im annoyed that these all get replaced with a stock message rather than telling them what they are going to perform, will need to disscuss this
            ('/contents/1/boom'                 ,'you will Boom'    ),
            ('/contents/new?parent_id=1'        ,'you will respond' ),
            ('/contents/new?target_type=article','you will '        ),
        ]
        run_get_actions(action_responses)
