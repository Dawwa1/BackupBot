from nextcord import Guild, TextChannel
from datetime import datetime
import zlib
import json
import os
import traceback
import urllib.request

from nextcord import Guild, TextChannel, Message

class Backup:
    # kinda shit because if restoring, data is gonna be None and idk how to handle errors :)
    def __init__(self, channel, backup_limit: int | None, path_to_backup: str | None):
        self.channel_backup = path_to_backup
        
        self.channel = channel
        self.backup_limit = backup_limit
        
        self.backup_folder = "backups"
            
    
    @staticmethod
    def get_image_in_message(message: Message):
        pic_ext = [".jpg", ".png", ".jpeg", '.gif']
        images = []
        for attachment in message.attachments:
            if attachment.filename in pic_ext:
                images.append(attachment.url)
                
        return images
    
    async def messages_as_json(self, channel: TextChannel, backup_limit):
        messages = []
        async for msg in channel.history(limit=backup_limit):
            if not msg.author.bot and not msg.embeds:
                data = {
                    "author": msg.author.id,
                    "content": msg.content,
                    "attachments": [attachment.url for attachment in msg.attachments],
                    "images": Backup.get_image_in_message(msg),
                    "created_at": msg.created_at.timestamp()
                }
                
                messages.append(data)
                
        return messages
        
    async def create_new(self, guild: Guild, channel: TextChannel) -> bool:
        try:
            data = await self.messages_as_json(channel, self.backup_limit)
            
            guild_backups = f"{self.backup_folder}/{guild.name}"
            channel_backups = f"{guild_backups}/{channel.name}"
            
            # checks if variables above are valid paths. creates them if not
            os.makedirs(guild_backups) if not os.path.exists(guild_backups) else None
            os.makedirs(channel_backups) if not os.path.exists(channel_backups) else None

            backup_path = f"{channel_backups}/{datetime.now().strftime('%m-%d_%H-%M-%S')}.backup"
            backup = zlib.compress(json.dumps(data).encode("utf-8"))
            
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