#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tweepy 


# In[ ]:


from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


# In[ ]:


import socket


# In[ ]:


import json


# In[ ]:


consumer_key = 'RepN9liYtNkjGKHjs7mYIqMdu'


# In[ ]:


consumer_secret= '0W5CGbAtiyTj2AYMGuEPGUs2EBPanpFssSOS4yl2zuIDE4JFY9'


# In[ ]:


access_token= '1209197420271357953-hWAW4Xjkywh2VBdyBbyYlHIm96Nm8I'


# In[ ]:


access_secret= "LYqRlIooJomFzTr2sDDrhjT6ID4v2tZKT4cyOwlHrvU1Y"


# In[ ]:


class TweetsListener (StreamListener):
    
    def __init__(self, csocket):
        self.client_socket = csocket
        
    def on_data(self, data):
        try:
            msg = json.loads( data )
            print( msg['text'].encode('utf-8') )
            self.client_socket.send( msg['text'].encode('utf-8') )
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    
    def on_error(self, status):
            print(status)
            return True


# In[ ]:


def sendData(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['soccer'])


# In[ ]:


if __name__ == "__main__":
    s = socket.socket()
    host = "127.0.0.1"
    port = 5553
    s.bind((host, port))
    
    print('Listening on port: %s' % str(port))
    
    s.listen(5)
    
    c, addr = s.accept()
    
    print( "Received request from: " + str( addr ) )
    
    sendData( c )


# In[ ]:




