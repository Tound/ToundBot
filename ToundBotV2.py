import asyncio
import sys
import os
import discord
from discord.ext import commands
import random

from soundboard import *

import ImageRecog
import database
from datetime import datetime
import json
import threading
import tournament
import gamesnight
from poll import *
from dotenv import load_dotenv

# ToundBot Version 2.14
# discord.py Version 1.4.1

intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix='!',intents=intents)  # discord.Client()

# Load Environment variables
load_dotenv()
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN')

# Global variables
mute = False
profanityLevel = 0
version = 2.14
livetime = ""
currentTournaments = []
currentGamesNights = []
# currentPoll = []
currentPoll = None

# ====================EXTRAS========================


def updateLeaderboard():

    for guild in client.guilds:
        print(len(guild.members))
        for member in guild.members:
            yield member
            # print(guild.name)
            print(member)

    # with open('leaderboard.json') as f:


def grammarCheck(message,level):
    if message != '' and level != 0:
        message = message.lower()
        messageContentList = message.split(' ')
        if int(level) == 1:
            with open('swearWords.txt') as f:
                for i in range(len(messageContentList)):
                    if messageContentList[i].rstrip() in f.read():
                        f.close()
                        return 1
                    else:
                        f.seek(0)
        elif int(level) == 2:
            with open('swearWords2.txt') as f:
                for i in range(len(messageContentList)):
                    if messageContentList[i].rstrip() in f.read():
                        f.close()
                        return 1
                    else:
                        f.seek(0)
        elif int(level) == 3:
            with open('swearWords3.txt') as f:
                for i in range(len(messageContentList)):
                    if messageContentList[i].rstrip() in f.read():
                        f.close()
                        return 1
                    else:
                        f.seek(0)
        else:
            pass
    else:
        pass


def checkForGoodWords(content):
    content = content.lower()
    messageContentList = content.split(' ')
    for i in range(len(messageContentList)):
        if messageContentList[i] in good_words:
            return 1


# ==================================================
# Bot ready in cmd
@client.event
async def on_ready():
    global livetime
    print('Logged in as')
    print('ToundBot')
    print('350611730918801418')
    print('READY!')
    livetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    updateLeaderboard()

good_words = ['lovely', 'gorgeous', 'cutie', 'ily']


@client.event
async def on_member_join(member):
    print('{} has joined, welcome!'.format(member))
    # updateLeaderBoard()


@client.event
async def on_member_remove(member):
    print(f'{member} has left :(')


########################### ON MESSAGE ###########################


@client.event
async def on_message(message):
    if message.author != client.user and not mute:
        channel = message.channel
        if profanityLevel != 0:
            if grammarCheck(message.content, profanityLevel) == 1:
                await channel.send('@{} Excuse me... please do not say that'.format(message.author))
                await message.delete()
                with open("log.txt", 'a+', encoding='utf-8') as f:
                    t = datetime.now()
                    currentTime = t.strftime("%d/%m/%Y %H:%M:%S")
                    f.write(f"{currentTime} - {message.author} wrote: {message.content} // Channel: {channel.name} // ACTION: Message removed \n")
                    f.close()
                return

        if message.author.id == 679176297469182003:
            await channel.send("OMFG MY HUSBAND")

        if message.content.startswith('Toundy'):
            await channel.send('YOU CALLED')

        elif message.content.startswith("!unmod ben"):
            await channel.send('Unmodding Skidaddlemynoodle in 5 seconds...')
            for i in range(4, 0, -1):
                await channel.send(i)
            await channel.send('Skidaddlemynoodle has returned to role: Regular')

        elif checkForGoodWords(message.content) == 1:
            await message.add_reaction('\U0001F970')
            await message.add_reaction('\U00002764')

    await client.process_commands(message)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    if amount > 10:
        await ctx.send("You can only clear a maximum of 10 messages!")
    else:
        await ctx.channel.purge(limit=amount)

########################### ABOUT THE BOT ###########################


@client.command()
async def botinfo(ctx):
    await ctx.send(f"Bot name: ToundBot \nVersion: {version} \nLive since: {livetime}")


@client.command()
async def about(ctx):
    await ctx.send(f"ToundBot is a Discord Chat Bot created by Tound for an experimental project. "
                   f"\nThe bot is written in Python and has various functions.")


@client.command()
async def functions(ctx):
    await ctx.send(f"ToundBot Functions include:\n")
    await ctx.send("Create polls, see !poll\n"
                   "Create votes, see !vote\n"
                   "Create Tournaments, see !tournament\n"
                   "More to be added...")


@client.command()
async def remove(ctx):
    await ctx.send("ToundBot is being shut down!")
    exit(1)


