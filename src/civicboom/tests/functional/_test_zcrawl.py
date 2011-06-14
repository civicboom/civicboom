from civicboom.tests import *
from BeautifulSoup import BeautifulSoup

# This regexp will match any url starting with http(s):// not within civicboom.com or just # or mailto:*
not_civicboom = re.compile(r'((http(s{0,1})://(?!(www\.){0,1}civicboom\.com))|#|mailto\:.*).*')


class TestCrawlSite(TestController):
    """
    Controller to crawl the site and follow all links with hrefs starting from / 
    """
    # Ignore the following:
    # /members/civicboom as this does not exist unless we are looking at the live site!
    # None for blank hrefs (we use href='' quite a bit?!)
    # 'False' for invalid href (Why does this happen in /help/article, WTF?!)
    crawled = ['/members/civicboom', None, 'False']
    count = 0
    
    def setUp(self):
        pass
    
    def test_crawl(self):
        self.crawl('/', None)       # Crawl when not logged in
        self.log_in_as('unittest')
        self.count = 0              # Reset counter
        self.crawl('/', None)       # Crawl when logged in
        
    def crawl(self, url, prev_url):
        self.crawled.append(url)
        print url, 'from', prev_url
        response = self.app.get(url, status='*')
        if response.status not in [200, 301, 302]:
            print 'Got response', response.status
            print response.body
            print 'When calling', url, 'referred to by', prev_url
            assert False
        self.count += 1
        soup = BeautifulSoup(response.body)
        hrefs = [ link.get('href') for link in soup.findAll('a') if not re.match(not_civicboom, link.get('href', ''))]
        for href in hrefs:
            if href not in self.crawled:
                self.crawl(href, url)
        if not prev_url:
            print 'Crawled', self.count
