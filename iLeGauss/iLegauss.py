#!/usr/bin/python

#
# - iLegauss v0.9
# by thmosqueiro @ 02.2010
#


import re
import string
from sys import stdout
import httplib, urllib, urllib2
from xml.dom import minidom
import twitter
from time import sleep


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\e[0;34m'
    ENDC = '\033[0m'
    
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''



def warningmsg(string):
    clr = bcolors()
    print "\n\n-- " + clr.WARNING + string + clr.ENDC
    return
        
        
        
def shorten_url(long_url, login_user, api_key):
            
    try:
 #       print ".shortening %s" %(long_url)
        longUrl = urllib.urlencode(dict(longUrl=long_url))
        login = urllib.urlencode(dict(login=login_user))
        apiKey = urllib.urlencode(dict(apiKey=api_key))
        
        encodedurl="http://api.bit.ly/shorten?version=2.0.1&%s&%s&%s" % (longUrl, login, apiKey)
        
        request = urllib.urlopen(encodedurl)
        responde = request.read()
        request.close()
        responde_dict = eval(responde)
        short_url = responde_dict["results"][long_url]["shortUrl"]
        
#        print ".url shortened: %s" %(short_url)
        return short_url
    
    except IOError, e:
        warningmsg(" [ ERROR: sorry, we are experiencing some URLLIB error. ] ")
        raise
	
	
	
	
def shortentitle(title):
		
    maxs = 70 - 1
    size = len(title)
	
    if size <= maxs:
        return title
    else:
        shorttitle = title[0:maxs-6]
        shorttitle += " (...)"
        return shorttitle



class ModelFeed:

    tweet = []

    clr = bcolors()
    newlastlink = ''

    istherenewpost = False
    entry_list = []

    faddress = ''


    def __init__(self, address):

        print " [ starting everything. ]"
        self.data = []
        self.faddress = address

        try:
            stdout.write(" [ connecting...")

            stdout.flush()
            file_request = urllib2.Request(self.faddress)
            file_opener = urllib2.build_opener()

            stdout.write(self.clr.OKGREEN + " connected. " + self.clr.ENDC + "]\n")

        except:
            warningmsg("[ Problems when connecting to feed adddress. ]")
            raise
        
        try:
            stdout.write(" [ getting feed...")

            stdout.flush()
            file_feed = file_opener.open(file_request).read()
            file_xml = minidom.parseString(file_feed)
            self.entry_list = file_xml.getElementsByTagName("entry")

            stdout.write(self.clr.OKGREEN + " got." + self.clr.ENDC + " ]\n")

        except:
            warningmsg("[ Problems when getting feed. ]")
            raise




    def getPosts(self):

        lastpostlink = self.lastPostLink()
        postnumber = 0
        tweeti = [] # inverted post list for tweet.
        
        print " [ starting to read. ]"        

        try:
            for item in self.entry_list:

                postnumber += 1

                position = -1
                position = self.find("title", position, item)
                title = item.childNodes[position].firstChild.nodeValue

                shorttitle = shortentitle(title)
                
                position = self.find("link", position, item)
                link = item.childNodes[position+4].getAttribute("href")
                
            # important for debugging:
                if str(link).find(lastpostlink) == 0:
                    break

                if postnumber == 1:
                    istherenewpost == True
                    newlastlink = str(link)
                        
                print "\n -> getting new post - #%i " %(postnumber)

                shortlink = shorten_url(str(link), 'thmosqueiro', 'R_66a444b82f5fb461cbb80ba930b87690' ) 

                position = self.find("author", position, item)
                author = item.childNodes[position].childNodes[0].firstChild.nodeValue

                tweeti.append(shorttitle + " por " + author + " - " + shortlink + " #legauss") 
                print tweeti[postnumber - 1]

        except:
            warningmsg("[ DON'T PANIC: it's just an unexpected error. ] ")
            raise


        #-- END WHILE

        #finally, just inverting order
        for i in range(0, len(tweeti), 1): 
            self.tweet.append(tweeti[len(tweeti) - 1 - i])




    def find(self, keyword, startat, item):
        i = startat
        got = True
        while got:
            i += 1
            mattersn = item.childNodes[i]
            if mattersn.localName == keyword:
                got = False

        return i




    def lastPostLink(self):

        try:
            datafile = open("iLegauss.aux", "r")
            link = datafile.readline()
            datafile.close()
            return link[0:len(link)-1]

        except EOFError:
            warningmsg(" [ Error when reading from 'iLegauss.aux'. ] ")
            raise
        except IOError:
            warningmsg(" [ Error when oppening 'iLegauss.aux'. ] ")
            raise
        except:
            warningmsg(" [ PANIC: unexpected error! ] ")
            raise




    def LPUpdate(newlastlink):

        try:
            datafile = open('iLegauss.aux', 'w')
            datafile.write(newlastlink)
            datafile.close()
            return

        except EOFError:
            warningmsg(" [ Error when writing to 'iLegauss.aux'. ] ")
            raise
        except IOError:
            warningmsg(" [ Error when oppening 'iLegauss.aux'. ] ")
            raise
        except:
            warningmsg(" [ PANIC: unexpected error! ] ")
            raise




class twittcon:

    user = ''
    psswd = ''
	
    clr = bcolors()

    going = "-"
    togo = " "
    gone = "#"


    def __init__(self):
        stdout.write(" [ connecting to twitter... ")
        stdout.flush()
        self.api = twitter.Api(self.user, self.psswd) # configured only for legauss
        stdout.write(self.clr.OKGREEN + "connected" + self.clr.ENDC + " ]\n")


    def Post(self, status_list):
        counter = 0
        topost = len(status_list)

        for item in status_list:
            counter += 1
            stdout.write("\r [ tweeting: %i/%i " %(counter, topost))
            stdout.write((counter - 1)*self.gone + self.going + (topost-counter)*self.togo + "       ]")

            # this is a trial
            self.api = twitter.Api(self.user, self.psswd)
            status = self.api.PostUpdate(item)

            # nice to debugg!
            # stdout.write(" <" + str(status.GetId()) )#str(self.api.GetStatus(status.GetId()).GetText()) + ">")

            stdout.flush()            
            sleep(10) # pauses the status update so twitter does not fall apart...

        stdout.write("\r [ tweeting: %i/%i " %(counter, topost))
        stdout.write((topost + 1)*self.gone + self.clr.OKGREEN + " done." + self.clr.ENDC  + " ]")




def main():
    
    b = bcolors()
    gin = "thmosqueiro"
    apikey = "R_66a444b82f5fb461cbb80ba930b87690";
    feedurl = "http://legauss.blogspot.com/feeds/posts/default"
    
    print "\n\n -- iLegauss\n" + b.ENDC

    feed = ModelFeed(feedurl)
    feed.getPosts()

    print "\n"
    
    if feed.istherenewpost:

        twitinst = twittcon()
        twitinst.Post(feed.tweet)
        
        print "\n [ All new posts tweeted. ] "

        print " [Updating data. ]"
        try:
            if feed.istherenewpost:
                LPUpdate(feed.newlastpost)
        except:
            warningmsg()
            raise
    else:
        print " [ No new posts. ] "        
    
    print " [ Waiting for more... ] \n\n"


if __name__ == "__main__":
    main() 
