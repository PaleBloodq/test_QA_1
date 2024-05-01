import os
from aiohttp import web
import routes


def main():
    STAGE = os.environ.get('STAGE', 'test')
    HOST = 'localhost' if STAGE == 'test' else '0.0.0.0'
    PORT = int(os.environ.get('PAYMENTS_PORT'))
    
    app = web.Application()
    app.router.add_post('/create_payment', routes.create_payment)
    app.router.add_post('/get_payment', routes.get_payment)
    app.router.add_post('/check_token', routes.check_token)
    try:
        web.run_app(app, host=HOST, port=PORT)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
