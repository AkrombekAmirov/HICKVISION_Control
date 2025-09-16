from DatabaseService import DatabaseService1, User
from LoggingService import LoggerService
from asyncio import run
import os
import aiohttp

logger = LoggerService().get_logger()
db = DatabaseService1(logger=LoggerService())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FOLDER = os.path.join(BASE_DIR, "ImagesFolder")
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Log fayllar
SUCCESS_LOG = os.path.join(BASE_DIR, "success.txt")
ERROR_LOG = os.path.join(BASE_DIR, "errors.txt")

async def get_images_func():
    # oldingi loglarni tozalab olish
    open(SUCCESS_LOG, "w").close()
    open(ERROR_LOG, "w").close()

    try:
        user_info = await db.get(User)

        async with aiohttp.ClientSession() as session:
            for user in user_info:
                try:
                    url = user.image_url
                    filename = f"{user.turniket_id}.jpg"
                    file_path = os.path.join(SAVE_FOLDER, filename)

                    async with session.get(url) as resp:
                        if resp.status != 200:
                            error_msg = f"{user.turniket_id} | ❌ Yuklab bo‘lmadi | Status: {resp.status} | URL: {url}\n"
                            logger.error(error_msg.strip())
                            with open(ERROR_LOG, "a", encoding="utf-8") as ef:
                                ef.write(error_msg)
                            continue

                        image_bytes = await resp.read()

                        # Faylga yozish
                        with open(file_path, "wb") as f:
                            f.write(image_bytes)

                        success_msg = f"{user.turniket_id} | ✅ Saqlandi | Fayl: {file_path} | URL: {url}\n"
                        logger.info(success_msg.strip())
                        with open(SUCCESS_LOG, "a", encoding="utf-8") as sf:
                            sf.write(success_msg)

                except Exception as e:
                    error_msg = f"{user.turniket_id} | ❌ Exception: {e} | URL: {getattr(user, 'image_url', 'N/A')}\n"
                    logger.error(error_msg.strip())
                    with open(ERROR_LOG, "a", encoding="utf-8") as ef:
                        ef.write(error_msg)

    except Exception as ex:
        logger.error(f"Umumiy xatolik: {ex}")

if __name__ == "__main__":
    run(get_images_func())
