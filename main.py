import random
import lists
import settings
import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from APIs import anime_quotes, cats, coffees, dogs, ducks, nekos, quotes, trivias, waifu_stuff
from webscraping import anime_news, stock_check

logger = settings.logging.getLogger("bot")

INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=1124264065221541988&permissions=534723819584&scope=bot"

# this is literally only for the help command
def help_list(thing):
    string = ''
    for i in thing:
        string += str(f'`/{i}` ')
    return string


def run():

    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix='v!', intents=intents)
    bot.remove_command('help') # remove the default help command, it's ugly

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        logger.info(f"Guild ID: {bot.guilds[0].id}")
        #bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        print('The bot should be up and running.')

        await bot.tree.sync(guild=None)
    

   # Here are all the commands for the bot
    @bot.tree.command(name='help', description='Provides a list of all commands.')
    async def help(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_purple(),
            description='This bot has many fun commands for you to use!\n*Keep in mind that this bot uses slash commands.*',
            title=f'{bot.user.name}\'s commands!'
        )
        embed.add_field(name='Helpful Commands', value=lists.helpful_info + '\n' + help_list(lists.helpful), inline=False)
        embed.add_field(name='Random Commands', value=lists.random_info + '\n' + help_list(lists.random_commands), inline=False)
        embed.add_field(name='Image Commands', value=lists.image_info + '\n' + help_list(lists.image), inline=False)
        embed.add_field(name='Fun Commands', value=lists.fun_info + '\n' + help_list(lists.fun), inline=False)
        embed.add_field(name='Interaction Commands', value=lists.interactions_info + '\n' + help_list(lists.interactions), inline=False)
        embed.add_field(name='Anime Commands', value=help_list(lists.anime), inline=False)
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
        embed.set_footer(text='fadingstorm | creator')
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

    @bot.tree.command(name='cat', description='Sends a photo of a cat!')
    async def cat(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_gold(),
            title="Meow Meow! :cat:"
        )
        embed.set_image(url=cats.get_cat_url())
        embed.set_footer(text='Dogs or cats?')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='dog', description='Sends a photo of a dog!')
    async def dog(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_gold(),
            title="Woof Woof! :dog:"
        )
        embed.set_image(url=dogs.get_dog_url())
        embed.set_footer(text='Man\'s best friend')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='duck', description='Sends an image of a duck!')
    async def duck(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_gold(),
            title="Quack! :duck:"
        )
        embed.set_image(url=ducks.get_duck_img()[0])
        embed.set_footer(text=f'{ducks.get_duck_img()[1]}')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='neko', description='Sends an image of a neko!')
    async def neko(interaction: discord.Interaction):
        info = nekos.get_neko_img()
        embed = discord.Embed(
            color=discord.Color.pink(),
            title="Neko~"
        )
        embed.set_image(url=info[0])
        embed.set_footer(text=f'Artist: {info[1]}')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='coffee', description='Sends a random photo of coffee!')
    async def coffee(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_orange(),
            title="Coffee. :coffee:"
        )
        embed.set_image(url=coffees.get_coffee_img())
        embed.set_footer(text='Everyone needs it.')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='megumin', description='Sends a random photo of Megumin!')
    async def megumin(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.orange(),
            title="爆裂 :boom:"
        )
        embed.set_image(url=waifu_stuff.get_the_img('megumin'))
        embed.set_footer(text='Megumin')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='smug', description=':smirk:')
    async def smirk(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.dark_teal(),
            title=':smirk:'
        )
        embed.set_image(url=waifu_stuff.get_the_img('smirk'))
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='nom', description='nom nom nom')
    async def nom(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.yellow(),
            title='nom nom nom'
        )
        embed.set_image(url=waifu_stuff.get_the_img('nom'))
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='cringe', description='Cringe at something!')
    async def cringe(interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Color.random(),
            description=f'{interaction.user.mention} is cringing...'
        )
        embed.set_image(url=waifu_stuff.get_the_img('cringe'))
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='fate', description='Ask a yes or no question!')
    @app_commands.describe(question='Your yes or no question.')
    async def fate(interaction: discord.Interaction, question: str):
        embed = discord.Embed(
            color=discord.Color.random(),
            description=random.choice(lists.eight_ball_responses),
        )
        embed.set_author(name=question)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='slap', description='Slaps another user!')
    @app_commands.describe(user='The user you want to slap.')
    async def slap(interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.og_blurple(),
            description=f"**{interaction.user.mention} slapped {user.mention}!**"
        )
        embed.set_image(url=random.choice(lists.slap_gifs))
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='kiss', description='Kisses another user!')
    @app_commands.describe(user='The user you want to kiss~')
    async def kiss(interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"**{interaction.user.mention} kissed {user.mention}** :heart:"
        )
        embed.set_image(url=random.choice(lists.kiss_gifs))
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='bully', description='Bully another user!')
    @app_commands.describe(user='The user you want to bully!')
    async def bully(interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f"**{interaction.user.mention} is bullying {user.mention}!**"
        )
        embed.set_image(url=waifu_stuff.get_the_img('bully'))
        embed.set_footer(text='How mean!')
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='lick', description='Lick another user!')
    @app_commands.describe(user='The user you want to lick!')
    async def lick(interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.pink(),
            description=f"**{interaction.user.mention} licked {user.mention} :stuck_out_tongue:**"
        )
        embed.set_image(url=waifu_stuff.get_the_img('lick'))
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='highfive', description='High five another user!')
    @app_commands.describe(user='The user you want to high five!')
    async def highfive(interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.light_embed(),
            description=f"**{interaction.user.mention} high fived {user.mention} :hand_splayed:**"
        )
        embed.set_image(url=waifu_stuff.get_the_img('highfive'))
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='poke', description='Poke another user!')
    @app_commands.describe(user='Who do you want to poke?')
    async def poke(interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(
            color=discord.Color.random(),
            description=f"**{interaction.user.mention} :point_right: {user.mention}**"
        )
        embed.set_image(url=waifu_stuff.get_the_img('poke'))
        embed.set_footer(text='poke poke poke')
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
                    embed.set_footer(text=f'You chose: {answer.content.capitalize()}) {choices_dict[answer.content.capitalize()]}')
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