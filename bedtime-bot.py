# bot.py
import discord as dis
import time 
import configparser
import asyncio 

from discord.ext import commands
from discord.ext.tasks import loop

from datetime import datetime
from pytz import timezone

config = configparser.ConfigParser()
config.read('options.ini')

token = config.get('GENERAL', 'discord_token')
guild_id = int(config.get('GENERAL', 'guild_id'))

starttime=time.time()

time_est = datetime.now(timezone('EST'))

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
	print('ready!')
	
@loop(seconds=1)	
async def initial_bedtime_kick():
	await bot.wait_until_ready()
	
	#get the id of the guild from the client 
	id = bot.get_guild(guild_id)

	#store a list of bedtimes 
	for option in config['BEDTIMES']:
		cur_time = time_est.now().hour
		#print(convert_time(cur_time))
		#cur_time = time_est.now().minute

		#check if the current hour is in the set bedtimes
		if config.getint('BEDTIMES',option) == cur_time:
			#get the member from a user name (string)
			victim_name = config.get('USERS',option)
			victim_member = dis.utils.get(id.members, name=victim_name)
			await victim_member.move_to(channel=None, reason=None)
			
			#search through the channels and if general found then display the message there
			for channel in victim_member.guild.channels:
					if channel.name == 'bot-spam':
						#await channel.send(victim_name + ', its beddy-bye time! 😱')	
						break	
								
def convert_time(cur_time):
	if cur_time > 12:
		afternoon = True
		cur_time -= 12
	else:
		afternoon = False
	if cur_time == 0:
		# Special case
		cur_time = 12
	return cur_time
	
#allow a member to change their bedtime 	
@bot.command(name='time')
async def change_time(ctx, bedtime: int):
	username = ctx.message.author.name
	for option in config['USERS']:
		if username == config.get('USERS',option):
			#print(username + ' is ' + option) 
			config.set('BEDTIMES', option , str(bedtime))
			# Writing to configuration file 'options.ini'
			with open('options.ini', 'w') as configfile:
				config.write(configfile)
			await ctx.send(username + ' , your new bedtime is: ' + str(bedtime))
			break
		else:
			continue
			
		
@bot.command(name='exit')
async def shutdown(ctx):
	await ctx.bot.logout()

					
@bot.event	
async def on_voice_state_update(member, before, after):
	id = bot.get_guild(guild_id)
	for option in config['BEDTIMES']:
		#check if the current hour is in the set bedtimes
		cur_time = time_est.now().hour
		#cur_time = time_est.now().minute
		if config.getint('BEDTIMES',option) == cur_time:	
			if after.channel is None:
				#get the member from a user name (string)
				victim_name = config.get('USERS',option)
				victim_member = dis.utils.get(id.members, name=victim_name)
				await victim_member.move_to(channel=None, reason=None)
				
				#search through the channels and if general found then display the message there
				for channel in victim_member.guild.channels:
						if channel.name == 'bot-spam':
							#await channel.send(victim_name + ', its beddy-bye time! 😱')
							break
							
			if before.channel is None and after.channel is not None:
				#get the member from a user name (string)
				victim_name = config.get('USERS',option)
				victim_member = dis.utils.get(id.members, name=victim_name)
				await victim_member.move_to(channel=None, reason=None)
				
				#search through the channels and if general found then display the message there
				for channel in victim_member.guild.channels:
						if channel.name == 'bot-spam':
							#await channel.send(victim_name + ', its beddy-bye time! 😱')
							break	

initial_bedtime_kick.start()
bot.run(token)	

