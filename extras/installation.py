from requests import get
from os import path
from hashlib import sha1
response = get('https://api.modrinth.com/v2/project/modmenu/version').json()


with open('profile.txt', 'w+') as old_file:
    old_file = old_file.read().splitlines()

if old_file == []:
    print('New Index...')

file = []
file += [f'modmenu / {response[0]["version_number"]} / {response[0]["files"][0]["hashes"]["sha512"]}']
with open('profile.txt', 'w+') as profile:
    profile.write('\n'.join(file))

def hash(file):
    algo = sha1()
    with open(file, 'rb') as file:
        algo.update(file.read())
    return algo.hexdigest()
print(hash(r'C:\Users\User\Documents\Projects\Package Manager\tests\modmenu-3.1.0.jar') == response[0]["files"][0]["hashes"]["sha1"])