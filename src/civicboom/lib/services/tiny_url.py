import urllib

apiurl = "http://tinyurl.com/api-create.php?url="


def tiny_url(url): # pragma: no cover - testing shouldn't hit external servers
    """ Make a tinyurl for """
    try:
        return urllib.urlopen(apiurl + url).read()
    except:
        pass
    return None
