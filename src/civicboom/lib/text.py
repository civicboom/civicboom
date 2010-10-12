"""
A collection of text processing tools for Text, HTML and JSON
"""

import re
import xml.sax.saxutils as saxutils


#-------------------------------------------------------------------------------

def split_word(text, max_chars):
    """
    used to split long usernames with spaces, seeks capitals as a prefernce to split with

    >>> split_word("IAmAWaffleFiend", 6)
    'IAmA Waffle Fiend'

    >>> split_word("abcde12345abcde12345", 5)
    'abcde 12345 abcde 12345'

    >>> split_word("abc de12345", 5)
    'abc de123 45'

    >>> split_word("abc de12345", 0)
    'abc de12345'

    >>> split_word("Mr.Longname", 8)
    'Mr. Longname'
    """
    if max_chars <= 0:
        return text

    new_text = ''
    current_count = 0
    for i in range(len(text)):
        if (text[i].isspace()):
            current_count = 0
        elif current_count >= max_chars:
            for n in range(1, current_count):
                if new_text[-n].isupper():
                    new_text = new_text[0:-n] + " " + new_text[-n:]
                    current_count = n
                    break
            else:
                new_text += ' '
                current_count = 1
        else:
            current_count += 1
        new_text += text[i]

    return new_text

#-------------------------------------------------------------------------------

# AllanC - Is this needed now we have internationalisation?
def format_multiple_prefix(number, **kargs):
    """
    prefix a name with a number
    e.g.
      23 monkeys
       1 monkey
      No monkeys
    """
    text = format_multiple(number,**kargs)
    if number > 0:
        text = "%s %s" % (number, text)
    return text


def format_multiple(number,nothing="",single="",multiple=None,multiple_addition="s"):
    """
    Used to put 's at end of words if there is more than one of them
    """
    if number == 0:
        return nothing;
    if number == 1:
        return single;
    if number > 1:
        if multiple == None and single!="":
            return single+multiple_addition
        if multiple != None:
            return multiple
    return ""


#-------------------------------------------------------------------------------

html_tags_allowed = (r'br',r'br/',r'ul',r'/ul',r'ol',r'/ol',r'li',r'/li',r'/a',r'strong',r'/strong',r'em',r'/em',r'p',r'/p')

def clean_html_markup(text):
    """
    1.) Takes the content text that may have markup for <strong>,<a>,<li>,<ul> etc.
    2.) Escapes all markup (in case it is harmful)
    3.) re-instantiate the needed tags carefuly

    Todo: ? could enforce start and end tags so that people cant just inset a </ul> without a <ul> before it

    When text comes to us from the rich text component, some characters already come escaped
     e.g &nbsp;   when this is escaped again it becaomes &amp;nbsp;
    we need to perform an saxutils.escape to remove malicious markup that has not been though our site and posted directly.
    so the purpose of this here is to convert these characters created by the rich text, knowing that they will be escaped next line
    This levels the playing field, malicious &lt &gt are converted to < > and escaped in the same way
    """
    
    text = re.sub(r'<style(.*?)style>', " ", text) #Strip STYLE (under no circumstances do we want this)
    text = re.sub("&nbsp;"," ",text)               #Replace escaped spaces
    #text = re.sub("&amp;","&",text)
    text = re.sub("&lt;","-lt-",text) #convert legitmate lt gt's so that they can be untouched and reinserted later
    text = re.sub("&gt;","-gt-",text)
    
    text = saxutils.escape(text) #webhelpers.html.converters.format_paragraphs(text)
    def process_tag(m):
        tag_contents = m.group(1)
        tag_type     = tag_contents.split(" ")[0]
        if tag_type in html_tags_allowed: return "<%s>" % tag_type
        if tag_contents.startswith("a"):
            url = ""
            url_find = re.search(r'href="(.*)"', tag_contents) # Question, why have the " not been escaped to &quot; ? I dont like this saxutils should have escaped them
            if url_find: url = url_find.group(1)
            return r'<a href="' + saxutils.unescape(url) + r'">'
        return '' #&lt;%s&gt;' % tag_contents
    p = re.compile(r'&lt;(.*?)&gt;',re.DOTALL)
    text = p.sub(process_tag, text)
    
    text = re.sub("-lt-","&lt;",text) #Add back the legitmate escapes for gt and lt
    text = re.sub("-gt-","&gt;",text)
    text = re.sub("<br>","<br/>",text) #replace all line breaks with XHTML complient tags
    return text


from lxml.html.clean import Cleaner
def clean_html(text):
    return Cleaner(links=False, style=True).clean_html(text)

#-------------------------------------------------------------------------------

