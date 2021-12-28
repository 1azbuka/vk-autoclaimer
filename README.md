## VK Autoclaimer
A little project that allows you to autoclaim any VK URL you want (4lulz)

### Features
* groups/profiles parser (name, url, uid/gid, type, etc.)
* fast asynchronous autoclaimer (webhook logs, auto group creation with captcha solver)

### Prerequisites
[Discord](https://discord.com/)\
Tested on [Python 3.9.7](https://www.python.org/ftp/python/3.9.7) with **add to path** button selected along with pip.
```py
requests
pyyaml
discord
vk_captchasolver
```

### Usage & Installation
Make sure to do step-by-step again if things don't work out.
1. Install [Python 3.9.7](https://www.python.org/ftp/python/3.9.7).
2. Open a command prompt and install modules that are required:
   ```
   pip install requests pyyaml discord vk_captchasolver
   ```
3. Generate VK Admin tokens with offline & groups scopes:
   ```
   https://oauth.vk.com/authorize?client_id=6121396&scope=327680&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1
   ```
4. Open "config.yml" file with any text editor and paste your VK token:
   ```py
   vk_token: token # make sure that you're using a token that isn't being used by autoclaimer
   ```
5. Put your VK tokens (to be used by autoclaimer) in the "tokens.txt" file, separated with newlines:
   ```
   token1
   token2
   token3
   token4
   ```
6. Install [Discord](https://discord.org) and create a server.
7. Create a [Discord bot](https://discord.com/developers/applications) and put his token in the "config.yml" file:
   ```py
   dc_token: token
   ```
8. Add a Discord bot on your server, create a webhook and paste it into "config.yml" file:
   ```py
   webhook: url
   ```
7. Run the bot.py & claimer.py.
8. Type "!help" to see bot commands.

## FAQ
By the way, to inspect the SQL file that will contain most of your actions—you can use [SQLite browser](https://sqlitebrowser.org/dl/); however, it is not really needed, the claimer has initially been designed to work remotely (that's why Discord support exists), for example on a VPS. Although with this app, you can claim an URL for an already existing group (add/replace gid), that may bypass a limit from VK, which is related to group creation (ex. too many actions)

>No module named...


Repeat all pip-related steps.

>I am getting too many request error.

Well, you shouldn't even if you're using the same tokens on everything. So replace them with fresh ones which are not repeating themself.

>I've got a claim, but I receive nothing in discord.


Make sure that webhook are in good standing. You can also follow this guide if you don't understand what you are doing at all — [https://discordpy.readthedocs.io/en/stable/discord.html](https://discordpy.readthedocs.io/en/stable/discord.html)


>My accounts were banned because of this app!

There is a risk that **ALL** of your accounts will be banned since this type of script are forbidden by the VK ToS, which is, by the way, are not include any rules related to claimers, but VK Support doesn't care at all and will ban your account for cybersquatting or just because they can. Even if you change your own URLs, you're in the danger zone (that's the original point of the app, yeah). (ex. 8.6)

>The Site Administration does not bear liability for the User’s 
breach of these Terms and reserves the right, at its own discretion as 
well as upon receipt of information from other Users or third parties on
 the User’s breach of these Terms, to modify (moderate), block or remove
 any information published by the User in breach of the prohibitions set
 by these Terms, suspend, limit or terminate the User’s access to all or
 any sections or services of the Site at any time for any reason or 
without explaining the reason, with or without advance notice. The Site 
Administration reserves the right to remove the User’s personal page 
and/or suspend, limit or terminate the User’s access to any of the Site 
services, if the Site Administration believes that the User poses a 
threat to the Site and/or its Users. Along with the stated in the 
paragraph above the Site Administration has the right to block and/or 
remove API Applications, limit the User's access to API Applications, 
websites, third-party applications, other third-party resources, block 
and/or remove links to them, in case the Site Administration has a 
reason to believe that such API Applications, websites, third-party 
applications, and other third-party resources pose or may pose a threat 
to the normal operation of the Site and its Users. The Site 
Administration implements the measures described above in accordance 
with applicable law and does not bear liability for any negative 
consequences of such measures for the User or third parties. 
