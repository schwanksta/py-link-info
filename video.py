"""
Take a YouTube or Vimeo URL and extract the ID, title, description and a thumbnail.
"""

import urllib2, simplejson, re
from xml.dom import minidom

#Regex should match any valid Vimeo video's URL
VIMEO_URL = re.compile("(http://)?(www\.)?vimeo.com/(\d+)/?")   
#Regex should match any valid YouTube video' URL
YOUTUBE_URL = re.compile("(http://)?(www\.)?youtube.com/watch\?v=([-a-zA-Z0-9]+)")    


def get_single_node_value(node):
    """
    Takes the result of minidom.getElementsByTagName and returns the value of the first node.
    """
    return node.pop().childNodes[0].nodeValue


class Video():

    def __init__(self):
        pass        

class YouTube(Video):

    def __init__(self, url, save_location=""):
        self.url = url
        self.id = self.snip_id()
        self.title, self.description, self.thumb_url = self.load_data()


    def snip_id(self):
        """
        Returns a YouTube video ID from a video's URL
        """
        match = YOUTUBE_URL.search(self.url)

        return match.groups()[-1]


    def load_data(self):
        """
        Queries YouTube's API for information on a single video. Returns the title and description.
        """

        data_url = "http://gdata.youtube.com/feeds/api/videos/%s" % (self.id)

        feed = urllib2.urlopen(data_url)
        
        doc = minidom.parse(feed)

        title = get_single_node_value(doc.getElementsByTagName("title"))
        description = get_single_node_value(doc.getElementsByTagName("content"))
        thumb_url = "http://img.youtube.com/vi/%s/default.jpg" % (self.id)

        return title, description, thumb_url
        

    
    def process_thumb(self, save_location):
       pass 


class Vimeo(Video):

    def __init__(self, url, save_location=""):
        self.url = url
        self.id = self.snip_id()
        self.title, self.description, self.thumb_url = self.load_data()

    
    def snip_id(self):
        """
        Returns a Vimeo video ID from a video's URL
        """
        match = VIMEO_URL.search(self.url)

        return match.groups()[-1]


    def load_data(self):
        """
        Takes a Vimeo video ID and returns the video's title, description and thumbnail's file name -- in that order
        """

        thumb_url = "http://vimeo.com/api/clip/%s/json" % (self.id)

        try:
            result = simplejson.load(urllib2.urlopen(thumb_url))
        except Exception:
            print result['Error']
        return result[0]['title'], result[0]['caption'], result[0]['thumbnail_large'] #finish me
        
