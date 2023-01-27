import httpx
import asyncio
import re
import json

from nonebot import get_driver

AUTH = (get_driver().config.r6db_user_id, get_driver().config.r6db_password)


async def get_data_from_r6scn(user_name: str, trytimes=6) -> dict:
    if trytimes == 0:
        return ""
    try:
        url = f"https://www.r6s.cn/Stats?username={user_name}&platform="
        headers = {
            'Host': 'www.r6s.cn',
            'referer': 'https://www.r6s.cn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        if not response.json() and trytimes == 1:
            return "Not Found"
        r: dict = response.json()
        if not (r.get("username") or r.get("StatCR")):
            trytimes -= 1
            await asyncio.sleep(0.5)
            r = await get_data_from_r6scn(user_name, trytimes=trytimes)
        return r
    except:
        trytimes -= 1
        await asyncio.sleep(0.5)
        r = await get_data_from_r6scn(user_name, trytimes=trytimes)
        return r


async def get_data_from_r6sground(user_name: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://global.r6sground.cn/stats/{user_name}/data")
    datas = re.split(r"(data: )", resp.text)
    rdatas = {}
    for d in datas:
        if d[:1] == "{":
            d = d.replace("!46$", "false")
            d = d.replace("!47$", "true")
            d_jdson = json.loads(d)
            rdatas[d_jdson["key"]] = d_jdson["data"]
    if not rdatas.get("userMainData") or rdatas["userMainData"].get("!15$_!6$s:!5$"):
        return {user_name: f"{user_name}", "error": "Not Found"}
    return rdatas


async def get_data_from_r6stats(user_name: str) -> dict:
    # parse user_name to ubi_id first
    ubi_id = user_name  # todo
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://r6stats.com/api/stats/{ubi_id}?queue=true")
    # todo


async def get_data_from_r6db(user_name: str) -> dict:
    async with httpx.AsyncClient(timeout=10, auth=AUTH, follow_redirects=True) as client:
        resp = await client.get(f"https://api.statsdb.net/r6/pc/player/{user_name}")
    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code == 404:
        return {user_name: f"{user_name}", "error": "Not Found"}
    else:
        return {user_name: f"{user_name}", "error": "Error"}
