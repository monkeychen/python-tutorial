import asyncio
import orm
from models import User, Blog, Comment

async def test(loop):
    await orm.create_pool(loop, user='root', password='admin', db='tutorial')
    user = User(name='Admin2', email='test2@simiam.com', passwd='admin', image='about:blank')
    affectRows = await user.save()
    print("Success to save user, affectedRows: %s" % affectRows)


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
