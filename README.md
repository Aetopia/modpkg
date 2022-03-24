# modpkg
A Simple Mod Manager for Modrinth.

## Aim
This is project aims to implement a simple mod manager for Modrinth API.          
Allows the user to update and install mods of their choice.

## Usage
#### Begin by creating a profile for a MC installation.
```
modpkg.py -p MyProfile 1.18.2 C:\Users\User\AppData\.minecraft\game\1.18.2
```
The same command can be used to update/overwrite an existing profile.

#### Install some mods.
```
modpkg.py -i MyProfile sodium lithium modmenu
```

#### Update all mods installed for a specific profile.
```
modpkg.py -u MyProfile
```
