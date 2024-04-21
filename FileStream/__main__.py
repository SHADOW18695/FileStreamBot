# import sys
# import asyncio
# import logging
# import traceback
# import logging.handlers as handlers
# from FileStream.config import Telegram, Server
# from aiohttp import web
# from pyrogram import idle

# from FileStream.bot import FileStream
# from FileStream.server import web_server
# from FileStream.bot.clients import initialize_clients

# logging.basicConfig(
#     level=logging.INFO,
#     datefmt="%d/%m/%Y %H:%M:%S",
#     format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
#     handlers=[logging.StreamHandler(stream=sys.stdout),
#               handlers.RotatingFileHandler("streambot.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8")],)

# logging.getLogger("aiohttp").setLevel(logging.ERROR)
# logging.getLogger("pyrogram").setLevel(logging.ERROR)
# logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

# server = web.AppRunner(web_server())

# loop = asyncio.get_event_loop()

# async def start_services():
#     print()
#     if Telegram.SECONDARY:
#         print("------------------ Starting as Secondary Server ------------------")
#     else:
#         print("------------------- Starting as Primary Server -------------------")
#     print()
#     print("-------------------- Initializing Telegram Bot --------------------")


#     await FileStream.start()
#     bot_info = await FileStream.get_me()
#     FileStream.id = bot_info.id
#     FileStream.username = bot_info.username
#     FileStream.fname=bot_info.first_name
#     print("------------------------------ DONE ------------------------------")
#     print()
#     print("---------------------- Initializing Clients ----------------------")
#     await initialize_clients()
#     print("------------------------------ DONE ------------------------------")
#     print()
#     print("--------------------- Initializing Web Server ---------------------")
#     await server.setup()
#     await web.TCPSite(server, Server.BIND_ADDRESS, Server.PORT).start()
#     print("------------------------------ DONE ------------------------------")
#     print()
#     print("------------------------- Service Started -------------------------")
#     print("                        bot =>> {}".format(bot_info.first_name))
#     if bot_info.dc_id:
#         print("                        DC ID =>> {}".format(str(bot_info.dc_id)))
#     print(" URL =>> {}".format(Server.URL))
#     print("------------------------------------------------------------------")
#     await idle()

# async def cleanup():
#     await server.cleanup()
#     await FileStream.stop()

# if __name__ == "__main__":
#     try:
#         loop.run_until_complete(start_services())
#     except KeyboardInterrupt:
#         pass
#     except Exception as err:
#         logging.error(traceback.format_exc())
#     finally:
#         loop.run_until_complete(cleanup())
#         loop.stop()
#         print("------------------------ Stopped Services ------------------------")

import sys
import asyncio
import logging
import traceback
import logging.handlers as handlers
from FileStream.config import Telegram, Server
from aiohttp import web
from pyrogram import idle

from FileStream.bot import FileStream
from FileStream.server import web_server
from FileStream.bot.clients import initialize_clients

logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(stream=sys.stdout),
              handlers.RotatingFileHandler("streambot.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8")],)

logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

async def start_services():
    try:
        if Telegram.SECONDARY:
            print("------------------ Starting as Secondary Server ------------------")
        else:
            print("------------------- Starting as Primary Server -------------------")
        print()
        print("-------------------- Initializing Telegram Bot --------------------")
        
        await FileStream.start()
        bot_info = await FileStream.get_me()
        FileStream.id = bot_info.id
        FileStream.username = bot_info.username
        FileStream.fname = bot_info.first_name
        print("------------------------------ DONE ------------------------------")
        print()
        print("---------------------- Initializing Clients ----------------------")
        await initialize_clients()
        print("------------------------------ DONE ------------------------------")
        print()
        print("--------------------- Initializing Web Server ---------------------")
        
        app = web.Application()
        app.router.add_routes(web_server())
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, Server.BIND_ADDRESS, Server.PORT).start()
        
        print("------------------------------ DONE ------------------------------")
        print()
        print("------------------------- Service Started -------------------------")
        print("                        bot =>> {}".format(bot_info.first_name))
        if bot_info.dc_id:
            print("                        DC ID =>> {}".format(str(bot_info.dc_id)))
        print(" URL =>> {}".format(Server.URL))
        print("------------------------------------------------------------------")
        await idle()
    except Exception:
        logging.error("Error starting services:\n%s", traceback.format_exc())

async def cleanup():
    try:
        await FileStream.stop()
    except Exception:
        logging.error("Error stopping FileStream:\n%s", traceback.format_exc())
    try:
        await asyncio.gather(*asyncio.all_tasks())
    except Exception:
        logging.error("Error cleaning up tasks:\n%s", traceback.format_exc())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(cleanup())
        loop.close()
        print("------------------------ Stopped Services ------------------------")
