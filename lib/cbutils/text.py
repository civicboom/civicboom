"""
A collection of text processing tools for Text, HTML and JSON
"""

import re
import xml.sax.saxutils as saxutils
import unicodedata

#-------------------------------------------------------------------------------

def split_word(text, max_chars):
    """
    used to split long usernames with spaces, seeks capitals as a preference to split with

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

html_tags_allowed = (r'h1',r'h2',r'h3',r'h4','h5',r'/h1',r'/h2',r'/h3',r'/h4','/h5',r'br',r'br/',r'ul',r'/ul',r'ol',r'/ol',r'li',r'/li',r'/a',r'strong',r'/strong',r'em',r'/em',r'p',r'/p')


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
    
    >>> clean_html_markup(u'<h1>Test</h1><p>Test</p>')
    u'<h1>Test</h1><p>Test</p>'
    >>> clean_html_markup(u'<h1>Test</h1><P style="no">clean</P><br/><a href="#" onclick="h4ckzors">me</a>')
    u'<h1>Test</h1><p>clean</p><br/><a href="#">me</a>'

    """
    text = re.sub(r'<style(.*?)style>', " ", text) #Strip STYLE (under no circumstances do we want this)
    text = re.sub("&nbsp;"," ",text)               #Replace escaped spaces
    #text = re.sub("&amp;","&",text)
    text = re.sub("&lt;","-lt-",text) #convert legitmate lt gt's so that they can be untouched and reinserted later
    text = re.sub("&gt;","-gt-",text)
    text = re.sub(r'&(\w{1,6}?);', r'-amp-\1;', text)
    
    text = saxutils.escape(text) #webhelpers.html.converters.format_paragraphs(text)

    def process_tag(m):
        tag_contents = m.group(1)
        tag_type     = tag_contents.split(" ")[0].lower()
        if tag_type in html_tags_allowed:
            return "<%s>" % tag_type
        if tag_contents.startswith("a "):
            url = ""
            url_find = re.search(r'href="(.*?)"', tag_contents) # Question, why have the " not been escaped to &quot; ? I dont like this saxutils should have escaped them
            if url_find:
                url = url_find.group(1)
            return r'<a href="' + saxutils.unescape(url) + r'">'
        return '' #&lt;%s&gt;' % tag_contents
    p = re.compile(r'&lt;(.*?)&gt;',re.DOTALL)
    text = p.sub(process_tag, text)
    
    text = re.sub("-lt-","&lt;",text) #Add back the legitmate escapes for gt and lt
    text = re.sub("-gt-","&gt;",text)
    text = re.sub(r'-amp-(\w{1,6}?);', r'&\1;', text)
    text = re.sub("<br>","<br/>",text) #replace all line breaks with XHTML complient tags
    return text


def clean_html(text):
    from lxml.html.clean import Cleaner
    return Cleaner(links=False, style=True).clean_html(text)

#-------------------------------------------------------------------------------


def scan_for_embedable_view_and_autolink(text, remove=False, protocol='http'): #, size=(300,225)
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
            #text = re.sub(regex_youtube  , '<object width="%(width)s" height="%(height)s"><param name="wmode" value="transparent"></param><param name="movie" value="%(protocol)s://www.youtube.com/v/\\1"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="%(protocol)s://www.youtube.com/v/\\1" type="application/x-shockwave-flash" wmode="transparent" allowscriptaccess="always" allowfullscreen="true" width="%(width)s" height="%(height)s"></embed></object>\\2' % dict(width=size[0], height=size[1], protocol=protocol), text)
            text = re.sub(regex_youtube   , '<iframe class="video_embed" src="%(protocol)s://www.youtube.com/embed/\\1" frameborder="0" allowfullscreen></iframe>' % dict(protocol=protocol), text)
            # Google video embed removed as we have removed our pixel sizes from the config
            #text = re.sub(regex_googlevid , '<embed id=VideoPlayback src=%(protocol)s://video.google.com/googleplayer.swf?docid=\\1&fs=true style=width:%(width)spx;height:%(height)spx wmode="transparent" allowFullScreen=true allowScriptAccess=always type=application/x-shockwave-flash></embed>\\2' % dict(width=size[0], height=size[1], protocol=protocol) , text)
    except:
        pass
    return text

