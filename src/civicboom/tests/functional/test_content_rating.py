from civicboom.tests import *


class TestContentRating(TestController):
    
    def test_rate_content(self):
        
        def rate(content_id, rating):
            response = self.app.post(
                url('content_action', action='rate', id=content_id, format='json'),
                params={
                    '_authentication_token': self.auth_token,
                    'rating': rating,
                },
                status=200
            )
        
        content_id = self.create_content(title='Rating Test', content='Testing the rating system')
        
        content_response = self.get_content(content_id)
        self.assertEqual(content_response['content']['rating'], 0)
        
        rate(content_id, 3)
        
        content_response = self.get_content(content_id)
        self.assertGreater(content_response['content']['rating'], 0)
        
        rate(content_id, 0) # Should remove rating
        
        content_response = self.get_content(content_id)
        self.assertEqual(content_response['content']['rating'], 0)
        
        # AllanC - Shish has written magical Shish code that trancends time and space and does some crazzy weighting system pruning the top 5% of extreems and doing magic.
        #          without understanding and reproducing this algorithum I cant test it in detail
        
        self.delete_content(content_id)