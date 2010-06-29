
from selenium import selenium
import unittest

class CBTestCase(unittest.TestCase):
    def setUp(self):
        # connect
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome /usr/lib/firefox-3.6.3/firefox-bin", "http://test.civicboom.com/")
        self.selenium.start()

        # log in
        sel = self.selenium
        sel.open("/")
        sel.click("link=Sign in or Sign up")
        sel.wait_for_page_to_load("30000")
        sel.type("username", "unittest")
        sel.type("password", "unittest123")
        sel.click("submit")
        sel.wait_for_page_to_load("30000")

    def tearDown(self):
        # log out
        sel = self.selenium
        sel.open("/article/view/345")
        sel.click("link=Sign out")
        sel.wait_for_page_to_load("30000")
        sel.click("flash_message")
        try: self.failUnless(sel.is_text_present("Successfully signed out!"))
        except AssertionError, e: self.verificationErrors.append(str(e))

        # disconnect
        self.selenium.stop()
        self.assertEqual([], filter(lambda x: len(x)>0, self.verificationErrors))