#-------------------------------------------------------------------------------


def strip_html_tags(text):
    """
    Removes anything between html tags <>
    Needs updating to match > or end of string, in case a tag was not closed
    
    >>> strip_html_tags(u'<h1>Test</h1>')
    u'Test'
    >>> strip_html_tags(u'<h1>Test</h1>\\n<p style="no">clean</p>\\n\\n<br/><a href="#">me</a>')
    u'Test \\n clean \\n\\n me'
    """
    #import webhelpers.markdown.HtmlBlockPreprocessor - using proper modules to do this would be good, couldnt work out how to use this HTML processor
    #text = webhelpers.html.converters.markdown(text)
    ##return re.sub(r'&lt;(.*?)&gt;', " ", saxutils.escape(text))
    text = re.sub(r'<(.*?)>', ' ', text)
    text = re.sub(r'[ \t]+' , ' ', text)
    return text.strip()
    
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
    
    text = content_html
    text_body = re.sub(r'(?is)<body>(.*)</body>',r'\1',text)  #Extact the body if text if it is a full HTML doc
    if text_body:
        text = text_body
    text = re.sub(r'(?is)<style.*</style>',r'',text)       # The style tag has contents that are not human readable, dispose of contents and not just the tag
    text = re.sub(r'(?i)<br>|<br/>|</p>|</li>',r'\n',text) # Replace any ends of sections with new lines
    text = re.sub(r'(?i)<li>',r' - ',text)                 # List items should have starters (enchancement? numbers for ol?)
    text = re.sub(r'(?i)\&nbsp\;', r' ', text)             # Replace html entities with plaintext equivalent
    text = re.sub(r'(?i)\&lt\;', r'<', text)
    text = re.sub(r'(?i)\&gt\;', r'>', text)
    text = re.sub(r'(?i)\&amp\;', r'&', text)              # Ensure &amp; is the last replacement to ensure &amp;lt; is replaced with &lt; and not <

    def heading_replace(m):
        # improvement idea: use str.center(width[, fillchar]) Return centered in a string of length width. Padding is done using the specified fillchar (default is a space).
        heading_level = m.group(2)
        heading_decoration = ""
        for i in range(5-int(heading_level)):
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
    return text


#-------------------------------------------------------------------------------

def get_html_links(text):
    return re.findall(r'<a href=(.*?)>', text)

#-------------------------------------------------------------------------------


