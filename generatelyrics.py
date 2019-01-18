import lyricsgenius as genius
import re
from random import choice


def getLyrics():
    print("Getting lyrics from Genius API...")
    token = 'IDaz9BipEhMH7Tpcgrl3WIaJvslArOP_wPkrSgZyUwJA7Mjlht_aFBvXYJGzhvud'
    api = genius.Genius(token)
    artists = ['Ozuna', 'Anuel AA', 'J Alvarez', 'Daddy Yankee', 'Don Omar', 'Bad Bunny',
               'DJ Luian & Mambo Kingz',
              'Nicky Jam', 'J Balvin', 'Farruko', 'Nio García', 'Casper Mágico', 'Brytiago',
               'Wisin', 'Yandel', 'Wisin & Yandel', 'Arcángel', 'Tego Calderón',
              'Anonimus', 'Juhn', 'Darell', 'Zion & Lennox', 'Noriel',
               'Cosculluela', 'Ñengo Flow', 'Juanka "El Problematik"', 'Bryant Myers',
               'Lary Over','Manuel Turizo', 'Justin Quiles']

    lyrics = ""
    index = []
    i = 0
    while i < 50:
        index.append(i)
        i += 1

    for x in artists:
        artist = api.search_artist(x, max_songs=5)
        for y in index:
            if index[y] == len(artist.songs):
                break
            lyrics += artist.songs[y].lyrics + "\n"

    formattedLyrics = re.sub("[\(\[].*?[\)\]]", "", lyrics)
    txtfile = open("lyricsfile.txt", "w")
    txtfile.write(formattedLyrics)
    txtfile.close()
    print("DONE")
    return formattedLyrics


def generateModel(text, order):
    model = {}
    for i in range(0, len(text) - order):
        fragment = text[i:i + order]  # Range is exclusive at upper bound
        nextLetter = text[i + order]  # So this is the next letter
        if fragment not in model:
            model[fragment] = {}
        if nextLetter not in model[fragment]:
            model[fragment][nextLetter] = 1
        else:
            model[fragment][nextLetter] += 1
    return (model)


def getNextCharacter(model, fragment):
    letters = []
    for letter in model[fragment].keys():
        for occurences in range(0, model[fragment][letter]):
            letters.append(letter)  # So random.choice has a greater weighted chance of selecting this one
    return (choice(letters))


def generateLyrics(trainingText, order, length):
    print("Generando una letra chido..." + "\n")
    model = generateModel(trainingText, order)
    currentFragment = trainingText[0:order]
    output = ""
    for i in range(0, length - order):
        newCharacter = getNextCharacter(model, currentFragment)
        output += newCharacter
        currentFragment = currentFragment[1:] + newCharacter
    return (output)



# getLyrics()

with open('lyricsfile.txt', 'r') as myfile:
    lyrics = myfile.read()
generated = generateLyrics(lyrics, 8, 600)

print(generated)