def scan_for_embedable_view_and_autolink(text, remove=False):
    """
    Scan trhough content text looking for video URL's
    Replace them with embed tags
    
    Enhancement:
      Use the youtube API to get the privew image from the server
      EXAMPLE: http://img.youtube.com/vi/FAKidwlx_w8/0.jpg
    """
    regex_youtube   = r'http://www.youtube.com/watch\?v=(.*?)([&#<>\n "])'
    regex_googlevid = r'http://video.google.com/videoplay\?docid=(.*?)([&#<>\n "])'
    try:
        if remove==True:
            text = re.sub(regex_youtube  , '', text)
            text = re.sub(regex_googlevid, '', text)
        else:
            text = re.sub(regex_youtube  , r'<object width="500" height="308"><param name="movie" value="http://www.youtube.com/v/\1"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/\1" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="500" height="308"></embed></object>\2', text)
            text = re.sub(regex_googlevid, r'<embed id=VideoPlayback src=http://video.google.com/googleplayer.swf?docid=\1&fs=true style=width:400px;height:326px allowFullScreen=true allowScriptAccess=always type=application/x-shockwave-flash></embed>\2', text)
    except:
        pass
    return text

#-------------------------------------------------------------------------------

def strip_html_tags(text):
    """
    Removes anything between html tags <>
    Needs updating to match > or end of string, in case a tag was not closed
    """
    #import webhelpers.markdown.HtmlBlockPreprocessor - using proper modules to do this would be good, couldnt work out how to use this HTML processor
    #text = webhelpers.html.converters.markdown(text)
    ##return re.sub(r'&lt;(.*?)&gt;', " ", saxutils.escape(text))
    return re.sub(r'<(.*?)>', " ", text)
    
#-------------------------------------------------------------------------------
   
def convert_html_to_plain_text(content_html, ommit_links=False):
    """
    Convert and HTML document into a plain text equivelent
      -inspecting known html tags and replacing them with text equivelents
        -remove the head
        -<br> or </p> to /n
        -h? to -???-
        -a to full address
        -li to ' - '
    """
    
    #print "CONTENT IN: %s" % content_html
    text = content_html  
    text_body = re.sub(r'(?is)<body>(.*)</body>',r'\1',text)  #Extact the body if text if it is a full HTML doc
    if text_body:
        text = text_body
    text = re.sub(r'(?is)<style.*</style>',r'',text)       # The style tag has contents that are not human readable, dispose of contents and not just the tag
    text = re.sub(r'(?i)<br>|<br/>|</p>|</li>',r'\n',text) # Replace any ends of sections with new lines
    text = re.sub(r'(?i)<li>',r' - ',text)                 # List items should have starters (enchancement? numbers for ol?)
    def heading_replace(m):
        # improvement idea: use str.center(width[, fillchar]) Return centered in a string of length width. Padding is done using the specified fillchar (default is a space).
        heading_level = m.group(2)
        heading_decoration = ""
        for i in range(int(heading_level)):
          heading_decoration += "="
        newline_before = ""
        newline_after  = ""
        if m.group(1)!='':
          newline_after = '\n'
        else:
          newline_before = '\n'
        return newline_before+" "+heading_decoration+" "+newline_after
    text = re.sub(r'(?i)<(/?)h([1-9])>',heading_replace,text)  #Replace headdings with ==Heading==
    link_replacement_pattern = r'\2 (\1)'
    if ommit_links:  # Sometimes when we convert to plain text we dont want verbose http://site in it because we want it to be a concise and possible
        link_replacement_pattern = r'\2'
    text = re.sub(r'(?is)<a.*?href=[\'"](.*?)[\'"].*?>(.*?)</a>', link_replacement_pattern, text)
    text = strip_html_tags(text)            # Remove all left over HTML tags
    text = re.sub(r' +' ,r' ' ,text)        # Concatinate multiple spaces into a single space
    text = re.sub(r'[\r\f\a\v]',r'\n',text) # Convert all known new lines characters into a single type
    text = re.sub(r'\n \n',r'\n',text)      # This is the pain in the ass, spaces locked inbetween new lines ... rrrrr
    text = re.sub(r'\n+',r'\n',text)        # Replace multiple occourences of new lines with a single one
    #print "CONTENT OUT: %s" % text
    return text


#-------------------------------------------------------------------------------

def get_html_links(text):
    return re.findall(r'<a href=(.*?)>', text)

#-------------------------------------------------------------------------------

def safe_python_strings(d):
    """
    Recursivly steps though a python dictionary
    Identifys strings and removes/replaces harmful/unwanted characters + collapses white space
    """
    if isinstance(d, basestring):
        d = re.sub("'"   , "`", d)
        d = re.sub("\n"  , " ", d)
        d = re.sub(r"\s+", " ", d)
        d = d.strip()
    elif hasattr(d, 'keys'):
        for key in d.keys():
            d[key] = safe_python_strings(d[key])
    return d
