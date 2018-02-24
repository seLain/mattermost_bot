## Notice

Please visit [attzonko/mattermost_bot](https://github.com/attzonko/mattermost_bot) if you are searching for stable version of `mattermost_bot` and any furthur support.

## Branches in this Repository

 * **master** : my version of mattermost_bot.
 * *others* : feature or bug-fix branches

## Running Tests

You will need a MatterMost server to run test cases. 

 * Create two user accounts for bots to login, ex. `driverbot` and `testbot`
 * Create a team, ex. `test-team`, and add `driverbot` and `testbot` into the team
 * Make sure the default public channel `off-topic` exists
 * Create a private channel (ex. `test`) in team `test-team`, and add `driverbot` and `testbot` into the private channel

Install `PyTest` in development environment.

```
pip install -U pytest
```

There are two test categories in `mattermost_bot\tests`: __unit_tests__ and __behavior_tests__. The __behavior_tests__ is done by interactions between a __DriverBot__ and a __TestBot__.

To run the __behavior_tests__, you have to configure `behavior_tests\bot_settings.py` and `behavior_tests\driver_settings.py`. Example configuration:

__driver_settings.py__:
```python
PLUGINS = [
]

BOT_URL = 'http://mymattermost.server/api/v4'
BOT_LOGIN = 'driverbot@mymail'
BOT_NAME = 'driverbot'
BOT_PASSWORD = 'password'
BOT_TEAM = 'test-team'  # this team name should be the same as in bot_settings
BOT_CHANNEL = 'off-topic' # default public channel name
BOT_PRIVATE_CHANNEL = 'test' # a private channel in BOT_TEAM
SSL_VERIFY = True
```

__bot_settings.py__:
```python
PLUGINS = [
]

BOT_URL = 'http://mymattermost.server/api/v4'
BOT_LOGIN = 'testbot@mymail'
BOT_NAME = 'testbot'
BOT_PASSWORD = 'password'
BOT_TEAM = 'test-team'  # this team name should be the same as in driver_settings
BOT_CHANNEL = 'off-topic'   # default public channel name
BOT_PRIVATE_CHANNEL = 'test' # a private channel in BOT_TEAM
SSL_VERIFY = True
```

Please notice that `BOT_URL`, `BOT_TEAM`, `BOT_CHANNEL`, and `BOT_PRIVATE_CHANNEL` must be the same in both setting files.

After the settings files are done, switch to root dir of mattermost, and run `pytest` to execute test cases.


## Add Local Settings and Plugins

If you would like to do settings and import local plugins without alter mattermost_bot.settings in Python site-packages, you can simply create a `local_settings.py` in your developement dir, and a `plugins` directory.

The `local_settings.py` looks like this :

```python
PLUGINS = [
    'plugins'
]

BOT_URL = 'http://mm.example.com/api/v3'
BOT_LOGIN = 'bot@example.com'
BOT_PASSWORD = None
BOT_TEAM = 'devops'
SSL_VERIFY = True
```

Then you can create your own Bot class and overwrite `__init__()` constructor :

```python
from mattermost_bot.bot import Bot, PluginsManager
from mattermost_bot.mattermost import MattermostClient
from mattermost_bot.dispatcher import MessageDispatcher
import local_settings

class LocalBot(Bot):

    def __init__(self):
        self._client = MattermostClient(
            local_settings.BOT_URL, local_settings.BOT_TEAM,
            local_settings.BOT_LOGIN, local_settings.BOT_PASSWORD,
            local_settings.SSL_VERIFY
            )
        self._plugins = PluginsManager(local_settings.PLUGINS)
        self._dispatcher = MessageDispatcher(self._client, self._plugins)

if __name__ == "__main__":
    LocalBot().run()
```

example for APIv4:

```python
from mattermost_bot.bot import Bot, PluginsManager
from mattermost_bot.mattermost_v4 import MattermostClientv4
from mattermost_bot.dispatcher import MessageDispatcher
import local_settings

class LocalBot(Bot):

    def __init__(self):
        self._client = MattermostClientv4(
            local_settings.BOT_URL, local_settings.BOT_TEAM,
            local_settings.BOT_LOGIN, local_settings.BOT_PASSWORD,
            local_settings.SSL_VERIFY
            )
        self._plugins = PluginsManager(local_settings.PLUGINS)
        self._dispatcher = MessageDispatcher(self._client, self._plugins)

if __name__ == "__main__":
    LocalBot().run()
```