import sqlite3
import discord
from discord.ext import commands
import yaml
import requests
import vk_captchasolver as vc

conn = sqlite3.connect('xx.db', isolation_level=None, check_same_thread=False)
curs = conn.cursor()

bot = commands.Bot(command_prefix='!', case_sensitive=False)
bot.remove_command('help')

config = yaml.safe_load(open('config.yml', 'r').read())

@bot.command()
async def help(ctx):
    await ctx.send('!add — add URL to the claim list\n!remove — remove URL from the claim list\n!urls — claim list\n!resolve — parse VK group/page')

@bot.command()
async def add(ctx, url):
    if len(url) >= 5:
        for token in list(open('tokens.txt')):
            if not bool(len(curs.execute('SELECT * FROM `claimlist` WHERE `token` = ?', (token,)).fetchall())):
                try:
                    data = requests.get('https://api.vk.com/method/groups.create', params={
                        'access_token': token,
                        'title': 'test',
                        'type': 'group',
                        'v': 5.131,
                    }).json()
                    requests.get('https://api.vk.com/method/groups.edit', params={
                        'access_token': token,
                        'group_id': data['response']['id'],
                        'access': 1,
                        'v': 5.131,
                    }).json()
                    requests.get('https://api.vk.com/method/groups.leave', params={
                        'access_token': token,
                        'group_id': data['response']['id'],
                        'v': 5.131 
                    })
                    if data['response']:
                        curs.execute('INSERT INTO `claimlist` (`url`, `gid`, `token`) VALUES (?, ?, ?)', (url, data['response']['id'], token,))
                        await ctx.send(f'Successfully added **{url}** to the claim list | Group ID: `{data["response"]["id"]}`')
                        break
                except:
                    if data['error']:
                        if data['error']['error_code'] == 14:
                            data = requests.get('https://api.vk.com/method/groups.create', params={
                                'access_token': token,
                                'title': 'test',
                                'type': 'group',
                                'v': 5.131,
                                'captcha_sid': data['error']['captcha_sid'],
                                'captcha_key': vc.solve(sid=data['error']['captcha_sid'], s=1)
                            }).json()
                            requests.get('https://api.vk.com/method/groups.edit', params={
                                'access_token': token,
                                'group_id': data['response']['id'],
                                'access': 1,
                                'v': 5.131,
                            }).json()
                            requests.get('https://api.vk.com/method/groups.leave', params={
                                'access_token': token,
                                'group_id': data['response']['id'],
                                'v': 5.131 
                            })
                            if data['response']:
                                curs.execute('INSERT INTO `claimlist` (`url`, `gid`, `token`) VALUES (?, ?, ?)', (url, data['response']['id'], token,))
                                await ctx.send(f'Successfully added **{url}** to the claim list | Group ID: `{data["response"]["id"]}`')
                                break
                        elif data['error']['error_code'] == 5:
                            with open('tokens.txt', 'r') as file:
                                lines = file.readlines()
                            with open('tokens.txt', 'w') as file:
                                for line in lines:
                                    if line.strip('\n') != f'{token}':
                                        file.write(line)

@bot.command()
async def remove(ctx, url):
    if bool(len(curs.execute('SELECT * FROM `claimlist` WHERE `url` = ?', (url,)).fetchall())):
        curs.execute('DELETE FROM `claimlist` WHERE `url` = ?', (url,))
        await ctx.send(f'Successfully removed **{url}** from the claim list')

@bot.command()
async def urls(ctx):
    urls = []
    for row in curs.execute('SELECT `url` FROM `claimlist`').fetchall():
        for url in row:
            urls.append(url)
    await ctx.send(urls)

@bot.command()
async def resolve(ctx, url):
    data = requests.get('https://api.vk.com/method/utils.resolveScreenName', params={
        'access_token': config['vk_token'],
        'screen_name': url,
        'v': 5.131
    }).json()
    if data['response']['object_id']:
        if data['response']['type'] == 'user':
            x = requests.get('https://api.vk.com/method/users.get', params={
                'access_token': config['vk_token'],
                'user_ids': data['response']['object_id'],
                'fields': 'photo_200,domain',
                'v': 5.131
            }).json()
            embed = discord.Embed(title=f'{x["response"][0]["first_name"]} {x["response"][0]["last_name"]}', description=f'Information for [{url}](https://vk.com/{url})', color=33279)
            embed.set_thumbnail(url=f'{x["response"][0]["photo_200"]}')
            embed.add_field(name='URL', value=f'{x["response"][0]["domain"]}', inline=False)
            embed.add_field(name='User ID', value=f'{data["response"]["object_id"]}', inline=False)
            try:
                if x['response'][0]['deactivated'] == 'deleted':
                    embed.add_field(name='Type', value='Deleted', inline=False)
                elif x['response'][0]['deactivated'] == 'banned':
                    embed.add_field(name='Type', value='Banned', inline=False)
            except:
                if x['response'][0]['is_closed'] == 0:
                    embed.add_field(name='Type', value='Public', inline=False)
                elif x['response'][0]['is_closed'] == 1:
                    embed.add_field(name='Type', value='Private', inline=False)
            await ctx.send(embed=embed)
        elif data['response']['type'] == 'group':
            x = requests.get('https://api.vk.com/method/groups.getById', params={
                'access_token': config['vk_token'],
                'group_id': data['response']['object_id'],
                'v': 5.131
            }).json()
            embed = discord.Embed(title=f'{x["response"][0]["name"]}', description=f'Information for [{url}](https://vk.com/{url})', color=33279)
            embed.set_thumbnail(url=f'{x["response"][0]["photo_200"]}')
            embed.add_field(name='URL', value=f'{x["response"][0]["screen_name"]}', inline=False)
            embed.add_field(name="Group ID", value=f'{data["response"]["object_id"]}', inline=False)
            try:
                if x['response'][0]['deactivated'] == 'banned':
                    embed.add_field(name='Type', value='Banned', inline=False)
            except:
                if x['response'][0]['is_closed'] == 0:
                    embed.add_field(name='Type', value='Open', inline=False)
                elif x['response'][0]['is_closed'] == 1:
                    embed.add_field(name='Type', value='Closed', inline='False')
                elif x['response'][0]['is_closed'] == 2:
                    embed.add_field(name='Type', value='Private', inline=False)
            await ctx.send(embed=embed)

bot.run(config['dc_token'])
