from restful_lib import Connection, ConnectionError
from microblog_exceptions import MicroBlogMsgLimitExceeded

from xml.etree import ElementTree as ET

class FailWhale(Exception):
    def __str__(self):
        return "Oh noes, the failwhale cometh!"

TWITTER_ENDPOINT = "http://twitter.com"

class Twitter(object):
    def __init__(self, username,password):
        self._conn = Connection(TWITTER_ENDPOINT, username, password)

    def post(self, message, clip_length=False):
        if isinstance(message, list):
            # Default to a joining up the list of words with a space
            message = " ".join(message)

        if len(message)>140:
            if clip_length:
                message = message[:140]
            else:
                raise MicroBlogMsgLimitExceeded

        resp = self._conn.request_post("/statuses/update.json", args={"status":message})

        if resp.get('headers').get('status') not in ["200", 200, "204", 204]:
            print resp
            raise FailWhale

    def listfriends(self):
        class Friend(object):
            def __init__(self):
                self.name = ""
            def __setattr__(self, name, value):
                object.__setattr__(name,value)
            def __str__(self):
                return self.name

        class Friends(object):
            def __init__(self, connection):
                self.c = connection
                self.xml_dom = []
                self.page=0
            def __iter__(self):
                if not self.xml_dom:
                    self.get_next_batch()
                while(len(self.xml_dom)>0):
                    for friend in self.xml_dom.getchildren():
                        f = Friend()
                        for item in friend.getchildren():
                            f.__setattr__(item.tag, item.text)
                        yield f
            def get_next_batch(self):
                self.page = self.page+1
                resp = self.c.request_get("statuses/friends.xml", args={"lite":"true", "page":self.page})
                status = resp.get('headers').get('status')
                if status in [200, "200"]:
                    # TODO catch error
                    self.xml_dom = ET.fromstring(resp.get("body").encode("UTF-8"))
                    return
                self.xml_dom = []
        return Friends(self._conn) 
