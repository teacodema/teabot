from setup.properties import *
from setup.actions import *


def init_check_membership(params):

	bot = params['bot']
	slash = params['slash']
	get = params['get']
	
	######################## CHECK NEWMEMBERSHIP PERIODE ########################
	@slash.slash(name="unm", guild_ids=[guildId],
		permissions={ guildId: slash_permissions({'founders'}, {'members', 'everyone'}) })
	async def update_new_members(ctx):
		try:
			if not is_founders(ctx):
				await ctx.send('❌ Missing Permissions', hidden=True)
				return
			await ctx.send('Updating ...', hidden=True)
			updatedMembers = await checkNewMemberRole(bot, get)
			msg = ''
			updatedMembersCount = len(updatedMembers)
			if updatedMembersCount:
				for member in updatedMembers:
					msg += f'{member} , '
			await ctx.send(f'{updatedMembersCount} updated members.\n{msg}', hidden=True)
		except Exception as ex:
			print('----- /update_new_members() -----')
			print(ex)
