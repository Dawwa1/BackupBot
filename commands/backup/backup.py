import nextcord
import traceback
from nextcord.ext import commands, application_checks
from nextcord import SlashOption

from client.Backup.Backup import Backup as bkup


class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @application_checks.has_permissions(manage_messages=True)
    @nextcord.slash_command(guild_ids=[1041433223487557682], description="Backs up a channel")
    async def backup(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel = SlashOption(description="Channel that you want to backup", required=False),
        message_count: int = SlashOption(description="Number of messages that you want to backup", required=False, default=50)
        ):
        if not channel:
            channel = interaction.channel
        
        try:
            messages = []
            async for msg in channel.history(limit=message_count):
                msg: nextcord.Message = msg
                
                if not msg.author.bot and not msg.embeds:
                    data = {
                        "author": msg.author.id,
                        "content": msg.content,
                        "attachments": [attachment.url for attachment in msg.attachments],
                        "created_at": msg.created_at.timestamp()
                    }
                    
                    messages.append(data)
                    
            backup = bkup(messages, None)
            resp = await backup.create_new(interaction.guild, channel)
            if not resp:
                await interaction.response.send_message(f"Backup of {channel.mention} already exists", ephemeral=True)
            else:
                await interaction.response.send_message(f"Backup of {channel.mention} has been created\n{len(messages)} messages backed up.", ephemeral=True)
                    
        except Exception:
            print(traceback.format_exc())
        
    

def setup(bot):
    bot.add_cog(Backup(bot))
