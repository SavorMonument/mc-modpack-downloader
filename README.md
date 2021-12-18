# Minecraft modpack downloader

This script downloads the mods for a modpack using the manifest file

### Usage
  python3 downloader.py [manifest_path]

#### Manifest file
  - find the modpack on curseforge.com go to: Files -> click on version.zip -> download
  - uzip and the manifest is in there

#### Build modpack
  - create a folder in ~/.minecraft/modded/[name_of_modpack]
  - put in the mods/ folder that the script downloads
  - put in the files from overrides(found in the modpack zip), no need for mods/
  
  - get correct version of forge(version in manifest) and install it
  
  - in the minecraft launcher
    - create new installation with correct version of curse 
      - select the game directory to the modpack path
      - you can also change the java args here to increase ram
  
