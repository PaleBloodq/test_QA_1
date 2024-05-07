import logging
import os
from aiohttp import web
import routes
logging.basicConfig(level=logging.DEBUG)

def main():
    app = web.Application()
    app.router.add_post('/create_payment', routes.create_payment)
    app.router.add_post('/get_payment', routes.get_payment)
    app.router.add_post('/check_token', routes.check_token)
    try:
        web.run_app(
            app,
            host=os.environ.get('PAYMENTS_HOST'),
            port=int(os.environ.get('PAYMENTS_PORT')),
        )
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
