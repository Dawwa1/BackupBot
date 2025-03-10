from nextcord import Guild, TextChannel
from datetime import datetime
import zlib
import json
import os
import traceback

from nextcord import Guild, TextChannel

"""

Figure out a good way to organize all file-handling code in a class
to both backup and restore messages.

Idea 1:
    - single backup class that handles only backups, so if you are restoring a backup, you will need to
    read the file and then pass the data to the backup function to get the messages.
    
    Problems:
        NOT ANYMORE- not very efficient, all libraries to restore messages are already here but I have to also import them in the restore command file.
        NOT ANYMORE- checking if backup exists doesn't work

"""

class Backup:
    # kinda shit because if restoring, data is gonna be None and idk how to handle errors :)
    def __init__(self, data: bytes | list | None, path_to_backup: str | None):
        self.data = data
        self.channel_backup = path_to_backup
        
        self.backup_folder = "backups"
        
    async def create_new(self, guild: Guild, channel: TextChannel) -> bool:
        try:
            
            guild_backups = f"{self.backup_folder}/{guild.name}"
            channel_backups = f"{guild_backups}/{channel.name}"
            
            # checks if variables above are valid paths. creates them if not
            os.makedirs(guild_backups) if not os.path.exists(guild_backups) else None
            os.makedirs(channel_backups) if not os.path.exists(channel_backups) else None

            backup_path = f"{channel_backups}/{datetime.now().strftime('%m-%d_%H-%M-%S')}.backup"
            backup = zlib.compress(json.dumps(self.data).encode("utf-8"))
            
            # checks if same backup exists (checks only last backup)
            if len(os.listdir(channel_backups)) > 0:
                for root, dirs, files in os.walk(channel_backups):
                    with open(f"{channel_backups}/{files[-1]}", "rb") as f:
                        data = f.read()
                        if data == backup:
                            return False
            
            with open(backup_path, "wb") as f:
                f.write(backup)
                
            return True
            
        except Exception:
            print(traceback.format_exc())
            return False
        
    def get_messages(self) -> list:
        try:
            if len(os.listdir(self.channel_backup)) == 0:
                return ValueError("No backups found")

            
            files = os.listdir(self.channel_backup)
            paths = [os.path.join(self.channel_backup, basename) for basename in files]
            
            with open(paths[-1], "rb") as f:
                data = f.read()
                messages = json.loads(zlib.decompress(data).decode("utf-8"))
                
            return messages
            
        except Exception:
            print(traceback.format_exc())