import nextcord
from nextcord.ext import commands

import os
import fnmatch

from dotenv import load_dotenv # type: ignore

load_dotenv()

client = commands.Bot(command_prefix='!', intents=nextcord.Intents.all())

# loads all cogs
folder = './commands'
file_ending = "*.py"
for path, subdirs, files in os.walk(folder):
    for name in files:
        if fnmatch.fnmatch(name, file_ending):
            path = os.path.join(path, name)[2:][:-3].replace("/", ".")
            try:
                client.load_extension(path)
                print(f"Loaded {path}")
            except nextcord.ext.commands.errors.NoEntryPointError as e:
                print(f"Error loading {path}: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}\nServers: {len(client.guilds)}\n--------')
    for i in client.guilds:
        print(f"{i.name}")
    
    
client.run(os.getenv("TOKEN"))
