
from imports.actions.common import *
from imports.data_common.slash_commands_permissions import *

def init_slash_commands_bot(params):

	bot = params['bot']
	discord = params['discord']
	commands = params['commands']

	@bot.slash_command(name="teabot")
	async def teabot(inter):
		pass

	states = ["online", "dnd", "idle", "offline", "streaming"]
	discord_states = [ discord.Status.online, discord.Status.dnd, discord.Status.idle, discord.Status.offline, discord.Status.streaming]
	activity_types = ["watching", "listening", "playing", "streaming", "competing"]
	discord_activity_types = [discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.playing, discord.ActivityType.streaming, discord.ActivityType.competing]

	@teabot.sub_command(name = "activity")
	async def tc_bot_activity(interaction, status=commands.Param(choices=states), activity_type=commands.Param(choices=activity_types), name = None):
		"""
		Update bot activity & status
		Parameters
		----------
		status: status options list
		activity_type: activity options list
		name: value of the activity
		"""
		try:
			status = discord_states[states.index(status)]
			if name == None:
				name = "🌐 teacode.ma ☕"
			activity = discord.Activity(type = discord_activity_types[activity_types.index(activity_type)], name=name)
			await bot.change_presence(status=status, activity=activity)
		except Exception as ex:
			print('----- /tc_bot_activity() -----')
			print(ex)
			await log_exception(ex, '/tc_bot_activity', interaction)

	@teabot.sub_command(name = "list-commands")
	async def tc_list_commands(interaction):
		"""
		List all / commands
		Parameters
		----------
		"""
		try:
			member = interaction.author
			for cmds_list in slash_commands_permissions:
				embed = discord.Embed(title=f'Bot Commands / Permission : {cmds_list}', description="", color=member.color)
				embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.display_avatar)
				embed.set_thumbnail(url=member.display_avatar)
				for cmd_name in slash_commands_permissions[cmds_list]:
					slash_cmd = bot.get_slash_command(cmd_name)
					if slash_cmd:
						_name = slash_cmd.name
						if slash_cmd.parent:
							_name = f'{slash_cmd.parent.name} {_name}'
						embed.add_field(name=_name, value=slash_cmd.body.description, inline=True)
				embed.set_footer(text=f"🌐 Visit teacode.ma")
				await interaction.send(embed=embed, ephemeral=True)
		except Exception as ex:
			print('----- /tc_list_commands() -----')
			print(ex)
			await log_exception(ex, '/tc_list_commands', interaction)

	@teabot.sub_command(name = "bot-reacts")
	async def tc_bot_react(interaction, msg_id, emojis, remove:int=0, member: discord.Member = None):
		"""
		Add/Remove reaction to/from msg - ,
		Parameters
		----------
		msg_id: Message ID
		emojis: Server existing emojis separated by , or space
		remove: Remove the reaction - enter 1 to activate (default 0)
		member: Member to remove reactions for (remove param should be == 1)
		"""
		try:
			msg = await interaction.channel.fetch_message(msg_id)
			emojis = split_str(emojis)
			for e in emojis:
				try:
					if remove:
						if member: await msg.remove_reaction(e, member)
						else: await msg.clear_reaction(e)
					else: await msg.add_reaction(e)
				except Exception as ex:
					print('---------- /tc_bot_react()/loop --------')
					print(ex)
					pass
		except Exception as ex:
			print('---------- /tc_bot_react() --------')
			print(ex)
			await log_exception(ex, '/tc_bot_react', interaction)
			