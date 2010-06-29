#!/usr/bin/env python

from selenium import selenium
from cbtest import CBTestCase
import unittest, time, re

class StatusUpdates(CBTestCase):
    def test_update(self):
        sel = self.selenium
        sel.open("/reporter/myhome")
        sel.type("instant_news_text", "I like kittens")
        sel.click("//input[@value='Update instant news']")
        sel.wait_for_page_to_load("30000")
        sel.click("//div[@id='col_left']/div/div[1]/a/strong")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Instant Update: I like kittens"))
        except AssertionError, e: self.verificationErrors.append(str(e))

    def test_empty(self):
        sel = self.selenium
        sel.open("/reporter/profile/unittest")
        sel.click("link=Goto MyHome")
        sel.wait_for_page_to_load("30000")
        sel.type("instant_news_text", "")
        sel.click("//input[@value='Update instant news']")
        sel.wait_for_page_to_load("30000")
        sel.click("//img[@alt='unittest']")
        sel.wait_for_page_to_load("30000")
        # FIXME: is this supposed to be shown?
        try: self.failUnless(sel.is_text_present("Instant Update:"))
        except AssertionError, e: self.verificationErrors.append(str(e))

    def test_long(self):
        sel = self.selenium
        sel.open("/reporter/myhome/unittest")
        sel.type("instant_news_text", "I like kittens and using lots of words to go over the limits of this box, will it recommend I stop, or will it just not let me type any more")
        sel.click("//input[@value='Update instant news']")
        sel.wait_for_page_to_load("30000")
        sel.click("//img[@alt='unittest']")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Instant Update: I like kittens and using lots of words to go over the limits of this box, will it recommend I stop, or will it just not let me type any more"))
        except AssertionError, e: self.verificationErrors.append(str(e))

if __name__ == "__main__":
    unittest.main()
