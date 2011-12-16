from civicboom.tests import *
from BeautifulSoup import BeautifulSoup

from pylons import config
from nose.plugins.skip import SkipTest

# This regexp will match any url starting with http(s):// not within civicboom.com or just # or mailto:*
not_civicboom = re.compile(r'((http(s{0,1})://(?!(www\.){0,1}civicboom\.com))|#|mailto\:.*).*')


class TestCrawlSite(TestController):
    """
    Controller to crawl the site and follow all links with hrefs starting from / 
    """
    crawled     = []
    count       = 0
    error_count = 0
    
    def setUp(self):
        if not config['test.crawl_links']:
            raise SkipTest('Crawl not enabled in config - crawl test skipped')
        # Ignore the following:
        # /members/civicboom as this does not exist unless we are looking at the live site!
        # None for blank hrefs (we use href='' quite a bit?!)
        # 'False' for invalid href (Why does this happen in /help/article, WTF?!)
        self.crawled     = ['/members/civicboom', '/doc/', '/doc', 'None', 'False']
        self.count       = 0
        self.error_count = 0

    def crawl(self, url, prev_url, **kwargs):
        self.crawled.append(url)
        print url, 'from', prev_url
        response = self.app.get(url, status='*', **kwargs)
        if response.status not in [200, 301, 302]:
            print '\tGot response', response.status
            print '\tWhen calling', url, 'referred to by', prev_url
            self.error_count += 1
            return
        self.count += 1
        soup = BeautifulSoup(response.body)
        hrefs = [ link.get('href') for link in soup.findAll('a') if link.get('href') and not re.match(not_civicboom, link.get('href', ''))]
        hrefs.extend([ link.get('data-frag') for link in soup.findAll('a') if link.get('data-frag') and not re.match(not_civicboom, link.get('href', ''))])
        hrefs = set(hrefs)
        ## Iframe srcs? widget. and m. links
        for href in hrefs:
            if href and href not in self.crawled:
                self.crawl(href, url)
        if not prev_url:
            print 'Crawled', self.count
            if self.error_count:
                assert False, 'An error occured whilst crawling, see printed log'

    #---------------------------------------------------------------------------
    # Tests
    #---------------------------------------------------------------------------
    
    def test_crawl_web(self):
        self.crawl('/', None)       # Crawl when not logged in
        self.log_in_as('unittest')
        self.count = 0              # Reset counter
        self.crawl('/', None)       # Crawl when logged in
        
    def test_crawl_sub_domains(self):
        for sub_domain in ['m']:
            self.count = 0
            self.crawl('/', None, extra_environ={'HTTP_HOST': '%s.civicboom_test.com' % sub_domain})
            self.log_in_as('unittest')
            self.count = 0
            self.crawl('/', None, extra_environ={'HTTP_HOST': '%s.civicboom_test.com' % sub_domain})

    # AllanC - annoyingly crawls the whole site again ... these are covered by the test_widget file anyway.
    #def test_crawl_widget(self):
    #    self.crawl(url('member_action', id='unittest', action='content_and_boomed', w_theme='basic'   ), None, extra_environ={'HTTP_HOST': 'widget.civicboom_test.com'})
    #    count = 0
    #    self.crawl(url('member_action', id='unittest', action='content_and_boomed', w_theme='gradient'), None, extra_environ={'HTTP_HOST': 'widget.civicboom_test.com'})
