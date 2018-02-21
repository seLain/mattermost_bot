import time

from mattermost_bot.bot import Bot, PluginsManager
from mattermost_bot.mattermost_v4 import MattermostClientv4
from mattermost_bot.dispatcher import MessageDispatcher
import driver_settings, bot_settings

class DriverBot(Bot):

    def __init__(self):
        self._client = MattermostClientv4(
            driver_settings.BOT_URL, driver_settings.BOT_TEAM,
            driver_settings.BOT_LOGIN, driver_settings.BOT_PASSWORD,
            driver_settings.SSL_VERIFY
            )
        self._plugins = PluginsManager()
        self._plugins.init_plugins()
        self._dispatcher = MessageDispatcher(self._client, self._plugins)

class Driver(object):

	def __init__(self):
		self.bot = DriverBot()
		self.bot_username = driver_settings.BOT_NAME
		self.bot_userid = None
		self.testbot_username = bot_settings.BOT_NAME
		self.testbot_userid = None
		self.dm_chan = None	# direct message channel

	def start(self):
		self._retrieve_bot_user_ids()
		self._create_dm_channel()

	def _retrieve_bot_user_ids(self):
		# get bot user info
		self.users_info = self.bot._client.api.post('/users/usernames', 
							[driver_settings.BOT_NAME, bot_settings.BOT_NAME])
		# get user ids
		for user in self.users_info:
			if user['username'] == self.bot_username:
				self.bot_userid = user['id']
			elif user['username'] == self.testbot_username:
				self.testbot_userid = user['id']

	def _create_dm_channel(self):
		"""create direct channel and get id"""
		response = self.bot._client.api.post('/channels/direct', 
						[self.bot_userid, self.testbot_userid])
		self.dm_chan = response['id']

	def _format_message(self, msg, tobot=True, colon=True, space=True):
		colon = ':' if colon else ''
		space = ' ' if space else ''
		if tobot:
			msg = u'@{}{}{}{}'.format(self.testbot_username, colon, space, msg)
		return msg

	def _send_message_to_bot(self, channel, msg):
		self._start_ts = time.time()
		self.bot._client.channel_msg(channel, msg)

	def send_direct_message(self, msg, tobot=False, colon=True):
		msg = self._format_message(msg, tobot=tobot, colon=colon)
		self._send_message_to_bot(self.dm_chan, msg)

	def validate_bot_direct_message(self, match):
		posts = self.bot._client.api.get('/channels/%s/posts' % self.dm_chan)
		last_response = posts['posts'][posts['order'][0]]
		if match == last_response['message']:
			return
		else:
			raise AssertionError('expected to get message like "{}", but got nothing'.format(match))

	def wait_for_bot_online(self):
		self._wait_for_bot_presense(True)
		# sleep to allow bot connection to stabilize
		time.sleep(2)

	def _wait_for_bot_presense(self, online):
		for _ in range(10):
			time.sleep(2)
			if online and self._is_testbot_online():
				break
			if not online and not self._is_testbot_online():
				break
		else:
			raise AssertionError('test bot is still {}'.format('offline' if online else 'online'))

	# [ToDo] implement this method by checking via MM API
	def _is_testbot_online(self):
		# check by asking MM through API
		return True
