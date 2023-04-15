import discord
import os
from discord.ext import commands
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']
extensions = [
	"Commands.misc"
]

#All permission enabled.
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix = ["mj ", "Mj ", "MJ "], case_insensitive = True, intents = intents)

if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)

#Help command is in an embed.
class HelpCommand(commands.MinimalHelpCommand):
	async def send_pages(self):
		destination = self.get_destination()
		e = discord.Embed(color = discord.Color.random(), description = "**Mecha-Jimmy's Commands:**\n\n")
		e.set_thumbnail(url = bot.user.avatar_url)
		for page in self.paginator.pages:
			e.description += page
		await destination.send(embed=e)

bot.help_command = HelpCommand()

@bot.event
async def on_ready():
	await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "mj help"))
	print(f"\n\nLogged in as: {bot.user.name}#{bot.user.discriminator}\nID: {bot.user.id}\nVersion: {discord.__version__}\n")
	print("Everything's all ready to go!")

@bot.event
async def on_message(message):
	print("The message's content was", message.content)
	await bot.process_commands(message)

#Pings a website every so often to keep the program running indefinitely with UptimeRobot.
keep_alive()
bot.run(my_secret, bot = True)
