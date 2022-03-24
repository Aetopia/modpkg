from glob import glob
from requests import get
from os import mkdir, path, remove
from pathlib import PurePath
from subprocess import run

# Variables
API_BASE = 'https://api.modrinth.com/v2'

def search(queries: tuple):
    for query in queries:
        params =  {'query':query, 'index':'relevance'}
        results = get(f'{API_BASE}/search', params = params).json()["hits"]
        if results != []:
            print(f'Looking for "{query}"...\nResults:')
            for result in results:
                if result['client_side'] == 'required':
                    print(f'\n{result["title"]} | {result["slug"]}\n{result["description"]}\nVersion: {result["latest_version"]}')  
            print()  
        else:
            print(f"Couldn't find", f'"{query}".')

class profile():
    def add(name: str, version: str, dir: str):
        if path.exists('profiles') is False:
            mkdir('profiles')
        with open(f'profiles/{name.lower()}.txt', 'w+') as profile:
            profile.write('\n'.join((version, path.abspath(dir))))
            print(f'Added [{name}] as a profile.')

    def get(profile: str):
        profile = profile.lower()
        if path.exists('profiles') is False:
            mkdir('profiles')
        if str(PurePath(f'profiles/{profile}.txt')) in glob('profiles/*.txt'):
            with open(path.abspath(f'profiles/{profile}.txt'), 'r+') as file:
                return file.read().splitlines()
        else:
            print(f"{profile} doesn't exist!")
            exit(0)        

    class mods():
        def index(name: str, mods: tuple):
            name = name.lower()
            with open(path.abspath(f'profiles/{name.lower()} - mods.txt'), 'w+') as file:
                file.write('\n'.join(mods))

        def get(name: str):
            name = name.lower()
            if str(PurePath(f'profiles/{name} - mods.txt')) in glob('profiles/*.txt'):
                with open(path.abspath(f'profiles/{name} - mods.txt'), 'r+') as file:
                    return file.read().splitlines()   
            else:
                return []                  

class mod():
    def install(slugs: tuple, name: str):
        mods = profile.mods.get(name)
        version, dir = profile.get(name)
        valid = True
        if path.exists(f'{dir}/mods') is False:
            mkdir(f'{dir}/mods')
        if mods == []:
            mods_list = True
        else:
            mods_list = False  
            installed_mods = ()
            for mod in mods:
                installed_mods += mod.split('/', 1)[0].strip(),  
        for slug in slugs:
            slug = str(slug).lower()
            response = get(f'{API_BASE}/project/{slug}/version')
            if response.status_code == 404:
                print('404 Error!')
            else:
                response = response.json()
                for index in range(len(response)):
                    if version in response[index]["game_versions"]:
                        mod_data = response[index]["files"][0]  
                        valid = True
                        break
                    else:
                        valid = False
                if valid is False:
                    print(f"({version}) isn't a valid MC version.") 
                    exit(1)       
                if mods_list:
                    print(f'Installing {slug} ({response[index]["version_number"]})... | {name}')
                    run(['curl', '-#', '-L', f'{mod_data["url"]}', '-o', f'{dir}/mods/{mod_data["filename"]}'])
                    mods += [f'{slug} / {mod_data["filename"]} / {mod_data["hashes"]["sha1"]} / {response[index]["version_number"]}'] 
                    print()
                elif mods_list is False: 
                    if slug in installed_mods:
                        print(f'Update "{slug}" using "-update".')   
                    else:
                        print(f'Installing {slug} ({response[index]["version_number"]})...')
                        run(['curl', '-#', '-L', f'{mod_data["url"]}', '-o', f'{dir}/mods/{mod_data["filename"]}'])
                        mods += [f'{slug} / {mod_data["filename"]} / {mod_data["hashes"]["sha1"]} / {response[index]["version_number"]}']  
                        print()   
        profile.mods.index(name, mods)    

    def update(name: str):
        mods = profile.mods.get(name)
        version, dir = profile.get(name)
        valid = True
        if mods == []:
            print('No installed mods for the specified profile.')
            exit(1)
        print(f'Checking [{name}]...\n')    
        slugs, hashes, files, versions = (), (), (), ()
        for mod in mods:
            slugs += mod.split('/')[0].strip(),
            files += mod.split('/')[1].strip(),
            hashes += mod.split('/')[2].strip(),
            versions += mod.split('/')[3].strip(),
        for slug_index, slug in enumerate(slugs):
            response = get(f'{API_BASE}/project/{slug}/version')
            if response.status_code == 404:
                print('404 Error!')
            else:
                response = response.json()
                for index in range(len(response)):
                    if version in response[index]['game_versions']:
                        mod_data = response[index]['files'][0]
                        valid = True
                        break    
                    else:
                        valid = False
                if valid is False:
                    print(f"({version}) isn't a valid MC version.") 
                    exit(1)      
                if mod_data['hashes']['sha1'] in hashes:
                    print(f'{slug} is update to date.')
                else:
                    print(f'Updating {slug}...\n({versions[slug_index]} -> {response[index]["version_number"]})')
                    if path.exists(f'{dir}/mods/{files[slug_index]}'):
                        remove(f'{dir}/mods/{files[slug_index]}')
                    run(['curl', '-#', '-L', f'{mod_data["url"]}', '-o', f'{dir}/mods/{mod_data["filename"]}'])  
                    mods[slug_index] = f'{slug} / {mod_data["filename"]} / {mod_data["hashes"]["sha1"]} / {response[index]["version_number"]}'   
                    print()
        profile.mods.index(name, mods)      