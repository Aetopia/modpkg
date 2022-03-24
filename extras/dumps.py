from requests import get
from json import dumps

params = {'query':'modmenu', 'index':'relevance'} 
search = get('https://api.modrinth.com/v2/search', params = params).json()
with open('results.json', 'w') as file:
    file.write(dumps(search, indent = 4))

response = get('https://api.modrinth.com/v2/project/modmenu/version').json()
with open('version.json', 'w') as file:
    file.write(dumps(response, indent = 4))    