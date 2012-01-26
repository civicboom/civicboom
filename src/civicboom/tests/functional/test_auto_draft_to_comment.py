from civicboom.tests import *
from pylons import config

from nose.plugins.skip import SkipTest

class TestAutoDraftToComment(TestController):

    #---------------------------------------------------------------------------
    # Assignment Limit
    #---------------------------------------------------------------------------
    def test_draft_to_comment(self):
        """
        """
        
        raise SkipTest('Feature disabled at customer request')
        
        #-----------------------------------------------------------------------
        # Create assignment 
        assignment_id =self.create_content(title   = 'auto_draft_to_comment',
                                           content = 'Automated test to test that drafts when published that are less than config[setting.content.max_comment_length] are auto converted to comments',
                                           type    = 'assignment')
        
        # Swich to another user
        self.log_in_as('unitfriend')
        
        #-----------------------------------------------------------------------
        # Auto convert draft -> comment
        
        # Create draft to above assignment - with less than config[setting.content.max_comment_length]
        draft_id_1 =self.create_content(title     = 'auto_draft_to_comment_response',
                                        content   = '<p>auto_draft_to_comment_response</p>', # The HTML should be removed because comments should not have HTML in
                                        type      = 'draft',
                                        parent_id = assignment_id)
        
        # Check draft is in place
        response      = self.app.get(url('content', id=draft_id_1, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals('draft', response_json['data']['content']['type'])
        
        # Publish draft - BUT! as content is less than config[setting.content.max_comment_length] it SHOULD audo convert to comment
        self.publish_content(draft_id_1)
        
        # Check comments on assignment has 'auto_draft_to_comment_response' as first comment
        response      = self.app.get(url('content', id=assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals('auto_draft_to_comment_response', response_json['data']['comments']['items'][0]['content'])
        
        
        
        #-----------------------------------------------------------------------
        # DONT Auto convert draft -> comment
        
        # Create draft to above assignment - with less than config[setting.content.max_comment_length]
        draft_id_2 =self.create_content(title     = 'auto_draft_to_comment_response_too_long',
                                        content   = 'auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long auto_draft_to_comment_response_too_long ',
                                        type      = 'draft',
                                        parent_id = assignment_id)
        
        # Check draft is in place
        response      = self.app.get(url('content', id=draft_id_2, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals('draft', response_json['data']['content']['type'])
        
        # Publish draft - as content is MORE than config[setting.content.max_comment_length] it WILL NOT auto convert to comment
        self.publish_content(draft_id_2)
        
        # Check comments on assignment has 'auto_draft_to_comment_response' as first comment
        response      = self.app.get(url('content', id=assignment_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals('auto_draft_to_comment_response_too_long', response_json['data']['responses']['items'][0]['title'])
        
        #-----------------------------------------------------------------------
        # Cleanup
        self.delete_content(draft_id_1)
        self.delete_content(draft_id_2)
        
        self.log_in_as('unittest')
        self.delete_content(assignment_id)
