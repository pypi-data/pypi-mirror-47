# aniScrape
Scraper for aniSearch.de and aniSearch.com

# requirements
- requests
- Python 3.x

# How to use it and what does it do?
It returns an dictionary for the given ID.
```
import aniScrape
dictionary = aniScrape.scrape(aS_ID,language,imghoster)

#aS_ID is the aniSearch ID 
#language determines whether it uses .de or .com. It will ONLY use .com if you input "en". Standard(without inputting anything) is .de
#imghoster: you can input "imgur" or "imgbb", it will upload the image from aS to the given hoster. If nothing is given, it will return an None statement
```

# Dictionary Definitions

```
{
 "id": aS ID,
 "error": Whether an Error occured or not(if no Error: False),
 "jap": "Japanese Name*",
 "kan": "Kanjis*",
 "eng": "English/International Name*",
 "ger": "German Name*",
 "syn": [
  "Synonyms in a List"
 ],
 "description": "Full Description without links*",
 "type": "Type of Series*",
 "time": "Average Time per Episode in Minutes*",
 "episodes": "Episodes of the season*",
 "date": {
  "year": "year*",
  "month": "month*",
  "day": "day*"
 },
 "origin": "Japan*",
 "adaption_of": "Light Novel*",
 "targetgroup": "Male*",
 "genres": {
  "genre_main": [
   "Main Genre in a List"
  ],
  "genre_sub": [
   "Sub",
   "Genres",
   "in",
   "a",
   "List"
  ],
  "tags": [
   "Tags",
   "in",
   "a",
   "List"
  ]
 },
 "img": "Link to the aniSearch image* (Will be None if the picture at aniSearch is Empty)",
 "hoster": "link to the chosen host*"
}

* Everything with a "*" CAN be "None" if not available on website
```

# Full Dictionary Example

```
print(json.dumps(aniScrape.scrape(7335,"en","imgbb"),indent=1))

{
 "id": 7335,
 "error": false,
 "jap": "Sword Art Online",
 "kan": "\u30bd\u30fc\u30c9\u30a2\u30fc\u30c8\u30fb\u30aa\u30f3\u30e9\u30a4\u30f3",
 "eng": "Sword Art Online",
 "ger": null,
 "syn": [
  "SAO"
 ],
 "description": "Blurb:Escape was impossible until it was cleared; a game over would mean an actual \u00abdeath\u00bb. Without knowing the \u00abtruth\u00bb of the mysterious next generation MMO, \u00abSword Art Online\u00bb (SAO), approximately ten thousand users logged in together, opening the curtains to this cruel death battle. Participating alone in SAO, protagonist Kirito had promptly accepted the \u00abtruth\u00bb of this MMO. And in the game world, a gigantic floating castle named \u00abAincrad\u00bb, he distinguished himself as a solo player.Aiming to clear the game by reaching the highest floor, Kirito riskily continued alone. Because of a pushy invitation from a female warrior and rapier expert, Asuna, he teamed up with her. That encounter brought about an opportunity to call out to the fated Kirito.",
 "type": "TV-Series",
 "time": "24",
 "episodes": "25",
 "date": {
  "year": "2012",
  "month": "07",
  "day": "08"
 },
 "origin": "Japan",
 "adaption_of": "Light Novel",
 "targetgroup": "Male",
 "genres": {
  "genre_main": [
   "Action Drama"
  ],
  "genre_sub": [
   "Action",
   "Adventure",
   "Drama",
   "Fantasy",
   "Romance",
   "Science-Fiction"
  ],
  "tags": [
   "Alternative World",
   "Contemporary Fantasy",
   "Hero of Strong Character",
   "Magic",
   "Swords & Co",
   "Virtual World"
  ]
 },
 "img": "https://cdn.anisearch.com/images/anime/cover/full/7/7335.jpg",
 "hoster": "https://i.ibb.co/WnBXx3c/7335.jpg"
}

```
