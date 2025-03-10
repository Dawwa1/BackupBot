import nextcord
import traceback
from nextcord.ext import commands, application_checks
from nextcord import SlashOption

import os
from time import strftime, localtime
from client.Backup.Backup import Backup as bkup



# literally just copied from discord.py docs


# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class Dropdown(nextcord.ui.Select):
    def __init__(self, available_backups: list[str], channel_backups: str): # takes in a list of file names of available backups

        # Set the options that will be presented inside the dropdown
        
        self.channel_backups = channel_backups
        
        options = []
        
        for backup in available_backups:
            options.append(nextcord.SelectOption(label=backup))

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Pick what backup you want to restore', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        
        backup = bkup(None, self.channel_backups)
        messages = backup.get_messages()
        
        for message in reversed(messages):
            embed = nextcord.Embed()
            
            author = nextcord.utils.get(interaction.guild.members, id=int(message["author"]))
            disp_name = author.display_name if author else "Unknown"    
            
            embed.set_author(name=disp_name, icon_url=author.avatar.url)
            
            time = strftime('%Y-%m-%d %H:%M:%S', localtime(float(message["created_at"])))
            embed.set_footer(text=time)
            
            message_content = message["content"]
            if len(message_content) > 1024:
                message_content1 = message_content[:1021] + ".." # goes to 1023 (1021 + 2 dots)
                message_content = message_content[1021:]
                embed.add_field(name="Content", value=message_content1)
                await interaction.channel.send(embed=embed)
                embed.clear_fields()
            
            # error if content > 1024 characters
            # will have to split it into multiple embeds
            embed.add_field(name="Content", value=message_content)
            
            await interaction.channel.send(embed=embed)


class DropdownView(nextcord.ui.View):
    def __init__(self, available_backups: list[str], channel_backups: str):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(available_backups=available_backups, channel_backups=channel_backups))


class Restore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @application_checks.has_permissions(manage_messages=True)
    @nextcord.slash_command(guild_ids=[1041433223487557682], description="Restores a backed up channel")
    async def restore(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel = SlashOption(description="Channel that you want to restore", required=False)
        ):
        if not channel:
            channel = interaction.channel
        
        try:
            
            guild_backups = f"backups/{interaction.guild.name}"
            channel_backups = f"{guild_backups}/{channel.name}"
            
            os.makedirs(guild_backups) if not os.path.exists(guild_backups) else None
            os.makedirs(channel_backups) if not os.path.exists(channel_backups) else None
            
            if len(os.listdir(channel_backups)) == 0:
                await interaction.send("No backups found for this channel", ephemeral=True)
                return

            backup = bkup(None, channel_backups)
            backup.get_messages()
            
            view = DropdownView(available_backups=os.listdir(channel_backups), channel_backups=channel_backups)
            
            await interaction.send("Pick a backup to restore", view=view, ephemeral=True)
            #print(messages[0])
            #await interaction.send("Restored messages", ephemeral=True)
            
        except IndexError:
            await interaction.send("No backups found for this channel", ephemeral=True)
            return
        except Exception:
            print(traceback.format_exc())
        
    

def setup(bot):
    bot.add_cog(Restore(bot))
