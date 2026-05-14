import os
import sys
import time
import shutil
import zipfile
import requests
import subprocess
from colorama import init, Fore, Style

import gdown

init()


urls = {
    "mod_tools_file": "https://drive.google.com/file/d/1nxYZZfiE8KVJQiJ3ed9-Y8tgi8Dz2QY7/view?usp=sharing",
    "game_mod": "https://github.com/Nukem9/LinkerMod/releases/download/v1.3.2/game_mod.zip",
    "linker_mod": "https://github.com/Nukem9/LinkerMod/releases/download/v1.0.0-r/LinkerMod-1.0.0.zip",
    "end_message": "https://dn721905.ca.archive.org/0/items/black_ops_mod_tools_installer_files/End_Message.txt",
    "shippuden_map_maker": "https://drive.google.com/file/d/1N7hcNr2SMLfAS2Wru5QmqPj5hkFScUkE/view?usp=sharing"
}


process_name = 'BlackOps.exe'


if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir  = os.path.dirname(os.path.abspath(__file__))


temp_dir = f'{script_dir}/temp'

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)


os.chdir(temp_dir)


def download_file(url, dest):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Downloaded {dest}')
    except requests.exceptions.RequestException as e:
        print(f'Failed to download {url}: {e}')


def extract_zip(file_path, extract_to):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f'Extracted {file_path} to {extract_to}')
    except zipfile.BadZipFile as e:
        print(f'Failed to extract {file_path}: {e}')


def print_intro():
    print(Fore.GREEN + Style.BRIGHT + """
                                    #     #                                           ###
                                    ##   ## #   # ##### #    # #  ####    ##   #      ###  ####
                                    # # # #  # #    #   #    # # #    #  #  #  #       #  #
                                    #  #  #   #     #   ###### # #      #    # #      #    ####
                                    #     #   #     #   #    # # #      ###### #               #
                                    #     #   #     #   #    # # #    # #    # #          #    #
                                    #     #   #     #   #    # #  ####  #    # ######      ####
#####   ####    #    #  ####  #####    #####  ####   ####  #       ####    # #    #  ####  #####   ##   #      #      ###### #####
#    # #    #   ##  ## #    # #    #     #   #    # #    # #      #        # ##   # #        #    #  #  #      #      #      #    #
#####  #    #   # ## # #    # #    #     #   #    # #    # #       ####    # # #  #  ####    #   #    # #      #      #####  #    #
#    # #    #   #    # #    # #    #     #   #    # #    # #           #   # #  # #      #   #   ###### #      #      #      #####
#    # #    #   #    # #    # #    #     #   #    # #    # #      #    #   # #   ## #    #   #   #    # #      #      #      #   #
#####   ####    #    #  ####  #####      #    ####   ####  ######  ####    # #    #  ####    #   #    # ###### ###### ###### #    #
""")

    print(Fore.GREEN + Style.BRIGHT + """
This tool installs the following:

- Game_mod
- Linker_mod
- Assets_wip_0.1.0
- Ville's various mod tools fixes, the latest from Jan 2, 2024
- FTG Remastered BO map source example
- Shippuden Map Maker
- SteamCMD
- It will also run the setup.bat, converter, and clean up unneeded files

It will also automatically handle merging the the mod tools dir with the game dir as need be

Important Notes:

- Having Bgamer installed can replace key files, if you are having issues check this first
- Some errors/warning when the converter is ran is normal, you can ignore them.
- Don't run the converter yourself unless you're absolutely sure.
- rerunning this bat will rerun the converter. Backup projects first if you're worried.
- It has the potential to delete files you may want to keep.
- Installing older mod fixes over this will likely cause problems.
- The Launcher.exe must be ran as administrator or else errors may occur.
- Your Install will approximately 15gb or so depending on dlc owned.
- If this window gets stuck, try clicking on it, then hitting enter.
- If that doesn't work close it and run it again.
- If you haven't already placed this bat in your BO + Mod Tools install (next to your BlackOps.exe) close this window and do so before continuing.
""")
    input("Enter 'start' to continue: ")


