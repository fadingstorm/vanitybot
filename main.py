import random
import lists
import settings
import discord
import asyncio
import typing
from paginator import Paginator
from discord.ext import commands
from discord import app_commands
from APIs import anime_quotes, dadjokes, quotes, trivias
from webscraping import anime_news, lorem_ipsum, stock_check, songlyrics

logger = settings.logging.getLogger("bot")

INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=1124264065221541988&permissions=534723819584&scope=bot"


# this is literally only for the help command
def help_list(thing):
    string = ''
    for i in thing:
        string += str(f'`{i}`, ')
    string = string[:-2]
    return string


def run():

    intents = discord.Intents.all()

    # the bot doesn't actually use prefixes
    bot = commands.Bot(command_prefix='v!', intents=intents)
    bot.remove_command('help') # remove the default help command

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        logger.info(f'Guild ID: {bot.guilds[0].id}')
        #bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        print('The bot should be up and running.')

        await bot.load_extension("COGs.images")
        await bot.load_extension("COGs.interactions")
        await bot.load_extension("COGs.information")
        await bot.load_extension("COGs.text_commands")
        await bot.tree.sync(guild=None)

   # Here are all the commands for the bot
    @bot.tree.command(name='help', description='Provides a list of all commands.')
    async def help(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_purple(),
            description=f'A list of all commands available in this bot.\n*Keep in mind that this bot ONLY uses [slash commands](https://support.discord.com/hc/en-us/articles/1500000368501-Slash-Commands-FAQ).*',
            title=f'{bot.user.name}\'s Commands'
        )
        embed.add_field(name='Helpful Commands', value=lists.helpful_info + '\n' + lists.helpful, inline=False)
        embed.add_field(name='Info Commands', value=lists.infoOfInfo + '\n' + help_list(lists.info_commands), inline=False)
        embed.add_field(name='Miscellaneous Commands', value=lists.misc_info + '\n' + help_list(lists.misc_commands), inline=False)
        embed.add_field(name='Image Commands', value=lists.image_info + '\n' + help_list(lists.image), inline=False)
        embed.add_field(name='Fun Commands', value=lists.fun_info + '\n' + help_list(lists.fun), inline=False)
        embed.add_field(name='Interaction Commands', value=lists.interactions_info + '\n' + help_list(lists.interactions), inline=False)
        embed.add_field(name='Text Commands', value=lists.text_info + '\n' + help_list(lists.textCmds), inline=False)
        embed.add_field(name='Anime Commands', value=help_list(lists.anime), inline=False)

        # embed.set_footer(text='This bot was created by @fadingstorm')

        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name='invite', description='Provides an invite link for the bot!')
    async def invite(interaction: discord.Interaction):
        view = discord.ui.View()
        button = discord.ui.Button(label='Invite', url=INVITE_LINK)
        view.add_item(button)
        embed = discord.Embed(
            color=discord.Color.teal(),
            title='Thanks for using my bot!'
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @bot.tree.command(name='ping', description='Sends pong!')
    async def ping(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.blurple(),
            description=f"{round(bot.latency * 100000) / 100}ms {interaction.user.mention}",
            title="Pong!"
        )
        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name='quote', description='Sends a random quote!')
    async def quote(interaction: discord.Interaction):
        info = quotes.get_quote()
        embed = discord.Embed(
            color=discord.Color.darker_grey(),
            title=f'*{info[0]}*',
        )
        embed.set_footer(text=f'—{info[1]}')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='stockinfo', description='Get info on your favorite stock!')
    @app_commands.describe(symbol='The ticker symbol of the stock.')
    async def stockinfo(interaction: discord.Interaction, symbol: str):
        stock = stock_check.get_stock(symbol)
        if stock is False:
            embed = discord.Embed(
                color=discord.Color.brand_red(),
                title="Sorry, I'm not familiar with that stock.",
                description="*Make sure to enter the symbol correctly.*"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            name = stock[0]
            price = stock[1]
            changePrice = stock[2]
            changePercent = stock[3]
            if changePrice[0] == '+':
                goodbad = ':green_circle:'
            else:
                goodbad = ':red_circle:'
            embed = discord.Embed(
                color=discord.Color.light_grey(),
                title=f'{symbol.upper()} ({name})',
            )
            embed.set_footer(text="Data may be slightly delayed.")
            embed.add_field(name="Current Price:", value=price, inline=False)
            embed.add_field(name=f"Today's Change: {goodbad}", value=f"{changePrice} | {changePercent}", inline=False)
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='lipsum', description='Generates placeholder text for you!')
    @app_commands.describe(amount='The number of paragraphs generated.', length='The length of each paragraph.')
    async def lipsum(
        interaction : discord.Interaction,
        amount : typing.Literal[
            '1',
            '2',
            '3',
        ],
        length : typing.Literal[
            'short',
            'medium',
            'long'
        ]
    ):
        info = lorem_ipsum.get_lipsum(amount, length)
        embed = discord.Embed(
            color=discord.Color.light_grey(),
            title=info[0],
            description=info[1]
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='lyrics', description='Find the lyrics to your favorite song!')
    @app_commands.describe(song='The name of the song. Include the artist for more accuracy.')
    async def lyrics(interaction: discord.Interaction, song: str):
        info = songlyrics.get_lyrics(song)
        if info != 'Sorry, I couldn\'t find that song!':
            embeds = []
            for s in info[2]:
                embed = discord.Embed(title=info[0], description=f'By: {info[1]}', color=discord.Color.purple())
                embed.add_field(name='Lyrics', value=s)

                embeds.append(embed)
            
            view = Paginator(embeds)
            await interaction.response.send_message(embed=view.initial, view=view)
        
        else:
            embed = discord.Embed(
                title=info
            )
            embed.set_footer(text='Make sure to type the name correctly.')
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='8ball', description='Ask a yes or no question!')
    @app_commands.describe(question='Your yes or no question.')
    async def eight_ball(interaction: discord.Interaction, question: str):
        embed = discord.Embed(
            color=discord.Color.random(),
            description=random.choice(lists.eight_ball_responses),
        )
        embed.set_author(name=question)
        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name='dadjoke', description='Get a random dad joke!')
    async def dadjoke(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.random(),
            title=dadjokes.get_dadjoke(),
        )
        await interaction.response.send_message(embed=embed)    

    @bot.tree.command(name='animenews', description='Read up on the latest anime headlines!')
    async def animenews(interaction: discord.Interaction):
        stuff = anime_news.get_anime_news()

        # for the button (read more button)
        view = discord.ui.View()
        button = discord.ui.Button(label="Read More", url=stuff[2], style=discord.ButtonStyle.red)
        view.add_item(button)

        # for the actual embed content
        TITLE = stuff[0]
        DESC = stuff[1]
        embed = discord.Embed(
            color=discord.Color.dark_magenta(),
            title=TITLE,
            description=DESC
        )
        await interaction.response.send_message(embed=embed, view=view)

    @bot.tree.command(name='animequote', description='Sends a random anime quote!')
    async def animequote(interaction: discord.Interaction):
        QUOTE = anime_quotes.get_anime_quote()
        CHARACTER = QUOTE[0]
        TEXT = QUOTE[1]
        ANIME = QUOTE[2]
        embed = discord.Embed(
            color=discord.Color.dark_purple(),
            title=CHARACTER,
            description=f'*{TEXT}*'
        )
        embed.set_footer(text=f'{CHARACTER} | {ANIME}')
        await interaction.response.send_message(embed=embed)  
    
    # this command took the longest........
    # TRIVIAAA
    # the code is probably very inefficient
    @bot.tree.command(name='trivia', description='Asks a random trivia question!')
    async def trivia(interaction: discord.Interaction):
        channel = interaction.channel
        info = trivias.get_trivia()
        all_choices = [info['correct_answer']] + info['incorrect_answers']
        random.shuffle(all_choices)
        question_type = info['type']

        # matches each choice to ABCD (if it is a multiple choice)
        if question_type != 'boolean':
            choices_dict = {
                'A':all_choices[0],
                'B':all_choices[1],
                'C':all_choices[2],
                'D':all_choices[3],
            }

        # Creating the actual embed to ask the question
        embed = discord.Embed(
            color=discord.Color.blue(),
            description='Type the letter of the correct answer or true/false!'
        )
        embed.add_field(name='Category', value=info['category'])
        embed.add_field(name='Difficulty', value=info['difficulty'].upper())
        embed.add_field(name='Question', value=info['question'], inline=False)

        # I dont wanna type this out again
        correct_letter = list(choices_dict.keys())[list(choices_dict.values()).index(info['correct_answer'])]

        # if the question is a multiple choice, or a true/false, the bot will take answers differently
        # prolly could have made this more efficient but whatever
        if question_type == 'boolean':
            embed.add_field(name='True or False?', value='')
            await interaction.response.send_message(embed=embed)
            
            # now waiting for a response
            def check(m):
                return (m.content.capitalize() in ('True', 'False')) and m.channel == channel
            try:
                answer = await bot.wait_for('message', check=check, timeout=12)

                # when the answer is right
                if answer.content.capitalize() == info['correct_answer']:
                    embed.color = discord.Color.brand_green()
                    embed.description = f'{answer.author.mention} got it first!'
                    embed.add_field(name='Correct Answer\n', value=info['correct_answer'], inline=False)
                    embed.set_footer(text='Nice job!')
                    await interaction.edit_original_response(embed=embed)
                else: # when the answer is wrong
                    embed.color = discord.Color.brand_red()
                    embed.description = f'{answer.author.mention} got it wrong!'
                    embed.add_field(name='Correct Answer\n', value=info['correct_answer'], inline=False)
                    embed.set_footer(text=f'You chose: {answer.content.capitalize()}')
                    await interaction.edit_original_response(embed=embed)
            except asyncio.TimeoutError: # when the time is up
                embed.color = discord.Color.brand_red()
                embed.description = 'Time\'s up!'
                embed.add_field(name='Correct Answer\n', value=info['correct_answer'], inline=False)
                embed.set_footer(text='You get 12 seconds to answer.')
                await interaction.edit_original_response(embed=embed)       
        else:
            embed.add_field(
                name='Choices',
                value=f'**A)** {all_choices[0]}\n**B)** {all_choices[1]}\n**C)** {all_choices[2]}\n**D)** {all_choices[3]}'
            )
            await interaction.response.send_message(embed=embed)
        
            # now waiting for a response
            def check(m):
                return (m.content.capitalize() in ('A', 'B', 'C', 'D')) and m.channel == channel
            try:
                answer = await bot.wait_for('message', check=check, timeout=12)

                # when the answer is right
                if choices_dict[answer.content.capitalize()] == info['correct_answer']:
                    embed.color = discord.Color.brand_green()
                    embed.description = f'{answer.author.mention} got it first!'
                    embed.add_field(name='Correct Answer\n', value=correct_letter + '\n' + info['correct_answer'], inline=False)
                    embed.set_footer(text='Nice job!')
                    await interaction.edit_original_response(embed=embed)
                else: # when the answer is wrong
                    embed.color = discord.Color.brand_red()
                    embed.description = f'{answer.author.mention} got it wrong!'
                    embed.add_field(name='Correct Answer', value=correct_letter + '\n' + info['correct_answer'], inline=False)
                    embed.set_footer(text=f'You chose: {choices_dict[answer.content.capitalize()]}')
                    await interaction.edit_original_response(embed=embed)
            except asyncio.TimeoutError: # when the time is up
                embed.color = discord.Color.brand_red()
                embed.description = 'Time\'s up!'
                embed.add_field(name='Correct Answer', value=correct_letter + '\n' + info['correct_answer'], inline=False)
                embed.set_footer(text='You get 12 seconds to answer.')
                await interaction.edit_original_response(embed=embed)


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()