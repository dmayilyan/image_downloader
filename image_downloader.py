import asyncio
import os

import aiofiles
import aiohttp
import async_timeout
from beartype import beartype

max_page: dict = {
    1: 720,
    2: 720,
    3: 720,
    4: 720,
    5: 720,
    6: 720,
    7: 719,
    8: 720,
    9: 720,
    10: 736,
    11: 720,
    12: 752,
    13: 688,
}
VOLUME: int = 1

url_templates: dict = {
    1: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-2000px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    2: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-2000px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    3: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-2000px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    4: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-1024px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    5: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-2166px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    6: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-1024px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    7: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-1024px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    8: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-1024px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    9: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-1024px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    10: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-1024px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    11: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-1024px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    12: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-2197px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
    13: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu/page{p}-2197px-Հայկական_Սովետական_Հանրագիտարան_(Soviet_Armenian_Encyclopedia)_{vol}.djvu.jpg",
}


@beartype
def generate_urls() -> list:
    url_list: list = []
    for p in range(1, max_page[VOLUME] + 1):
        url: str = url_templates[VOLUME].format(vol=VOLUME, p=p)
        url_list.append(url)

    return url_list[44:45]


@beartype
async def get_image(url, session):
    file_name: str = url.split("/")[-1]

    async with async_timeout.timeout(120):
        async with session.get(url) as res:
            fd = await aiofiles.open(os.path.join("HSH", file_name), "wb")
            if res.status != 200:
                print(res.status)
            await fd.write(await res.read())
            await fd.close()

    return f"Successfully downloaded {file_name}"


@beartype
async def main(urls, conn):
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [get_image(url, session) for url in urls]

        return await asyncio.gather(*tasks)


urls = generate_urls()

# limit number of requests
conn = aiohttp.TCPConnector(limit=10)
loop = asyncio.get_event_loop()

results = loop.run_until_complete(main(urls, conn))

print("\n".join(results))
