from hikvision_face_service import upload_user_to_hikvision
from DatabaseService import DatabaseService1, User
from LoggingService import LoggerService
from asyncio import run
from DataConfig.ImagesFolder import get_images_file_path

db = DatabaseService1(logger=LoggerService())
logger = LoggerService().get_logger()

device_info = {
    "name": "Asosiy Bino 2-turniket",
    "ip": "192.128.1.212",
    "username": "admin",
    "password": "abcd2024"
}

async def write_turniket():
    try:
        # 1. Bazadan foydalanuvchi olish
        user_info = await db.get(User, filters={"student_id": "20251212"})
        user = user_info[0]

        # 2. Surat tayyorlash
        image_path = await get_images_file_path(f"{user.turniket_id}.jpg")
        # prepared_image = prepare_hikvision_face_image(image_path, f"{user.turniket_id}.jpg")

        logger.info(f"📷 Surat yo‘li: {image_path}")
        logger.info(f"👤 Foydalanuvchi: {user.full_name} | ID: {user.turniket_id}")

        # 3. Turniketga foydalanuvchini yozish
        success = upload_user_to_hikvision(device_info, user, user.gender, image_path, logger)

        if success:
            print("🎉 Foydalanuvchi muvaffaqiyatli yozildi!")
        else:
            print("❌ Foydalanuvchi yozishda xatolik yuz berdi.")

        # 4. Face bilan bog‘langanini tekshirish
        # linked = check_user_face_link(device_info, user.turniket_id)
        # print("✅ Surat bog‘langan!" if linked else "❌ Surat bog‘lanmagan.")

    except Exception as ex:
        logger.exception(f"❌ Umumiy xatolik: {ex}")
if __name__ == "__main__":
    run(write_turniket())