def safe_python_strings(d):
    """
    Recursively steps though a python dictionary
    Identifies strings and removes/replaces harmful/unwanted characters + collapses white space
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


#-------------------------------------------------------------------------------
explicit_replacement  = '[Explicit]'
part_explicits = set([
    'cunt',
    'fuck',
    'fcuk',
    'shit',
])
whole_explicits = set([
    'piss',
    'slut',
    'whore',
    'slag',
    'cock',
    'cocksucker',
    'cocklover',
    'cockfag',
    'cockbite',
    'dick',
    'dickhead',
    'bollocks',
    'bollox',
    'wank',
    'wanker',
    'ass',
    'asswipe',
    'faggot',
    'niger',
    'nigger',
    'tard',
    'hardon',
    'bastard',
    'dildo',
    'penis',
    'asshole',
    'cum',
    'cumshot',
    'twat',
    'turd',
    'boobs',
    'fudgepacker',
    'spic',
    'wog',
    'beaner',
    'asshole',
    'wang',
    'schlong',
    'boner',
    'douche',
    'prick',
    'retard',
    'tits',
    'tit',
    'rape',
    'porn',
    'blowjob',
    'rimjob',
    'handjob',
    'bitch',
    'knob',
    'chink',
    'nutsack',
    'ballsack',
    'dickweed',
    'pubes',
    'pubic',
    'foreskin',
    'vagina',
    'testicles',
    'testicle',
    'dong',
    'pecker',
    'gaywad',
    'gaylord',
    'poontang',
    'skeet',
    'tosser',
    'lesbo',
    'jizz',
    'junglebunny',
    'gay',
    'fag',
    'tranny',
    'firing',
    'humping',
    'queer',
    'queef',
    'spac',
    'spactard',
    'kunt',
    'wankstain',
    'polesmoker',
    'deepthroat',
    'anal',
    'cooch',
    'clit',
    'coon',
    'fellatio',
    'cunnilingus',
])

def profanity_check(text):
    """
    Simple profanity check

    normalizes uniode characters and performs common l33t number replacements
    only checks for whole words
    
    >>> profanity_check(u'hello! how was your day?')['CleanText']
    u'hello! how was your day?'
    >>> profanity_check(u'hello! fuckballz')['CleanText']
    u'hello! [Explicit]'
    >>> profanity_check(u'hello! penis boy')['CleanText']
    u'hello! [Explicit] boy'
    >>> profanity_check(u'hello! f@g.g0t')['CleanText']
    u'hello! [Explicit]'
    >>> profanity_check(u'hello! <p>cock</p>')['CleanText']
    u'hello! <p>[Explicit]</p>'
    >>> profanity_check(u'hello! gay!!!! yeah!')['CleanText']
    u'hello! [Explicit] yeah!'
    """
    if isinstance(text,str):
        text = unicode(text)
    
    profanity_response = {
        'FoundProfanity' : False,
        'ProfanityCount' : 0,
        'CleanText'      : text,
    }
    
    def contains_part_explicit(word):
        for explicit in part_explicits:
            if explicit in word:
                return True
        return False
    
    def replace_part_explicit(word):
        for part_explicit in part_explicits:
            if part_explicit in word:
                return word.replace(part_explicit, explicit)
        return word
    
    def inc_profanity():
        profanity_response['FoundProfanity']  = True
        profanity_response['ProfanityCount'] += 1
    
    text_words = text.replace('<', ' -lt- ').replace('>', ' -gt- ').split(' ') # escape all html tags and split by spaces
    
    for i in range(len(text_words)):
        word_normalized = unicodedata.normalize('NFKD', text_words[i].lower()).encode('ascii','ignore')
        word_normalized = word_normalized  \
                         .replace('@','a') \
                         .replace('0','o') \
                         .replace('1','l') \
                         .replace('3','e') \
                         .replace('4','a') \
                         .replace('5','s') \
                         .replace('9','g')
        word_normalized = re.sub('\W','', word_normalized)
        if word_normalized in whole_explicits or contains_part_explicit(word_normalized):
            text_words[i] = explicit_replacement
            inc_profanity()
        #else:
            #word_normalized_replaced = replace_part_explicit(word_normalized)
            #if word_normalized_replaced != word_normalized:
            #    text_words[i] = word_normalized_replaced
            #    inc_profanity()
    
    if profanity_response['FoundProfanity']:
        profanity_response['CleanText'] = ' '.join(text_words).replace(' -lt- ', '<').replace(' -gt- ', '>') # unescape the '<' '>' back
    
    return profanity_response

def get_diff_words(a,b):
    """
    Used for comparing profanity checked text and rereving the words that at differnt
    
    Reference - http://docs.python.org/library/difflib.html#difflib.context_diff
    
    AllanC - TODO. it is possible that because the output from context_diff is a string, it is possible for a malitious user to insert the string '----\n' to abort the process
    
    >>> get_diff_words('The monkey jumped over the moon', 'The badger jumped over the donkey')
    ['monkey', 'moon']
    >>> t = u'This content is FUCKING disgusting'
    >>> get_diff_words(t, profanity_check(t)['CleanText'])
    [u'FUCKING']
    """
    if isinstance(a, basestring): a = a.split(' ')
    if isinstance(b, basestring): b = b.split(' ')
    # Old Difflib way - lame - why did I not use sets in the first place? Thanks Shish
    #words = []
    #for word in difflib.context_diff(a,b):
    #    if word.endswith('----\n'):
    #        break
    #    if word.startswith('! '):
    #        words.append(word[2:])
    #return words
    return list(set(a)-set(b))