@client.command()
@commands.has_role("🤠 Moderator")
async def sleep(ctx):
    global mute
    if not mute:
        mute = True
        await ctx.send('z z Z Z Z')
    else:
        await ctx.send('ToundBot is already sleeping.')


@client.command()
@commands.has_role("🤠 Moderator")
async def wake(ctx):
    global mute
    if not mute:
        await ctx.send("Excuse me, I'm already awake...")
        mute = False
    else:
        await ctx.send('Wassup Gamers')
        mute = False


########################### VOICE FUNCTIONS ###########################

# Voice Channel
@client.command()
async def joinVC(ctx, vChannel):
    vc = findAbbrev(vChannel)

    await vc.connect()
    await ctx.send(f'ToundBot is joining {vChannel}')


@client.command()
async def leaveVC(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send('ToundBot is leaving VC')
    else:
        await ctx.send('ToundBot is not in a VC')


@client.command()
async def play(ctx, *args):
    sound = ' '.join(args)
    sound_path = get_sound_path(sound)

    if sound_path is None:
        await ctx.send("Error, Unknown sound")
        return -1
    else:
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_path))

    if ctx.voice_client is None:
        v_channel = ctx.author.voice.channel
        await v_channel.connect()

        ctx.voice_client.play(source, after=lambda e: print("Done"))
        while ctx.voice_client.is_playing():
            await asyncio.sleep(0.1)

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    else:
        ctx.voice_client.play(source, after=lambda e: print("Done"))
        while ctx.voice_client.is_playing():
            await asyncio.sleep(0.1)
        ctx.voice_client.stop()


@client.event
async def on_voice_state_update(member, before, after):
    if member.id == 141303058528337920 and member.voice is not None:
        await member.voice.channel.connect()
        sound_path = "sounds/tokyo-drift.mp3"
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_path))
        guild = client.get_guild(222837782664577026)
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)

        voice_client.play(source, after=lambda e: print("Done"))

        while voice_client.is_playing():
            await asyncio.sleep(0.1)

        voice_client.stop()
        await voice_client.disconnect()

    elif member.id == 345917415215071234 and member.voice is not None:
        await member.voice.channel.connect()
        sound_path = "sounds/pierre.mp3"
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_path))
        guild = client.get_guild(222837782664577026)
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)

        voice_client.play(source, after=lambda e: print("Done"))

        while voice_client.is_playing():
            await asyncio.sleep(0.1)

        voice_client.stop()
        await voice_client.disconnect()

    else:
        pass



# Extras
@client.command()
async def toundsgf(ctx):
    await ctx.send(file=discord.File('camila.jpg'))

@client.command()
async def complimentme(ctx):
    with open('compliments.txt') as f:
        lines = f.read().splitlines()
        await ctx.send(random.choice(lines))
        f.close

@client.command()
async def imbored(ctx):
    with open('compliments.txt') as f:
        lines = f.read().splitlines()
        await ctx.send(random.choice(lines))
        f.close


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Sort the arguments out please')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('No idea what that is boo x')
    else:
        print(error)


########################### IMAGE RECOGNITION ###########################
@client.command()
async def whatsthis(ctx, thing):
    await ctx.send('Hmmmm, I think that is a... hmmmm')
    try:
        # predictions, percentages = ImageRecog.imageRecog(thing)
        # for index in range(len(predictions)):
        #     percentages[index] = int(percentages[index])
        #     if percentages[index] != 0:
        #         await ctx.send(f"I'm {percentages[index]} % certain that's a {predictions[index]}")
        objects, confidence, personInfo = ImageRecog.imageRecog(thing)
        confidence = int(confidence*100)
        personString = ''
        if len(objects) > 1:
            string = ''
            for i in range(len(objects)):
                string = string + objects[i]
                string = string + ', '

            await ctx.send(f"I'm {confidence} % certain that this image contains a {string}")
        else:
            await ctx.send(f"I'm {confidence} % certain that's a {objects[0]}")

        if personInfo != []:
            if len(personInfo[0]) > 1:
                for i in range(len(personInfo[0])):
                    await ctx.send("Calculating genders")
            else:
                await ctx.send(f"I'm {personInfo[0][0]} % certain the person is a {personInfo[1][0]}")
    except:
        print(sys.exc_info()[0])
        await ctx.send("Oh snap, I need to learn that")


