import os
from aiohttp import web
import routes


def main():
    STAGE = os.environ.get('STAGE', 'test')
    HOST = 'localhost' if STAGE == 'test' else '0.0.0.0'
    PORT = int(os.environ.get('PRODUCT_PARSER_PORT'))
    
    app = web.Application()
    app.router.add_post('/parse', routes.parse)
    try:
        web.run_app(app, host=HOST, port=PORT)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
