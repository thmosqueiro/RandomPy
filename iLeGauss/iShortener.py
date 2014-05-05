import urllib

def shorten_url(long_url, login_user, api_key):

	try:
		print " -- iShortener\n\n"
		print ".shortening %s" %(long_url)
        	longUrl = urllib.urlencode(dict(longUrl=long_url))
        	login = urllib.urlencode(dict(login=login_user))
	        apiKey = urllib.urlencode(dict(apiKey=api_key))
       
        	encodedurl="http://api.bit.ly/shorten?version=2.0.1&%s&%s&%s" % (longUrl, login, apiKey)

	        request = urllib.urlopen(encodedurl)
	        responde = request.read()
        	request.close()
        	responde_dict = eval(responde)
	        short_url = responde_dict["results"][long_url]["shortUrl"]
		
		print ".url shortened: %s" %(short_url)
	        return short_url

	except IOError, e:
        	raise "urllib error "


if __name__ == '__main__':
	shorten_url('http://http://tux-log.blogspot.com', 'thmosqueiro', 'R_66a444b82f5fb461cbb80ba930b87690' ) 
