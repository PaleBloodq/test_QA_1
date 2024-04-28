import os
import asyncio
import uvicorn


async def start():
    STAGE = os.environ.get('STAGE', 'test')
    HOST = 'localhost' if STAGE == 'test' else '0.0.0.0'
    PORT = int(os.environ.get('BACKEND_PORT'))
    
    config = uvicorn.Config("settings.asgi:app", host=HOST, port=PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == '__main__':
    asyncio.run(start())
