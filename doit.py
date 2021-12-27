#!/usr/bin/env python
import requests
import json

# get this from your browser (see exneuland links)
token = ""
first_slug = "/rc3_21/lebkuchis/cellar.json"
# first_slug = "rc3_21/lobby/main.json"
dldir = "maps"
from os.path import join,dirname,basename
from os import makedirs

def resolve_slug(slug:str,token:str) -> dict:
    # slug may be rc3_21/lobby/main.json
    url = f"https://visit.rc3.world/@/{slug}"
    return (requests.get("https://exneuland.rc3.world/map",params = { "playUri": url, "authToken": token}).json())

def download_tileset(url:str,outpath:str):
    print(url)
    r = requests.get(url)
    print(f"writing tileset to {outpath}")
    makedirs(dirname(outpath),exist_ok=True)
    with open(outpath,'wb+') as f:
        f.write(r.content)

def download_map(url:str,slug:str):
    mapdata = requests.get(url).json()
    map_storepath = join(dldir,slug)
    map_storedir = dirname(map_storepath)
    print(f"creating {map_storedir}")
    makedirs(map_storedir,exist_ok=True)

    for tileset in mapdata['tilesets']:
        tiledata = tileset['image']
        download_tileset(f"{dirname(url)}/{tiledata}",join(map_storedir,tiledata))

    with open(map_storepath,"w+") as f:
        json.dump(mapdata,f)


def main():
    resolved = resolve_slug(first_slug,token)
    download_map(resolved['mapUrl'],resolved['roomSlug'])

if __name__ == "__main__":
    main()
