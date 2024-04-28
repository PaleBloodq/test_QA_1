from aiohttp import web
import routes

app = web.Application()

app.router.add_post('/parse', routes.parse)

try:
    web.run_app(app, host='localhost', port=7723)
except KeyboardInterrupt:
    pass
