from nextcord import Guild, TextChannel
from datetime import datetime
import zlib
import json
import os
import traceback

from nextcord import Guild, TextChannel

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