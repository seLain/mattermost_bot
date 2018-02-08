## Notice

This is a fork repository from [LPgenerator/mattermost_bot](https://github.com/LPgenerator/mattermost_bot) which is the original repo.

## Branches in this Repository

 * **master** : my version of mattermost_bot.
 * **integrated** : A branch to integrate all other branches in this repository (except **master**).
 * *others* : feature or bug-fix branches

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

