import xml_objects
import base64
import StringIO
import gzip
from elementtree.ElementTree import *

class Payload(object):
    """Gnip Payload container class
    
    A Payload represents the payload information in a Gnip Activity.
    """

    def __init__(self, title=None, body=None, media_urls=None, raw=None):
        """Initialize the class.

        @type title string
        @param title Activity title
        @type body string
        @param body Activity body
        @type media_urls List of URLs
        @param media_urls MediaURLs associated with the activity
        @type raw raw data of a payload that will be compressed and encoded
        @param raw Raw text of activity

        """

        self.title = title
        self.body = body
        self.media_urls = media_urls
        self.write_raw(raw)

    def read_raw(self):
        """Return the decoded and uncompressed raw value from a payload
        
        @return string
        """
        if self.__raw is None:
            return None
        else:
            return self.__decompress_with_gzip(self.__decode(self.__raw))

    def write_raw(self, raw):
        """Set the raw for the payload.
        
           @type raw string
           @param raw string will be compressed and encoded.
        """
        if raw is None:
            self.__raw = None
        else:
            self.__raw = self.__encode(self.__compress_with_gzip(raw))

    def from_xml_node(self, payload_xml_node):
        """ Populates payload from a payload xml node
        
        @type payload_xml_node Element
        @param payload_xml_node an Element representing the Payload for an Activity.
        """

        if payload_xml_node is not None:

            title_node = payload_xml_node.find("title")
            if title_node is not None:
                self.title = title_node.text
            else:
                self.title = None

            body_node = payload_xml_node.find("body")
            if body_node is not None:
                self.body = body_node.text
            else:
                self.body = None

            media_url_nodes = payload_xml_node.findall("mediaURL")
            if media_url_nodes is not None:
                self.media_urls = []
                for media_url_node in media_url_nodes:
                    media_url = xml_objects.MediaURL(value=media_url_node.text, 
                                                     height=media_url_node.get("height"),
                                                     width=media_url_node.get("width"),
                                                     duration=media_url_node.get("duration"),
                                                     type=media_url_node.get("type"),
                                                     mimetype=media_url_node.get("mimeType")
                                                     )
                    self.media_urls.append(media_url)
            else:
                self.media_urls = None

            raw_node = payload_xml_node.find("raw")
            self.__raw = raw_node.text

    def to_xml_node(self):
        """ Return a XML representation of this object

        @return string containing XML representation of the Payload

        Returns a XML representation of this object.

        """

        payload_node = Element("payload")

        if self.title is not None:
            title_node = Element("title")
            title_node.text = self.title
            payload_node.append(title_node)

        if self.body is not None:
            body_node = Element("body")
            body_node.text = self.body
            payload_node.append(body_node)

        if self.media_urls is not None and len(self.media_urls) > 0:
            for media_url in self.media_urls:
                media_url_node = Element("mediaURL")
                media_url_node.text = media_url.value
                if media_url.height is not None:
                    media_url_node.set("height", media_url.height)
                if media_url.width is not None:
                    media_url_node.set("width", media_url.width)
                if media_url.duration is not None:
                    media_url_node.set("duration", media_url.duration)
                if media_url.type is not None:
                    media_url_node.set("type", media_url.type)
                if media_url.mimetype is not None:
                    media_url_node.set("mimeType", media_url.mimetype)
                payload_node.append(media_url_node)

        if self.__raw is not None:
            raw_node = Element("raw")
            raw_node.text = self.__raw
            payload_node.append(raw_node)

        return payload_node

    def __encode(self, string):
        return base64.b64encode(string)

    def __decode(self, string):
        return base64.b64decode(string)

    def __compress_with_gzip(self, string):
        zbuf = StringIO.StringIO()
        zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=9)
        zfile.write(string)
        zfile.close()
        return zbuf.getvalue()

    def __decompress_with_gzip(self, compresseddata):
        zbuf = StringIO.StringIO(compresseddata)
        zfile = gzip.GzipFile(fileobj=zbuf)
        return zfile.read()
        
    def __str__(self):
        return "[" + str(self.title) + \
            ", " + str(self.body) + \
            ", " + str(self.media_urls) + \
            ", " + str(self.read_raw()) + \
            "]"
