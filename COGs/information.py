import discord
from lists import bot_information
from paginator import Paginator
from discord import app_commands

class InfoCommands(app_commands.Group):
    def __init__(self, bot):
        super().__init__(name='info')
        self.bot = bot

    @app_commands.command(name='vanitybot', description='Get information about me!')
    async def vanitybot(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_purple(),
            title='VanityBot',
            description='**Created by fadingstorm**\n' + bot_information
        )
        embed.set_footer(text='Thank you for using VanityBot!')
        embed.set_thumbnail(url=self.bot.user.avatar)

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='user', description='Get information on a specific user.')
    @app_commands.describe(user='Specified user.')
    async def user(self, interaction: discord.Interaction, user: discord.User):
        if user.id == 766147685035933737:
            iscreator = True
        else:
            iscreator = False
        if user.bot is True:
            isbot = ':white_check_mark:'
        else:
            isbot = ':x:'
        
        embed = discord.Embed(
            color=discord.Color.blue(),
            title=user.name,
            description=f'ID: {user.id}'
        )
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name='Display Name', value=f'`{user.display_name}`', inline=False)
        embed.add_field(name='Created On', value=f'`{str(user.created_at)[:-13]}`', inline=False)
        embed.add_field(name='Joined Server', value=f'Joined **{interaction.guild}** at\n`{str(user.joined_at)[:-13]}`', inline=False)
        embed.add_field(name='Bot', value=isbot, inline=False)
        if iscreator:
            embed.description =f'ID: {user.id}\n' + f'**Creator of {self.bot.user.name}** :star:'

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='server', description='Get information on the current server.')
    async def server(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.blue(),
            title=interaction.guild,
            description=f"Server ID: {interaction.guild_id}",
        )
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.add_field(name='Server Created On', value=f'`{str(interaction.guild.created_at)[:-13]}`', inline=False)
        embed.add_field(name='Owner', value=f'`{interaction.guild.owner.name}`')
        embed.add_field(name='Roles', value=f'`{len(interaction.guild.roles)}`')
        embed.add_field(name='Members', value=f'`{interaction.guild.member_count}`')
        embed.add_field(name='Channels', value=f'Text: `{len(interaction.guild.text_channels)}`\nVoice: `{len(interaction.guild.voice_channels)}`')
        embed.add_field(name='Boosts', value=f'`{interaction.guild.premium_subscription_count}`')

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='serverroles', description='Get a list of the server\'s roles.')
    async def serverroles(self, interaction: discord.Interaction):
        embeds = []
        for roles in discord.utils.as_chunks(interaction.guild.roles, 10):
            embed = discord.Embed(
                color=discord.Color.blue(),
                title='Roles'
            )
            text = ''
            for i in roles:
                text += f'{i.mention} {len(i.members)}\n'
            embed.description = text.strip()
            embeds.append(embed)

        view = Paginator(embeds)
        await interaction.response.send_message(embed=view.initial, view=view)

async def setup(bot):
    bot.tree.add_command(InfoCommands(bot))