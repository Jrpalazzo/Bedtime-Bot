# bot.py
import discord as dis
import time 
import configparser

from discord.ext import commands
from datetime import datetime
from pytz import timezone

config = configparser.ConfigParser()
config.read('options.ini')

token = config.get('GENERAL', 'discord_token')
guild_id = int(config.get('GENERAL', 'guild_id'))

time_est = datetime.now(timezone('EST'))

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
	print('ready!')
	await bot.wait_until_ready()

	#get the id of the guild from the client 
	id = bot.get_guild(guild_id)

	#store a list of bedtimes 

	for option in config['BEDTIMES']:
		cur_time = time_est.now().hour

		#check if the current hour is in the set bedtimes
		if config.getint('BEDTIMES',option) == detect_time(cur_time):
			#get the member from a user name (string)
			victim_name = config.get('USERS',option)
			victim_member = dis.utils.get(id.members, name=victim_name)
			await victim_member.move_to(channel=None, reason=None)
			
			#search through the channels and if general found then display the message there
			for channel in victim_member.guild.channels:
					if channel.name == 'general':
						await channel.send(victim_name + ', it\'s beddy-bye time! 😱')
		
def detect_time(cur_time):
	current = 0
	while True:
		time.sleep(5)
		if cur_time != current:
			current = cur_time
			break
			
	return current

@bot.command(name='exit')
async def shutdown(ctx):
	await ctx.bot.logout()

					
@bot.event	
async def on_voice_state_update(member, before, after):
	id = bot.get_guild(guild_id)

	for option in config['BEDTIMES']:
		#check if the current hour is in the set bedtimes
		cur_time = time_est.now().hour
		if config.getint('BEDTIMES',option) == cur_time:	
			if after.channel is None:
				#get the member from a user name (string)
				victim_name = config.get('USERS',option)
				victim_member = dis.utils.get(id.members, name=victim_name)
				await victim_member.move_to(channel=None, reason=None)
				
				#search through the channels and if general found then display the message there
				for channel in victim_member.guild.channels:
						if channel.name == 'general':
							await channel.send(victim_name + ', it\'s beddy-bye time! 😱')
							
			if before.channel is None and after.channel is not None:
				#get the member from a user name (string)
				victim_name = config.get('USERS',option)
				victim_member = dis.utils.get(id.members, name=victim_name)
				await victim_member.move_to(channel=None, reason=None)
				
				#search through the channels and if general found then display the message there
				for channel in victim_member.guild.channels:
						if channel.name == 'general':
							await channel.send(victim_name + ', it\'s beddy-bye time! 😱')
								
bot.run(token)			


