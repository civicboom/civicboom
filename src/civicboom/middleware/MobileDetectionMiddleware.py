# Middleware to set environ['is_mobile'] to true or false
# originaly taken from code for django at http://djangosnippets.org/snippets/2001/ and modifyed to pylons

import re


class MobileDetectionMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # TODO: middleware needs to be upgraded to look for subdomain m. in url
        is_mobile = False

        if 'HTTP_USER_AGENT' in environ:
            user_agent = environ['HTTP_USER_AGENT']

            # Test common mobile values.
            pattern = "(up.browser|up.link|mmp|symbian|smartphone|midp|wap|phone|windows ce|pda|mobile|mini|palm|netfront|webos)"
            prog    = re.compile(pattern, re.IGNORECASE)
            match   = prog.search(user_agent)

            if match:
                is_mobile = True
            else:
                # Nokia like test for WAP browsers.
                # http://www.developershome.com/wap/xhtmlmp/xhtml_mp_tutorial.asp?page=mimeTypesFileExtension
                if 'HTTP_ACCEPT' in environ:
                    http_accept = environ['HTTP_ACCEPT']

                    pattern = "application/vnd\.wap\.xhtml\+xml"
                    prog    = re.compile(pattern, re.IGNORECASE)
                    match   = prog.search(http_accept)

                    if match:
                        is_mobile = True

            if not is_mobile:
                # Now we test the user_agent from a big list.
                user_agents_test = (
                            "w3c ", "acs-", "alav", "alca", "amoi", "audi",
                            "avan", "benq", "bird", "blac", "blaz", "brew",
                            "cell", "cldc", "cmd-", "dang", "doco", "eric",
                            "hipt", "inno", "ipaq", "java", "jigs", "kddi",
                            "keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
                            "maui", "maxo", "midp", "mits", "mmef", "mobi",
                            "mot-", "moto", "mwbp", "nec-", "newt", "noki",
                            "xda",  "palm", "pana", "pant", "phil", "play",
                            "port", "prox", "qwap", "sage", "sams", "sany",
                            "sch-", "sec-", "send", "seri", "sgh-", "shar",
                            "sie-", "siem", "smal", "smar", "sony", "sph-",
                            "symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
                            "upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
                            "wapi", "wapp", "wapr", "webc", "winw", "winw",
                            "xda-",)

                test = user_agent[0:4].lower() #Takes first 4 characters from the user agent and converts to lower case
                if test in user_agents_test:
                    is_mobile = True
        
        if is_mobile:
            environ['is_mobile'] = str(is_mobile)
        else:
            environ['is_mobile'] = None
        
        return self.app(environ, start_response)