def findAbbrev(ch):
    if ch == 'general' or ch == 'g' or ch == '1':
        return client.get_channel(238374962262441985) #"🌌 GENERAL CHIT CHAT"
    elif ch == 'main' or ch == 'm' or ch == '2':
        return client.get_channel(279365748038696960) #"🌌 MAIN LOBBY"
    elif ch == 'squad goals' or ch == 'squad' or ch == 'sg':
        return client.get_channel(350613656356257792) #"🎮 Squad Goals"
    elif ch == 'duos':
        return client.get_channel(350613594162987020) #"🎮 Duos"
    else:
        return ch


def checkRole(author):
    for role in author.roles:
        if role.name == "🤠 Moderator":
            return True
    return False


#Drag all members from one VC to another
@client.command()
@commands.has_role(244969009076764673)
async def drag(ctx, ch1, ch2):
    role_ok = checkRole(ctx.author)
    if role_ok == True:
        channel1 = findAbbrev(ch1)
        channel2 = findAbbrev(ch2)
        if not (type(channel1) == discord.VoiceChannel and type(channel2) == discord.VoiceChannel):
            await ctx.send("Channel specified must be voice channels!")
            return -1

        if channel1 == channel2:
            await ctx.send("Members are already in the specified channel")
        else:
            await ctx.send(f"Moving all members from {channel1.name} to {channel2.name}")
            for member in channel1.members:
                await member.move_to(channel2)
    else:
        await ctx.send("Your role is not high enough for this command!")

#Helpme commands - move to json format?
@client.command()
async def helpme(ctx, thing):
    if thing == 'drag':
        await ctx.send("Command: *!drag* \n"
                       "Follow the command with the channel you are "
                       "dragging from followed by the channel that you "
                       "would like to drag to. You can use known abbreviations for channels too!")
    elif thing == 'whatsthis':
        await ctx.send("Command: *!whatsthis* \n"
                       "This command uses OpenCV for image recognition. "
                       "Follow !whatsthis with an image. E.g. !whatsthis apple.jpg")
    elif thing == 'toundsgf':
        await ctx.send("Command: *!toundsgf* \n"
                       "Pretty obvious isn't it. Yes! It is Tound's gf!")
    elif thing == 'complimentme':
        await ctx.send("Command: *!complimentme* \n"
                       "Spits out a gorgeous compliment to brighten your day!")
    elif thing == '':
        await ctx.send("Command: *Unknown* \n"
                       "Follow !help with a command name "
                       "that you would like to have help about")
    elif thing == 'poll':
        await ctx.send("Command: *!poll* \n"
                       "Use the !poll command to view poll results or create a new poll.\n"
                       "If a poll is open, this command will show the poll's current results.\n"
                       "To create a new poll use the 'new' keyword after the command.\n"
                       "If you only want 1 vote per user, add the 'once' tag after the word 'new'.\n"
                       "The layout of the command is as follows:\n"
                       "!poll new <optional once> <Question>, <Answer 1>, <Answer 2>, ...\n\n"

                       "Example: \n!poll new Am I Cool?, Yes, No\n"
                       "!poll new once Am I Cool?, Yes, No")
    else:
        await ctx.send("That variable name is unknown...")


@client.command()
@commands.has_role(244969009076764673)
async def setProfLevel(ctx, level):
    #role_ok = checkRole(ctx.author)
    #if role_ok != True:
    #    await ctx.send("Your role is not high enough for this command!")
    #    return

    global profanityLevel
    if int(level) == 0:
        await ctx.send("Profanity filter removed!")
        profanityLevel = level
    elif int(level) == 1:
        await ctx.send("Profanity level set: Level 1, all profanity will be removed!")
        profanityLevel = level
    elif int(level) == 2:
        await ctx.send("Profanity level set: Level 2, medium level only filter!")
        profanityLevel = level
    elif int(level) == 3:
        await ctx.send("Profanity level set: Level 3, severe swears only will be removed!")
        profanityLevel = level
    else:
        await ctx.send("Unknown profanity level; setting level to 0. Filter removed!")
        profanityLevel = 0

@client.command()
async def currentProfLevel(ctx):
    await ctx.send(f"Current profanity filter level: {profanityLevel}")

@client.command()
async def sr(ctx, *args):
    VC = client.get_channel()
    name = args[0]
    await ctx.send(f"Now playing {name} in {VC}")
    #search yt for vid

#Tournament
@client.command()
async def tournament(ctx, *args):
    global currentTournaments
    if len(args) == 0:
        if len(currentTournaments) == 0:
            currentTournaments = tournament()
        else:
            ctx.send("There is always a game night")
    else:
        if args[0] == "clear":
            if int(args[1]).isDigit():
                try:
                    currentTournaments.remove(int(args[1])-1)
                except IndexError:
                    ctx.send("Index out of bounds")
            elif args[1] == "all":
                currentTournaments = None
            else:
                ctx.send(f"Cannot clear {args[1]}")
        elif len(args) > 4:
            del args[4:] #truncate args
            newTournament = tournament.tournament(args)
            currentTournaments.append(newTournament)
            ctx.send(newTournament.getAnnouncement())
        else:
            newGamesNight = gamesnight.gamesnight(args)
            currentTournaments.append(newGamesNight)
            ctx.send(newGamesNight.getAnnouncement())

