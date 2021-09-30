import requests

url = 'https://morgenwirdes.de/wetter.php?id=567'
r = requests.get(url).text
print(r)



#import urllib.request

#x = urllib.request.urlopen('https://www.google.com/')
#print(x.read())




# import requests module
#import requests
 
# Making a get request
#response = requests.get('https://expired.badssl.com/', verify = False)
 
# print request object
#print(response)