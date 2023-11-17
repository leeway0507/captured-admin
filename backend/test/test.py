import asyncio

import aiohttp
from custom_alru import alru_cache
from pprint import pprint


@alru_cache(maxsize=32)
async def get_pep(num):
    resource = "http://www.python.org/dev/peps/pep-%04d/" % num
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(resource) as s:
                return await s.read()
        except aiohttp.ClientError:
            return "Not Found"


async def main():
    for n in 8, 290, 308, 320, 8, 218, 320, 279, 289, 320, 9991:
        pep = await get_pep(n)
        print(n, len(pep))

    print(get_pep.cache_info())
    pprint(get_pep.get_cache())
    # CacheInfo(hits=3, misses=8, maxsize=32, currsize=8)

    # closing is optional, but highly recommended
    await get_pep.cache_close()


asyncio.run(main())
