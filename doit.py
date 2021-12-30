#!/usr/bin/env python
import requests
import json
import sys

# get this from your browser (see exneuland links)
token = ""
first_slug = "/rc3_21/lebkuchis/cellar.json"
# first_slug = "rc3_21/lobby/main.json"
first_slug = sys.argv[1] if len(sys.argv) == 2 else "rc3_21/lobby/main.json"
dldir = "maps"
from os.path import join,dirname,basename, normpath
from os import makedirs

managed_slugs = []

def resolve_slug(slug:str,token:str) -> dict:
    # slug may be rc3_21/lobby/main.json
    url = f"https://visit.rc3.world/@/{slug}"
    return (requests.get("https://exneuland.rc3.world/map",params = { "playUri": url, "authToken": token}).json())

def find_exits(mapdata:dict,slug:str):
    for layer in mapdata['layers']:
        for prop in layer.get('properties',[]):
            if prop.get('name','').lower() in [ 'exiturl','exitsceneurl']:
                val = prop['value'].split('#')[0]
                if val.startswith('/'):
                    yield val.strip("/@")
                else:
                    yield normpath(join(dirname(slug),val))
                pass

def download_tileset(url:str,outpath:str):
    #print(url)
    r = requests.get(url)
    #print(f"writing tileset to {outpath}")
    makedirs(dirname(outpath),exist_ok=True)
    with open(outpath,'wb+') as f:
        f.write(r.content)

def download_map(url:str,slug:str):
    mapdata = requests.get(url).json()
    map_storepath = join(dldir,slug)
    map_storedir = dirname(map_storepath)
    #print(f"creating {map_storedir}")
    makedirs(map_storedir,exist_ok=True)

    for tileset in mapdata['tilesets']:
        tiledata = tileset['image']
        download_tileset(f"{dirname(url)}/{tiledata}",join(map_storedir,tiledata))

    with open(map_storepath,"w+") as f:
        print(f"writing map to {map_storepath}")
        json.dump(mapdata,f)

    print(f"handled all exits of {slug}, finalizing")
    managed_slugs.append(slug)

    #with open('managed_slugs.json','w+') as f:
    #    json.dump(managed_slugs,f)
    
    # TODO: persist current exits so we can actually continue scraping
    for i in list(find_exits(mapdata,slug)):
        if i is not slug:
            handle_slug(i)
        else:
            print("will not handle self")



def handle_slug(slug):
    if slug in managed_slugs:
        print(f"skipping slug {slug} because we already downloaded it")
    else:
        print(f"handling slug {slug}")
        resolved = resolve_slug(slug,token)
        try:
            download_map(resolved['mapUrl'],resolved['roomSlug'])
        except Exception as e:
            print("something went horribly wrong when handing slug {slug}")
            print(e)


def main():
    handle_slug(first_slug)

if __name__ == "__main__":
    main()
