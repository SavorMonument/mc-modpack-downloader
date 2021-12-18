#!/usr/bin/env python3

import requests
import itertools
import json
import sys
import os

from concurrent.futures import ThreadPoolExecutor

# This is depricated
MOD_INFO_URL = 'https://cursemeta.dries007.net'

def download_mod(mod_details, index, mod_count):
    print('Downloading...(%d/%d)' % (index, mod_count))

    mod_data = get_mod_data(mod_details['projectID'], mod_details['fileID'])
    print(mod_data)
    download_url = mod_data['DownloadURL']
    file_name = mod_data['FileNameOnDisk']
    download_file(download_url, 'mods/' + file_name)

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

if __name__ == '__main__':
    manifest = load_manifest(sys.argv[1])
    os.mkdir('mods')

    mod_count = len(manifest['files'])

    print("Starting mods download")
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_mod, manifest['files'], itertools.count(1, 1), itertools.repeat(mod_count))
    print("Done")

