from restful_lib import Connection, ConnectionError

from microblog_exceptions import MicroBlogMsgLimitExceeded

import sys,os,xmpp,time

IDENTICA_DEFAULT = "update@identi.ca"

class XMPPAuthenticationError(Exception):
    def __str__(self):
        return "XMPP authentication step failed"

class Identica_xmpp(object):
    def __init__(self, username=None, password=None, base_identica_user=IDENTICA_DEFAULT):
        self.username = username
        self.password = password
        self.posttouser = base_identica_user

    def post(self, message, clip_length=False):
        if len(message)>140:
            if clip_length:
                message = message[:140]
            else:
                raise MicroBlogMsgLimitExceeded


        jid=xmpp.protocol.JID(self.username)
        cl=xmpp.Client(jid.getDomain(),debug=[])

        con=cl.connect()
        if not con:
            raise ConnectionError
        # print 'connected with',con
        auth=cl.auth(jid.getNode(),self.password,resource=jid.getResource())
        if not auth:
            raise XMPPAuthenticationError
        #print 'authenticated using',auth

        #cl.SendInitPresence(requestRoster=0)   # you may need to uncomment this for old server
        id=cl.send(xmpp.protocol.Message(self.posttouser,message))
        #print 'sent message with id',id
        time.sleep(1)   # some older servers will not send the message if you disconnect immediately after sending

        cl.disconnect()
