import urllib

apiurl = "http://tinyurl.com/api-create.php?url="


def tiny_url(url):
    """ Make a tinyurl for """
    try:
        return urllib.urlopen(apiurl + url).read()
    except:
        pass
    return None
