import asyncio
import os

from aiohttp import web
import aiofiles
from aiohttp.web_exceptions import HTTPNotFound

INTERVAL_SECS = 1


async def archivate(request):
    archive_hash = request.match_info['archive_hash']
    dir_path = f"test_photos/{archive_hash}"
    if not os.path.isdir(dir_path):
        raise HTTPNotFound(reason='Архив не существует или был удален')
    os.path.isdir(dir_path)
    os.chdir(dir_path)

    response = web.StreamResponse()
    response.headers['Content-Disposition'] = 'attachment; filename="photos.zip"'
    await response.prepare(request)

    args = f'zip -R - * -0'
    process_coro = await asyncio.create_subprocess_shell(
        args,
        stdin=None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    while not process_coro.stdout.at_eof():
        await response.write(await process_coro.stdout.read())

    os.chdir('../..')
    return response


async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r', encoding='utf-8') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archivate),
    ])
    web.run_app(app)
