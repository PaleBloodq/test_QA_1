import os
from aiohttp import web
import routes


def main():
    app = web.Application()
    app.router.add_post('/parse', routes.parse)
    try:
        web.run_app(
            app,
            host=os.environ.get('PRODUCT_PARSER_HOST'),
            port=int(os.environ.get('PRODUCT_PARSER_PORT')),
        )
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
