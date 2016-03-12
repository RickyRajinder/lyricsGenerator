import urllib
import urllib2
import json
from random import choice
from bs4 import BeautifulSoup

def readApiKey():
	configFile = open("config.json", "r").read()
	config = json.loads(configFile)
	apiKey = config["apiKey"]
	return(apiKey)

def getLyrics(band, apiKey):
	encodedBand = urllib.quote_plus(band)
	url = "http://api.lyricsnmusic.com/songs?api_key="+apiKey+"&artist="+encodedBand

	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')] #Default is blocked :|
	response = opener.open(url).read()
	feed = json.loads(response)
	
	trainingText = ""
	songsProcessed = 0
	for song in feed:
		snippet = song["snippet"]
		fullUrl = song["url"]
		fullPageHTML = opener.open(fullUrl).read()
		page = BeautifulSoup(fullPageHTML, "html.parser")
		
		try:
			lyrics = str(page.findAll("pre")[0]).replace("<pre itemprop=\"description\">","").replace("</pre>","")
			trainingText += lyrics
		except:
			trainingText += snippet+"\n"
		songsProcessed += 1
		print("Learned "+str(songsProcessed)+" songs...")

	return(trainingText)

def generateModel(text, order):
	model = {}
	for i in range(0, len(text)-order):
		fragment = text[i:i+order] #Range is exclusive at upper bound
		nextLetter = text[i+order] #So this is the next letter
		if fragment not in model:
			model[fragment] = {}
		if nextLetter not in model[fragment]:
			model[fragment][nextLetter] = 1
		else:
			model[fragment][nextLetter] += 1
	return(model)

def getNextCharacter(model, fragment):
	letters = []
	for letter in model[fragment].keys():
		for occurences in range(0, model[fragment][letter]):
			letters.append(letter) #So random.choice has a greater weighted chance of selecting this one
	return(choice(letters))

def generateLyrics(trainingText, order, length):
	model = generateModel(trainingText, order)
	currentFragment = trainingText[0:order]
	output = ""
	for i in range(0, length-order):
		newCharacter = getNextCharacter(model, currentFragment)
		output += newCharacter
		currentFragment = currentFragment[1:]+newCharacter
	return(output)


apiKey = readApiKey()
band = raw_input("Enter artist:\n")
#band = "The 1975"

lyrics = getLyrics(band, apiKey)



newLyrics = generateLyrics(lyrics, 8, 600)

print(newLyrics)


