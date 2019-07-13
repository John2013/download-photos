import asyncio
import subprocess


async def archivate():
    args = b'zip -r - photos -1'
    process_coro = await asyncio.create_subprocess_shell(
        args,
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    archive_chunk, stderr = await process_coro.communicate()
    with open('archive.zip', 'wb') as zip_file:
        zip_file.write(archive_chunk)


async def main():
    await archivate()


if __name__ == '__main__':
    asyncio.run(main())