def download_setup_files():
    print('\nDownloading necessary files...')
    gdown.download(urls['mod_tools_file'], 'black_ops_one_mod_tool_files.zip')
    gdown.download(urls['shippuden_map_maker'], 'shippuden_map_maker.zip')
    download_file(urls['game_mod'], 'game_mod.zip')
    download_file(urls['linker_mod'], 'LinkerMod-1.0.0.zip')
    download_file(urls['end_message'], 'End_Message.txt')


def extract_file_set_one():
    print('\nExtracting files...')
    extract_zip("game_mod.zip", script_dir)
    extract_zip("LinkerMod-1.0.0.zip", script_dir)


def extract_file_set_two():
    extract_zip('black_ops_one_mod_tool_files.zip', script_dir)
    extract_zip('shippuden_map_maker.zip', script_dir)


def run_setup_bat():
    setup_bat_path = f'{script_dir}/bin/scripts/setup.bat'
    subprocess.run(setup_bat_path, cwd=os.path.dirname(setup_bat_path))


def run_converter():
    converter_path = f'{script_dir}/bin/converter.exe'
    subprocess.run(f'{converter_path} -nopause -n -nospam', cwd=f'{script_dir}/bin')


def print_complete_message():
    with open(f'{temp_dir}/End_Message.txt', 'r') as f:
        print(f.read())
    print('\nInstallation complete. Exiting in 30 seconds...')
    time.sleep(30)


def open_game():
    black_ops_path = os.path.normpath(f'{script_dir}/{process_name}')
    if not os.path.isfile(black_ops_path):
        missing_exe_error = f'No black ops exe was found at the following location: "{black_ops_path}"'
        raise FileNotFoundError(missing_exe_error)
    subprocess.run(black_ops_path)
    time.sleep(45)


def close_game():
    subprocess.run(f'taskkill /F /IM {process_name}')


def file_cleanup():
    try:
        os.chdir(script_dir)
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Failed to remove temp directory: {e}")


def is_mod_tools_dir_already_merged() -> bool:
    mod_tools_dir = os.path.normpath(f'{script_dir}/../Call of Duty Black Ops 42740')
    return not os.path.isdir(mod_tools_dir)


def merge_mod_tools_dir():
    mod_tools_dir = os.path.normpath(f'{script_dir}/../Call of Duty Black Ops 42740')
    game_dir = script_dir

    if not os.path.isdir(mod_tools_dir):
        raise FileNotFoundError(f"Mod tools directory not found: {mod_tools_dir}")

    for item in os.listdir(mod_tools_dir):
        src = os.path.join(mod_tools_dir, item)
        dst = os.path.join(game_dir, item)

        if os.path.exists(dst):
            if os.path.isdir(src) and os.path.isdir(dst):
                for root, dirs, files in os.walk(src):
                    rel = os.path.relpath(root, src)
                    target_root = os.path.join(dst, rel)
                    os.makedirs(target_root, exist_ok=True)

                    for f in files:
                        s_file = os.path.join(root, f)
                        d_file = os.path.join(target_root, f)
                        if not os.path.exists(d_file):
                            shutil.move(s_file, d_file)
            else:
                print(f"Skipping existing: {dst}")
        else:
            shutil.move(src, dst)

    shutil.rmtree(mod_tools_dir)

    try:
        if os.name == 'nt':
            os.system(f'mklink /J "{mod_tools_dir}" "{game_dir}"')
        else:
            os.symlink(game_dir, mod_tools_dir)
    except Exception as e:
        print(f"Failed to create symlink/junction: {e}")

    return


def main():
    print_intro()
    if not is_mod_tools_dir_already_merged():
         merge_mod_tools_dir()
    download_setup_files()
    extract_file_set_one()
    open_game()
    close_game()
    run_setup_bat()
    run_converter()
    extract_file_set_two()
    print_complete_message()
    file_cleanup()


if __name__ == '__main__':
    print(script_dir)
    main()
