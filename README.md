# Minecraft modpack downloader

This script downloads the files for a modpack using it's zip file

### Usage
  python3 downloader.py [pack_path].zip
  - it's going to download and assemble the pack folder in the current directory

#### Pack zip
  - find the modpack on curseforge.com go to: Files -> click on version.zip -> download

#### Build modpack
  - you can put the pack folder somewhere in the game folder ex: `~/.minecraft/modded/[name_of_modpack]`
  - install the correct forge version(the script prints the link where to download it at the end)
  
  - in the minecraft launcher
    - create new installation with correct version of forge 
      - select the game directory to the modpack path
      - you can also change the java args here to increase ram
  
