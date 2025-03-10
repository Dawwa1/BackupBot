import nextcord
from nextcord.ext import commands, application_checks
from nextcord import SlashOption


class Clear(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @application_checks.has_permissions(manage_messages=True)
    @nextcord.slash_command(guild_ids=[1041433223487557682], description="Clear messages in a channel")
    async def clear(
        self,
        interaction: nextcord.Interaction,
        number: int = SlashOption(description="Number of messages that you want to delete", required=False)
        ):
        if not number:
            number = 1000
        try:
            message_count = [message async for message in interaction.channel.history(limit=number)]
            
            await interaction.send(f"Deleting {number if number < len(message_count) else len(message_count)}", ephemeral=True)
            await interaction.channel.purge(limit=number, bulk=True)
        except nextcord.Forbidden:
            await interaction.followup.send("I don't have the permission to delete messages", ephemeral=True)
        except nextcord.HTTPException:
            await interaction.followup.send("An error occurred while deleting messages", ephemeral=True)
        except nextcord.NotFound:
            pass
    

def setup(client):
    client.add_cog(Clear(client))