import json

import sqlalchemy as sa
from aiohttp import web
from aiopg.sa import create_engine

from aidja.settings import DATABASES

db = DATABASES['default']

metadata = sa.MetaData()

circle = sa.Table(
    'app_circle', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(20)),
    sa.Column('color', sa.String(10)),
    sa.Column('x', sa.Float()),
    sa.Column('y', sa.Float()),
)


async def wshandler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async with create_engine(user=db['USER'], database=db['NAME'], password=db['PASSWORD']) as engine:
        async with engine.acquire() as conn:
            async for msg in ws:
                if msg.tp == web.MsgType.text:
                    json_data = json.loads(msg.data)
                    await conn.execute(circle.insert().values(**json_data))
                elif msg.tp == web.MsgType.close:
                    break
            return ws


app = web.Application()
app.router.add_route('GET', '/echo', wshandler)
web.run_app(app)
