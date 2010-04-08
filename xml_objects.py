from elementtree.ElementTree import *
import urllib
import string

class URL(object):
    """Gnip URL container class.
    
    value:    string representation of the URL
    meta_url: string representation of the meta_url
    
    """

    def __init__(self, value=None, meta_url=None):
        self.value = value
        self.meta_url = meta_url

    def __str__(self):
        return "[" + str(self.value) + ", " + str(self.meta_url) + "]"

    def __cmp__(self, other):
        if isinstance(other, URL):
            ret = cmp(self.value, other.value)
            if ret == 0:
                ret = cmp(self.meta_url, other.meta_url)
        else:
            ret = 1
        return ret

class MediaURL(object):
    """Gnip Media URL container class.

    value:    string representation of the media URL
	height:   string the height
	width:   string the width 
	duration:   string the duration of the linked media
	type:   string the Gnip normalized type of the linked media
	mimeType: string the mimeType of the linked media
    """

    def __init__(self, value=None, height=None, width=None, duration=None, type=None, mimetype=None):
		self.value = value
		self.height = height
		self.width = width
		self.duration = duration
		self.type = type
		self.mimetype = mimetype

    def __str__(self):
        return "[" + str(self.value) + ", " \
				   + str(self.height) + ", "\
				   + str(self.width) + ", "\
				   + str(self.duration) + ", "\
				   + str(self.type) + ", "\
				   + str(self.mimetype) \
				+ "]"

    def __cmp__(self, other):
        if isinstance(other, MediaURL):
            ret = cmp(self.value, other.value)
            if ret == 0:
                ret = cmp(self.height, other.height)
                if ret == 0:
	                ret = cmp(self.width, other.width)
	                if ret == 0:
		                ret = cmp(self.duration, other.duration)
		                if ret == 0:
			                ret = cmp(self.type, other.type)
			                if ret == 0:
				                ret = cmp(self.mimetype, other.mimetype)
        else:
            ret = 1
        return ret

class Actor(object):
    """Gnip Actor container class
    
    value:     string representation of the Actor
    uid:       string representation of the uid
    meta_url:  string representation of the meta_url
    
    """

    def __init__(self, value=None, uid=None, meta_url=None):
        self.value = value
        self.uid = uid
        self.meta_url = meta_url

    def __str__(self):
        return "[" + str(self.value) + ", " + str(self.uid) + ", " + str(self.meta_url) + "]"

class Tag(object):
    """Gnip Tag container class
    
    value:     string representation of the Tag
    meta_url:  string representation of the meta_url
    
    """

    def __init__(self, value=None, meta_url=None):
        self.value = value
        self.meta_url = meta_url

    def __str__(self):
        return "[" + str(self.value) + ", " + str(self.meta_url) + "]"

    def __cmp__(self, other):
        if isinstance(other, Tag):
            ret = cmp(self.value, other.value)
            if ret == 0:
                ret = cmp(self.meta_url, other.meta_url)
        else:
            ret = 1
        return ret

class To(object):
    """Gnip To container class
    
    value:     string representation of the To
    meta_url:  string representation of the meta_url    
    
    """

    def __init__(self, value=None, meta_url=None):
        self.value = value
        self.meta_url = meta_url

    def __str__(self):
        return "[" + str(self.value) + ", " + str(self.meta_url) + "]"

    def __cmp__(self, other):
        if isinstance(other, To):
            ret = cmp(self.value, other.value)
            if ret == 0:
                ret = cmp(self.meta_url, other.meta_url)
        else:
            ret = 1
        return ret

class Point(object):
    """Gnip Point container class
    
    x:     float representation of the x coordinate
    y:     float representation of the y coordinate
    
    """

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def __cmp__(self, other):
        if isinstance(other, Point):
            if self.x < other.x:
                ret = -1
            elif self.x > other.x:
                ret = 1
            elif self.y < other.y:
                ret = -1
            elif self.y > other.y:
                ret = 1
            else:
                ret = 0
        else:
            ret = 1
        return ret

class Rule(object):
    """Gnip Rule container class
    
    type:    string representation of the rule type
    value:   string representation of the rule value
    
    """

    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value

    def to_delete_query_string(self):
        return urllib.urlencode([("type",self.type),("value",self.value)])

    def to_xml(self):
        rule_node = Element("rule")
        rule_node.text = self.value
        rule_node.set("type", self.type)
        return tostring(rule_node)

    def __str__(self):
        return "[" + str(self.type) + ", " + str(self.value) + "]"

    def __cmp__(self, other):
        if isinstance(other, Rule):
            ret = cmp(self.type, other.type)
            if ret is 0:
                ret = cmp(self.value, other.value)
        else:
            ret = 1
        return ret

class Result(object):
    """Gnip Result container class
    
    message:    string
    
    """

    def __init__(self, message=None):
        self.message = message

    def from_xml(self, xml):
        node = fromstring(xml)

        if node is not None:
            self.message = node.text
        else:
            self.message = ""

    def __cmp__(self, other):
        if isinstance(other, Result):
            ret = cmp(self.message, other.message)
        else:
            ret = 1
        return ret

class Error(object):
    """Gnip error container class
    
    message:    string
    
    """

    def __init__(self, message=None):
        self.message = message

    def from_xml(self, xml):
        node = fromstring(xml)

        if node is not None:
            self.message = node.text
        else:
            self.message = ""

    def __cmp__(self, other):
        if isinstance(other, Error):
            ret = cmp(self.message, other.message)
        else:
            ret = 1
        return ret