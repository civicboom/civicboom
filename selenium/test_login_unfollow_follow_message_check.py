#!/usr/bin/env python

from selenium import selenium
import unittest, time, re

class Login_Unfollow_Follow_SendMessage_ReceiveMessage(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("test-browser-linux-master", 4444, "IE on Windows", "http://test.civicboom.com/")
        self.selenium.start()
    
    def test_login_unfollow_follow_sendmessage_receivemessage(self):
        sel = self.selenium
        sel.open("http://test.civicboom.com/#cbhJTdCJTIyYmxvY2tzJTIyJTNBJTVCJTVEJTdE")
        sel.click("link=Sign in")
        sel.wait_for_page_to_load("30000")
        sel.type("username", "unittest")
        sel.type("password", "password")
        sel.click("submit")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("A user for automated tests to log in as"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//img[@alt='unitfriend']")
        for i in range(60):
            try:
                if sel.is_element_present("link=Unfollow"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=Unfollow")
        for i in range(60):
            try:
                if sel.is_element_present("link=Follow"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=Follow")
        for i in range(60):
            try:
                if sel.is_element_present("link=Follow"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.click("link=Send Message")
        for i in range(60):
            try:
                if sel.is_element_present("subject"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        sel.type("subject", "this is a test message 123")
        sel.type("content", "rar")
        sel.click("css=td > input[type=submit]")
        sel.click("link__account_signout_POST")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Sign in")
        sel.wait_for_page_to_load("30000")
        sel.type("username", "unitfriend")
        sel.type("password", "password")
        sel.click("submit")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("1", sel.get_text("css=a.icon32.i_message > div.icon_overlay_red"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=a.icon32.i_message")
        for i in range(60):
            try:
                if sel.is_element_present("css=span.icon16.i_message"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("this is a test message 123", sel.get_text("css=p.subject"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("rar", sel.get_text("css=p.content"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("From: Mr U. Test", sel.get_text("css=p.timestamp"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link__account_signout_POST")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
