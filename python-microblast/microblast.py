#!/usr/bin/env python

import sys, os, time

from tinyurl import Tinyurl

# Need to make this a plugin arch
from identica import Identica_xmpp
from twitter import Twitter

from restful_lib import Connection, ConnectionError

__module_name__ = "Twitter"
__module_description__ = "Tweet from XChat"
__module_version__ = "0.1"

MICROBLAST_CONFIG_NAME = ".microblast"

if len(sys.argv) < 2:
    print "Syntax: blaster.py message"
    sys.exit(0)

message=' '.join(sys.argv[1:])

params={}
if os.access(os.environ['HOME']+'/' + MICROBLAST_CONFIG_NAME,os.R_OK):
    for ln in open(os.environ['HOME']+'/'+MICROBLAST_CONFIG_NAME).readlines():
        if not ln[0] in ('#',';'):
            key,val=ln.strip().split('=',1)
            params[key.lower()]=val

if params.get("tinyurl", "n") != "n":
    t = Tinyurl()
    words = message.split(" ")
    new_message = []
    for word in words:
        if word.startswith("http://"):
            new_message.append(t.get(word))
        else:
            new_message.append(word)
    message = " ".join(new_message)

if params.get("identica_im"):
    try:
        i = Identica_xmpp(params.get("identica_im"), params.get("identica_pass"))
        i.postnew(message)
    except Exception, inst:
        print "Identica - failed: %s" % inst

if params.get("twitter_id"):
    try:
        t = Twitter(params.get("twitter_id"), params.get("twitter_pass"))
        t.post(message)
    except Exception, inst:
        print "Twitter - failed: %s" inst
