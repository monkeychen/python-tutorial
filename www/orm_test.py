import asyncio
import orm
from models import User

async def test(_loop):
    await orm.create_pool(_loop, user='root', password='admin', db='tutorial')
    user = User(name='Admin2', email='test2@simiam.com', passwd='admin', image='about:blank')
    affect_rows = await user.save()
    print("Success to save user, affectedRows: %s" % affect_rows)


loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
