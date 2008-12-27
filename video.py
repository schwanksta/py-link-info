"""
Take a YouTube or Vimeo URL and extract the ID, title, description and a thumbnail.
"""

import urllib2, simplejson, re, md5, cStringIO, urllib2
from xml.dom import minidom
from os import path
from PIL import Image
#import thumbs

#Regex should match any valid Vimeo video's URL
VIMEO_URL = re.compile("(http://)?(www\.)?vimeo.com/(\d+)")   

#Regex should match any valid YouTube video's URL
YOUTUBE_URL = re.compile("(http://)?(www\.)?youtube.com/watch\?v=([-_a-zA-Z0-9]+)")    

def get_single_node_value(node):
    """
    Takes the result of minidom.getElementsByTagName and returns the value of the first node.
    """
    return node.pop().childNodes[0].nodeValue


class Video():

    def __init__(self, url, title, description, thumb_url, id):
        self.url =  url
        self.title = title
        self.description = description
        self.thumb_url = thumb_url
        self.id = id

    def json(self):
        """
        Returns a JSON representation of the object
        """

        d = dict(title=self.title, description=self.description, thumb_url=self.thumb_url, id=self.id)

        return simplejson.JSONEncoder().encode(d)


    def stamp_thumb(self, save_location, playbutton, media_root=""):
        """
        Takes a location and saves the video thumbnail there with a play button over it. 
        File name is an MD5 has of self.thumb_url, and self.thumb_url is changed to the local name.
        If the file already exists, the function silently changes self.thumb_url to it 
        and does not try to add a button. 
        """

        if save_location[-1] != "/":
            save_location += "/" 

        if media_root == "":
            media_root = save_location
        else:
            if media_root[-1] != "/":
                media_root += "/"

        hashname = md5.new(self.thumb_url).hexdigest()

        filename = save_location + hashname + ".jpg"

        if path.exists(filename):
            self.thumb_url = media_root + hashname + ".jpg"
            return 1

        th = urllib2.urlopen(self.thumb_url)
        thumb = cStringIO.StringIO(th.read()) # Constructs a StringIO object holding the thumbnail

        background = Image.open(thumb) #now thumb implements seek(), etc.
        button = Image.open(playbutton)
        width, height = button.size
        background = background.resize((width, height), Image.ANTIALIAS)
        
        # get the alpha-channel (used for non-replacement)
        background = background.convert("RGBA")
        r,g,b,a = button.split()
        
        # paste the frame button without replacing the alpha button of the button image
        background.paste(button, mask=a)
        background.save(filename)
        
        self.thumb_url = media_root + hashname + ".jpg"

        return 0



class YouTube(Video):

    def __init__(self, url, save_location=""):
        self.url = url
        self.id = self.snip_id()
        self.title, self.description, self.thumb_url = self.load_data()

        if save_location != "":
            self.stamp_video(save_location)


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
        return result[0]['title'], result[0]['caption'], result[0]['thumbnail_large'] 
