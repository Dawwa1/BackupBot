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
            backup = bkup(channel, message_count, None)
            resp = await backup.create_new(interaction.guild, channel)
            if not resp:
                await interaction.response.send_message(f"Backup of {channel.mention} already exists", ephemeral=True)
            else:
                await interaction.response.send_message(f"Backup of {channel.mention} has been created", ephemeral=True)
                    
        except Exception:
            print(traceback.format_exc())
        
    

def setup(bot):
    bot.add_cog(Backup(bot))
