from os import chdir
from requests import get
from subprocess import run

# Get information on a given mod.
response = get('https://api.modrinth.com/v2/project/modmenu/version').json()

# Parse some information and display it.
for x, y in enumerate(response):
    versions = tuple(y['game_versions'])
    print(y['name'], versions)  

# Check if the given version is compatible.    
print(f'1.18.2 is {"1.18.2" in response[0]["game_versions"]}.')

# Download a Mod.
run(['curl', '-#', '-L', f'{response[0]["files"][0]["url"]}', '-o', f'{response[0]["files"][0]["filename"]}'])

# Search for a Mod.
params = {'query':'modmenu', 'index':'relevance'} 
search = get('https://api.modrinth.com/v2/search', params = params).json()
for x, _ in enumerate(search):
    print(f'Name: {search["hits"][x]["title"]} | {search["hits"][x]["slug"]}\n{search["hits"][x]["description"]}\n')