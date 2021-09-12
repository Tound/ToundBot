import sys
import os
import discord
from discord.ext import commands
import random

import ImageRecog
import database
from datetime import datetime
import json
import threading
import tournament
import gamesnight
from poll import *
from dotenv import load_dotenv



#ToundBot Version 2.11
#discord.py Version 1.4.1

client = commands.Bot(command_prefix='!')  # discord.Client()

#Load Environment variables
load_dotenv()
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN')

#Global variables
mute = False
profanityLevel = 0
version = 2.12
livetime = ""
currentTournaments = []
currentGamesNights = []
#currentPoll = []
currentPoll = None

# ====================EXTRAS========================
def updateLeaderboard():

    for guild in client.guilds:
        print(len(guild.members))
        for member in guild.members:
            yield member
            #print(guild.name)
            print(member)

    #with open('leaderboard.json') as f:

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
    #updateLeaderBoard()

@client.event
async def on_member_remove(member):
    print(f'{member} has left :(')

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

        elif message.content.startswith('remove'):
            await channel.send('ToundBot shutting down')
            exit()

        elif message.content.startswith("!unmod ben"):
            await channel.send('Unmodding Skidaddlemynoodle in 5 seconds...')
            for i in range(4, 0, -1):
                await channel.send(i)
            await channel.send('Skidaddlemynoodle has returned to role: Regular')

        elif checkForGoodWords(message.content) == 1:
            await message.add_reaction('\U0001F970')
            await message.add_reaction('\U00002764')

        elif message.content.startswith('!delmessages'):
            content = message.content.split(' ')
            if len(content) > 2:
                await channel.send('{} invalid use of command; 1 arg required'.format(message.author))
                return
            channelMessages = await channel.history(limit=int(content[1]))
            for i in range(len(channelMessages)):
                await message.delete(channelMessages[i])
            await channel.send('{} messages deleted'.format(int(content[1])))
    await client.process_commands(message)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    if amount > 10:
        await ctx.send("You can only clear a maximum of 10 messages!")
    else:
        await ctx.channel.purge(limit=amount)

@client.command()
async def botinfo(ctx):
    await ctx.send(f"Bot name: ToundBot \nVersion: {version} \nLive since: {livetime}")

@client.command()
async def about(ctx):
    await ctx.send(f"ToundBot is a Discord Chat Bot created by Tound for an experimental project. "
                   f"\n The bot is written in Python and has various functions.")

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


# Voice Channel
@client.command()
async def joinVC(ctx, vChannel):
    VC = findAbbrev(vChannel)

    await VC.connect()
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("toff.mp3"))
    source.volume = 5
    ctx.voice_client.play(source, after=lambda e: print("Done"))
    await ctx.send(f'ToundBot is joining {vChannel}')
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()

@client.command()
async def leaveVC(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send('ToundBot is leaving VC')

@client.command()
async def disconnect(ctx):
    if client.is_connected():
        client.disconnect
    else:
        await ctx.send('ToundBot aint even in a damn VC...')

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
    if ch == 'general':
        return client.get_channel(238374962262441985) #"🌌 GENERAL CHIT CHAT"
    elif ch == 'main':
        return client.get_channel(279365748038696960) #"🌌 MAIN LOBBY"
    elif ch == 'squad goals' or 'squad' or 'sg':
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
@commands.has_role("324294790609108992")
async def drag(ctx, ch1, ch2):
    role_ok = checkRole(ctx.author)
    if role_ok == True:
        channel1 = findAbbrev(ch1)
        channel2 = findAbbrev(ch2)
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
    else:
        await ctx.send("That variable name is unknown...")


@client.command()
async def setProfLevel(ctx, level):
    role_ok = checkRole(ctx.author)
    if role_ok != True:
        await ctx.send("Your role is not high enough for this command!")
        return

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
    if currentPoll != None: # If there is no poll
        # If the command has no arguments
        if len(args) == 0:
            if len(currentPoll) == 0:
                await ctx.send("There are no polls active currently, use the '!poll new' command to start a new poll!")
            else:
                results = currentPoll.results()
                await ctx.send(results)

        # If the command has arguments
        elif len(args) > 2:
            if len(currentPoll) == 0:
                if args[0] == "new":
                    newPoll = poll(args)
                    currentPoll.append(newPoll)
                    await ctx.send("Poll created")
            else:
                await ctx.send("There are no polls active currently, use the '!poll new' command to start a new poll!")

        elif args[0] == "end":
            if len(currentPoll) == 0:
                await ctx.send("There are no polls active currently, use the '!poll new' command to start a new poll!")
            else:
                results = currentPoll.close()
                await ctx.send(results)
                currentPoll = None
        else:
            await ctx.send("oof")
    else:
        await ctx.send("The results of the current poll is as follows!")
        results = currentPoll.results()
        await ctx.send(results)

@client.command()
async def vote(ctx,vote):
    if len(currentPoll) != 0:
        if vote in currentPoll[0].getChoices():
            currentPoll[0].vote(vote)
            results = currentPoll[0].results()
            await ctx.send(results)
        else:
            currentPoll[0].addChoice(vote)
            await ctx.send(f"{vote} added into possible choices!")
            results = currentPoll[0].results()
            await ctx.send(results)
    else:
        await ctx.send("There are no polls active currently, use the '!poll new' command to start a new poll!")

client.run(CLIENT_TOKEN)

#STUFF TO ADD
#Image recognition
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