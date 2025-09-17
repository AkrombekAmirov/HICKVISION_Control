from selenium.webdriver.support import expected_conditions as EC
from DataConfig.ImagesFolder import get_images_file_path
from selenium.webdriver.support.ui import WebDriverWait
from DatabaseService import DatabaseService1, User
from selenium.webdriver.common.by import By
from LoggingService import LoggerService
import time, asyncio, pyautogui
from selenium import webdriver

logger = LoggerService().get_logger()
db = DatabaseService1(logger=LoggerService())

ip = "http://10.32.104.163:9282"

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)


def add_user(person_id, full_name, photo_path):
    try:
        # + Add tugmasini bosish (Selenium orqali)
        add_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(@class,'ng-binding') and text()='Add']")))
        add_btn.click()
        time.sleep(1)  # modal ochilishi uchun

        # === Person ID (PyAutoGUI) ===
        pyautogui.click(800, 400, duration=0.3)
        time.sleep(0.5)
        pyautogui.write(str(person_id))

        # === Full Name (PyAutoGUI) ===
        pyautogui.click(800, 440, duration=0.3)
        time.sleep(0.5)
        pyautogui.write(full_name)

        # === Photo upload (PyAutoGUI) ===
        pyautogui.click(1170, 440, duration=0.3)
        time.sleep(1)
        pyautogui.write(photo_path)  # to‘liq path kerak!
        pyautogui.press("enter")

        time.sleep(2)  # rasm yuklanishi va yuz analiz

        # === OK tugmasi (PyAutoGUI) ===
        pyautogui.click(1100, 840, duration=0.3)
        time.sleep(2)  # modal yopilishini kutish

        logger.info(f"✅ User qo‘shildi: {person_id} | {full_name}")

    except Exception as e:
        logger.error(f"❌ Xato {person_id} | {full_name}: {e}")


async def main():
    user_info1 = await db.get(User)  # test uchun 5 ta

    driver.get(f"{ip}/#/login")

    # === LOGIN ===
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='User Name']"))).send_keys("admin")
    driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']").send_keys("abcd2024")
    driver.find_element(By.CSS_SELECTOR, "button.login-btn").click()

    # === Users sahifasiga kirish ===
    wait.until(EC.url_contains("#/home"))
    driver.get(f"{ip}/#/home/peopleManage")
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Add']")))

    # === Sikl orqali userlarni qo‘shish ===
    for user in user_info1:
        photo_path = await get_images_file_path(f"{user.turniket_id}.jpg")
        if photo_path:
            add_user(user.turniket_id, user.full_name, photo_path)
        else:
            logger.warning(f"⚠️ Surat topilmadi: {user.turniket_id}.jpg")

    print("✅ Test sikl tugadi.")


if __name__ == "__main__":
    asyncio.run(main())
    driver.quit()
    print("🔚 Dastur yakunlandi.")
