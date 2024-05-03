import os
import asyncio
import uvicorn


async def start():
    config = uvicorn.Config(
        "settings.asgi:app",
        host=os.environ.get('BACKEND_HOST'),
        port=int(os.environ.get('BACKEND_PORT')),
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == '__main__':
    asyncio.run(start())
