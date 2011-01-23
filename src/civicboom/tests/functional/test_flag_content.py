from civicboom.tests import *

#import json
import datetime



class TestFlagContentController(TestController):

    #---------------------------------------------------------------------------
    # Flag then Deflag Content
    #---------------------------------------------------------------------------
    def test_flag_deflag_content(self):
        """
        create content
        new user log in
        flag
        admin login
        check email generated
        deflag content
        """
        pass

    #---------------------------------------------------------------------------
    # Flag then take offline Content
    #---------------------------------------------------------------------------
    def test_flag_disable_content(self):
        """
        create content
        new user log in
        flag
        admin login
        check email generated
        take content offline
        """
        pass


    #---------------------------------------------------------------------------
    # Test Profanity Filter
    #---------------------------------------------------------------------------
    def test_flag_content(self):
        """
        create content with 'naughty words'
        check alert sent
        on admin pannel
        admin take offline
        """
        pass
