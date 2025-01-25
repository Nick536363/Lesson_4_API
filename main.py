import urllib.parse
from requests import *
from pprint import pprint
import os
import urllib

launch_id_spacex = "5eb87d47ffd86e000604b38a"
url_spacex = f"https://api.spacexdata.com/v5/launches/{launch_id_spacex}"
response_spacex = get(url_spacex)
response_spacex.raise_for_status()


url_apod = "https://api.nasa.gov/planetary/apod"
payload = {"api_key":"gCWcXPLpSbbu5zM6feOeF3VK2AzqMOpuZGdHvVIl",
           "count":30,
           }
response_apod = get(url_apod,params=payload)

url_epic = "https://api.nasa.gov/EPIC/api/natural/images?"
params = {"api_key":"gCWcXPLpSbbu5zM6feOeF3VK2AzqMOpuZGdHvVIl"}
responce_epic = get(url_epic,params=params)
responce_epic.raise_for_status()

def image_download(url,parametrs,path):
    response = get(url,params=parametrs)
    response.raise_for_status()
    with open(path, "wb") as file:
        file.write(response.content)

def get_file_ext(url):
    path = urllib.parse.urlparse(url).path
    return os.path.splitext(path)[1]

def fetch_spacex_last_launch():
    image_count = 0
    for link in response_spacex.json()["links"]["flickr"]["original"]:
        image_download(link,f"images\SPACEX\spacex_{image_count}.jpg")
        image_count+=1

def fetch_apod_image():
    for index, value in enumerate(response_apod.json(), 1):
        filename = f"image_{index}.jpg"
        apod_link = value["url"]

        image_download(apod_link,f"images\APOD\{filename}")
def fetch_epic_images():
    for index, value in enumerate(responce_epic.json()):
        date = value["date"].split(" ")[0].split("-")
        url_image = f"https://api.nasa.gov/EPIC/archive/natural/{date[0]}/{date[1]}/{date[2]}/png/{value["image"]}.png"
        image_download(url_image,params,f"images\EPIC\image_{index}.png")