#Games Night
@client.command()
async def gamesnight(ctx, *args):
    global currentGamesNights
    if len(args) == 0:
        if len(currentGamesNights) == 0:
            await ctx.send("There are no Games Nights setup! \nTo create a Games Night use '!gamesnight' followed by variables such as: time, players and games")
        else:
            count = len(currentGamesNights)
            string = ''
            for i in currentGamesNights:
                string = string + f"{i+1}." + currentGamesNights[i].getAnnouncement() + "\n"
            await ctx.send(f"There are currently {count} Games nights open! \n " + string)

    else:
        if args[0] == "clear":
            if int(args[1]).isDigit():
                try:
                    currentGamesNights.remove(int(args[1])-1)
                except IndexError:
                    ctx.send("Index out of bounds")
            elif args[1] == "all":
                currentGamesNights = None
            else:
                ctx.send(f"Cannot clear {args[1]}")
        elif len(args) > 4:
            del args[4:] #truncate args
            newGamesNight = gamesnight.gamesnight(args)
            currentGamesNights.append(newGamesNight)
            await ctx.send(newGamesNight.getAnnouncement())
        else:
            newGamesNight = gamesnight.gamesnight(args)
            currentGamesNights.append(newGamesNight)
            await ctx.send(newGamesNight.getAnnouncement())

# Poll
@client.command()
async def poll(ctx,*args):
    global currentPoll
    print(args)
    if currentPoll is None: # If there is no poll
        # If the command has no arguments

        if args == ():
            await ctx.send("A poll is not open, you can learn how to create a poll by typing '!helpme poll'")

        # If the command has arguments
        #!poll new lMAOOOO, me, you
        elif len(args) > 1:
            if args[0] == "new":
                if args[1] == "once":
                    content_string = ' '.join(args[2:])
                    content_string = content_string.split(', ')
                    title = content_string[0]
                    track_voters = True
                    answers = content_string[1:]
                else:
                    content_string = ' '.join(args[1:])
                    content_string = content_string.split(', ')
                    title = content_string[0]
                    track_voters = False
                    answers = content_string[1:]

                currentPoll = Poll(title, track_voters, answers)
                #newPoll = poll(args)
                #currentPoll.append(newPoll)
                await ctx.send("Poll created")
                await ctx.send(currentPoll.results())

            else:
                await ctx.send("To create a new poll, the first argument must be 'new'!")

        else:
            await ctx.send("oof")

    elif args[0] == "end":
        if currentPoll is None:
            await ctx.send("There are no polls active currently, use the '!poll new' command to start a new poll!")
        else:
            await ctx.send("The poll has ended!")
            results = currentPoll.close()
            await ctx.send(results)
            del currentPoll
            currentPoll = None

    else:
        await ctx.send("The results of the current poll is as follows!")
        results = currentPoll.results()
        await ctx.send(results)


@client.command()
async def vote(ctx,*args):
    if currentPoll is not None:
        vote = ' '.join(args)
        err_code = currentPoll.vote(ctx.author,vote)
        if err_code == 1:
            await ctx.send(f"{ctx.author}, you have already voted - Vote disallowed")
        elif err_code == 0:
            await ctx.send(f"{ctx.author}, vote added")
            await ctx.send(currentPoll.results())
        elif err_code == -1:
            await ctx.send(f"{ctx.send}, voting option ({vote}) was not an option in the poll")
        else:
            await ctx.send("Unknown error with voting")
    else:
        await ctx.send(f"{ctx.author}, you silly sausage, there isn't a poll open!")

client.run(CLIENT_TOKEN)

#STUFF TO ADD
#Image recognition /
#im bored bot
#Split up commands
#Zombies calc
#Bday counter (how old)
#heads or tails
#beatboxer
#leaderboard
#sqldatabase
#drag command?              /
#soundboard?
#APIs?
#Spotify integration?
#Email for errors
#VIP?
#Help                       /
#Custom command
#Bad word severity          /
#Excel/text leaderboard
#Famous quotes
#Facts
#Post version               /
#Tournament
#Games night
#C++ GUI
#Env file for ID
#Licensing
#Bug report
#Refactor
#Poll
#Votes