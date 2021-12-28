import sqlite3
import asyncio
import aiohttp
import webhook

conn = sqlite3.connect('xx.db', isolation_level=None, check_same_thread=False)
curs = conn.cursor()

async def claim(session, url, gid, token, **kwargs):
    resp = await session.request('GET', url=f'https://api.vk.com/method/utils.checkScreenName?screen_name={url}&access_token={token}&v=5.131', **kwargs)
    data = await resp.json()
    print(data)
    try:
        if data['response']['status'] == 1:
            resp = await session.request('GET', url=f'https://api.vk.com/method/groups.edit?group_id={gid}&screen_name={url}&access_token={token}&v=5.131', **kwargs)
            data = await resp.json()
            print(data)
            if data['response'] == 1:
                curs.execute('DELETE FROM `claimlist` WHERE `url` = ?', (url,))
                webhook.embed('Autoclaimed URL', f'Successfully autoclaimed {url}', 3066993)
                webhook.message(f'{url}: {gid}, {token}')
                return data
    except:
        if data['error']['error_code'] == 5:
            with open('tokens.txt', 'r') as file:
                lines = file.readlines()
            with open('tokens.txt', 'w') as file:
                for line in lines:
                    if line.strip('\n') != f'{token}':
                        file.write(line)
            conn.execute('DELETE FROM `claimlist` WHERE `token` = ?', (token,))
            return data

async def main(**kwargs):
    while True:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in conn.execute("SELECT * FROM `claimlist`").fetchall():
                await asyncio.sleep(0.2)
                tasks.append(claim(session=session, url=url[0], gid=url[1], token=url[2], **kwargs))
            await asyncio.gather(*tasks, return_exceptions=True)

asyncio.ensure_future(main())

loop = asyncio.get_event_loop()
loop.run_forever()
