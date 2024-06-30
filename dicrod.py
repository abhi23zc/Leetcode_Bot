import discord, requests, json
from discord.ext import commands
import schedule
import os, time

def task():

    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    api_data = ""

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True


    bot = commands.Bot(command_prefix='!', intents=intents)

    def getData():
        x = requests.get('http://127.0.0.1:5000/api/v1/')
    # print(x.json())
        data =  x.json()
        api_data = (f' Date: {data["date"]} \n Title: {data["title"]}\n url: {data["url"]} ')
        return api_data

    getData()

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')


    @bot.event
    async def on_message(message):

        if message.author == bot.user:
            return


        await message.channel.send(api_data or getData())

        await bot.process_commands(message)


    bot.run(TOKEN)

# Schedule the task every day at 8 PM
schedule.every().day.at("09:04").do(task)

print("Scheduler started, waiting for 8 PM to run the task...")

# schedule.run_all()
while True:
    schedule.run_pending()
    time.sleep(1)


