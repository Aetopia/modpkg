from argparse import ArgumentParser
from functions import profile, mod, search
from os import path, chdir

chdir(path.dirname(__file__))
parser = ArgumentParser(description = 'A Simple Mod Manager for Modrinth.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-install', '-i', action = "store", nargs = '*', metavar = ('<Profile>', 'Slugs'), help = 'Install mods for a specified profile.')
group.add_argument('-update', '-u', action = "store", nargs = 1, metavar = '<Profile>', help = 'Update all installed mods for a specfied profile.')
group.add_argument('-search', '-s', action =  "store", nargs = '*', metavar = 'Queries', help = 'Search for mods on Modrinth.')
group.add_argument('-profile', '-p', action = "store", nargs = 3, metavar = ('<Name>', '<Version>', '<Directory>'), help = 'Add a profile.')
args = parser.parse_args()

if args.search is not None:
    search(args.search)
elif args.install is not None:
    if len(args.install) != 0: 
        mod.install(args.install[1:], args.install[0])
elif args.update is not None:
    mod.update(args.update[0])       
elif args.profile is not None:
    profile.add(args.profile[0], args.profile[1], args.profile[2])    
else:
    parser.parse_args('-h'.split())    