#!/usr/bin/env python

from selenium import selenium
from cbtest import CBTestCase
import unittest, time, re

class UserSearch(CBTestCase):
    def test_empty(self):
        sel = self.selenium
        sel.open("/reporter/profile/AllanC")
        sel.click("link=Search users")
        sel.wait_for_page_to_load("30000")
        sel.click("search")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Your search returned no results."))
        except AssertionError, e: self.verificationErrors.append(str(e))

    def test_allanc(self):
        sel = self.selenium
        sel.open("/search/do_reporter_search")
        sel.click("link=Search users")
        sel.wait_for_page_to_load("30000")
        sel.type("reportername", "allanc")
        sel.click("search")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Your search returned 1 result:"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='main']/div/div[3]/div[2]/div/div[2]/div[1]/a/span")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Joined: 	12/08/2009"))
        except AssertionError, e: self.verificationErrors.append(str(e))

    def test_callaghan(self):
        sel = self.selenium
        sel.open("/search/do_reporter_search")
        sel.click("link=Search users")
        sel.wait_for_page_to_load("30000")
        sel.type("reportername", "callaghan")
        sel.click("search")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Your search returned no results."))
        except AssertionError, e: self.verificationErrors.append(str(e))

if __name__ == "__main__":
    unittest.main()
