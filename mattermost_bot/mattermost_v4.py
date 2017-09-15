import json
import logging
import ssl
import time

import requests
import websocket
import websocket._exceptions

from mattermost_bot.mattermost import MattermostClient, MattermostAPI

logger = logging.getLogger(__name__)

class MattermostAPIv4(MattermostAPI):

    def login(self, team, account, password):
        props = {'login_id': account, 'password': password}
        response =requests.post(
            self.url + '/users/login',
            data = json.dumps(props),
            verify=self.ssl_verify)
        if response.status_code == 200:
            self.token = response.headers["Token"]
            self.user = json.loads(response.text)
            return self.user
        else:
            response.raise_for_status()

    def create_post(self, user_id, channel_id, message, files=None, pid=""):
        create_at = int(time.time() * 1000)
        return self.post(
                    '/posts',
                    {
                        'channel_id': channel_id,
                        'message': message,
                        'filenames': files or [],
                        'root_id': pid,
                    })

    def channel(self, channel_id):
        channel = {'channel': self.get('/channels/%s' % channel_id)}
        return channel

class MattermostClientv4(MattermostClient):

    def __init__(self, url, team, email, password, ssl_verify=True, login=1):
        self.users = {}
        self.channels = {}
        self.mentions = {}
        self.api = MattermostAPIv4(url, ssl_verify)
        self.user = None
        self.info = None
        self.websocket = None
        self.email = None
        self.team = team
        self.email = email
        self.password = password

        if login:
            self.login(team, email, password)

    def connect_websocket(self):
        host = self.api.url.replace('http', 'ws').replace('https', 'wss')
        url = host + '/websocket'
        self._connect_websocket(url, cookie_name='MMAUTHTOKEN')
        return self.websocket.getstatus() == 101
