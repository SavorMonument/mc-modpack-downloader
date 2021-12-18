#!/usr/bin/env python3

import itertools
import pathlib
import json
import sys
import os

from concurrent.futures import ThreadPoolExecutor

import requests

# This is depricated
MOD_INFO_URL = 'https://cursemeta.dries007.net'
FORGE_URL_TEMPLATE = "https://maven.minecraftforge.net/net/minecraftforge/forge/%s-%s/forge-%s-%s-installer.jar"

def download_mod(mod_details, index, mod_count, mods_path):
    print('Downloading...(%d/%d)' % (index, mod_count))

    mod_data = get_mod_data(mod_details['projectID'], mod_details['fileID'])
    download_url = mod_data['DownloadURL']
    file_name = mod_data['FileNameOnDisk']
    download_file(download_url, mods_path / file_name)

def get_mod_data(project_id, file_id):
    url = '%s/%d/%d.json' % (MOD_INFO_URL, project_id, file_id)
    response = requests.get(url)
    return json.loads(response.content)

def download_file(download_url, path):
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def load_manifest(manifest_path):
    with open(manifest_path) as man_f:
        return json.load(man_f)

def download_mods(manifest, to_path):
    to_path.mkdir(exist_ok=True)

    mod_count = len(manifest['files'])

    print("Starting mods download")
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_mod, manifest['files'], itertools.count(1, 1),\
                itertools.repeat(mod_count), itertools.repeat(to_path))
    print("Done downloading mods")

def print_forge_download_url(manifest):
    game_version = manifest["minecraft"]["version"]
    forge_version = manifest["minecraft"]["modLoaders"][0]["id"]

    print("\nNow get and install forge: %s\n" %\
            (FORGE_URL_TEMPLATE % (game_version, forge_version[6:], game_version, forge_version[6:])))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 downloader.py [zip_path]")
        sys.exit(0)

    zip_path = pathlib.Path(sys.argv[1])

    pack_dir = pathlib.Path(__file__).parent / zip_path.stem
    pack_dir.mkdir()

    # Unzip in pack dir and copy overrides over
    os.system("unzip %s -d %s/" % (zip_path, pack_dir))
    os.system("mv %s/* %s" % (pack_dir / "overrides/", pack_dir))
    os.system("rm -rf %s" % (pack_dir / "overrides/"))

    manifest = load_manifest(pack_dir / "manifest.json")
    download_mods(manifest, pack_dir / "mods/")
    print_forge_download_url(manifest)

