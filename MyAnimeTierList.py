import requests as r
import re
import os

images_directory = "images"
images_extension = ".jpg"

username = input("Please enter your MAL username : ")

while True:
    response = r.get("https://api.myanimelist.net/v0/users/" + username + "/animelist?limit=1000&status=completed")
    if response.status_code != 200:
        print("Error code : " + str(response.status_code))
        print("This user's profile couldn't be found, please try again")
        username = input("Please enter your MAL username : ")
    else:
        break

rmdir = input("\nRemove previously downloaded images ? \n(y/n) ")

if os.path.exists(images_directory) and (rmdir == "y" or rmdir == "yes"):
    for f in os.listdir(images_directory):
        os.remove(os.path.join(images_directory, f))
    print("images deleted")

if not os.path.exists(images_directory):
    os.mkdir(images_directory)

only_first_season = input("\nOnly download first seasons ? \nThis will take a bit longer and won't perfectly work if "
                          "you skipped seasons (some animes may have inbetween seasons you're not be aware of ...)"
                          "\n(y/n) ")

animes = response.json()["data"]
animes_ids = []
for node in animes:
    animes_ids.append(node["node"]["id"])


english_titles = input("\nUse english title for image names ? (images names will be the janapese title by default) "
                       "\n(y/n) ")

for node in animes:
    anime=node["node"]
    first_season = True

    if only_first_season == "y" or only_first_season == "yes" or english_titles == "y" or english_titles == "yes":
        response = r.get("https://api.myanimelist.net/v0/anime/" + str(anime["id"]) + "?fields=related_anime,alternative_titles")
        if response.status_code == 200:
            details = response.json()

    if only_first_season == "y" or only_first_season == "yes":
        first_season = True
        for relation in details["related_anime"]:
            if (relation["relation_type"] == "prequel" or relation["relation_type"] == "parent_story") and relation["node"]["id"] in animes_ids:
                first_season = False

    if first_season:
        img_data = r.get(anime["main_picture"]["medium"]).content

        anime_name = anime["title"]
        if english_titles == "y" or english_titles == "yes":
            english_name = details["alternative_titles"]["en"]
            if english_name != "":
                anime_name = english_name

        filename = re.sub(r"[!\"\#$%&'()*+,-./:;<=>?@\[\]^_`{|}~]", "", anime_name)
        filename = re.sub(r" +", "_", filename)
        print("saved "+filename+images_extension)

        with open(images_directory+"/"+filename+images_extension, 'wb') as handler:
            handler.write(img_data)

print("\nDONE ! Images save to \"images\" folder")
