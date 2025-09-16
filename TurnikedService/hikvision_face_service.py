from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time, os, pyautogui
from DatabaseService import DatabaseService1, User
from LoggingService import LoggerService
from DataConfig.ImagesFolder import get_images_file_path
import asyncio

# === Loglar ===
logger = LoggerService().get_logger()
SUCCESS_LOG = "success_students.txt"
ERROR_LOG = "error_students.txt"

open(SUCCESS_LOG, "w").close()
open(ERROR_LOG, "w").close()

db = DatabaseService1(logger=LoggerService())

# === Selenium sozlamalari ===
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# === Helper funksiyalar ===
def write_log(file, text):
    with open(file, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def fill_and_save_user(user_id, full_name, photo_path):
    try:
        # 🔹 Avval peopleManage sahifasiga kirish
        driver.get("https://192.128.1.215/doc/index.html#/peopleManage")
        time.sleep(1)  # DOM yuklanishi uchun

        # 🔹 Keyin yangi forma ochish
        driver.get("https://192.128.1.215/doc/index.html#/peopleManage/addEditPeople")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "el-input__inner")))

        inputs = driver.find_elements(By.CLASS_NAME, "el-input__inner")

        # 🔹 Employee ID va Name kiritish
        if inputs and len(inputs) >= 2:
            # Employee ID
            inputs[0].clear()
            inputs[0].send_keys(user_id)
            # event trigger qilish
            driver.execute_script("""
                        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    """, inputs[0])

            # Full Name
            inputs[1].clear()
            inputs[1].send_keys(full_name)
            driver.execute_script("""
                        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    """, inputs[1])

            time.sleep(0.5)  # DOM ga o‘tishini kutish
        else:
            raise Exception("Input maydonlari topilmadi")

        # 🔹 Surat yuklash
        file_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        file_input.send_keys(photo_path)

        # Trigger JS event
        trigger_js = """
            const input = arguments[0];
            const evt = new Event('change', { bubbles: true });
            input.dispatchEvent(evt);
        """
        try:
            driver.execute_script(trigger_js, file_input)
        except StaleElementReferenceException:
            file_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            driver.execute_script(trigger_js, file_input)

        time.sleep(3)  # yuz analiz uchun

        # 🔹 Save tugmasi (PyAutoGUI)
        pyautogui.scroll(-300)
        time.sleep(1)
        x, y = 370, 990  # Сохранить tugmasining joylashuvi
        pyautogui.moveTo(x, y, duration=0.3)
        pyautogui.click()

        # 🔹 Saqlashdan keyin kutish
        time.sleep(2)
        success_msg = f"{user_id} | {full_name} | ✅ Saqlandi"
        logger.info(success_msg)
        write_log(SUCCESS_LOG, success_msg)

    except Exception as e:
        error_msg = f"{user_id} | {full_name} | ❌ Xato: {e}"
        logger.error(error_msg)
        write_log(ERROR_LOG, error_msg)

async def main():
    user_info = await db.get(User)

    # 🔹 1170 dan boshlab filter qilish
    # user_info = [u for u in user_info1 if u.turniket_id and int(u.turniket_id) >= 20251170]

    print(f"Topildi: {len(user_info)} ta foydalanuvchi (1170 dan boshlab).")
    print("🌐 Brauzer ishga tushirildi...")
    driver.get("https://192.128.1.215/doc/index.html#/portal/login")

    # === LOGIN ===
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Имя пользователя' or @placeholder='Username']")
        )
    )
    driver.find_element(
        By.XPATH, "//input[@placeholder='Имя пользователя' or @placeholder='Username']"
    ).send_keys("admin")
    driver.find_element(
        By.XPATH, "//input[@placeholder='Пароль' or @placeholder='Password']"
    ).send_keys("abcd2024")
    driver.find_element(
        By.XPATH, "//button[contains(.,'Вход') or contains(.,'Login')]"
    ).click()

    wait.until(EC.presence_of_element_located((By.ID, "portal")))
    time.sleep(1)

    # 🔹 Har bir talabani kiritish
    for user in user_info:
        try:
            user_id = user.turniket_id
            full_name = user.full_name
            photo_path = await get_images_file_path(f"{user_id}.jpg")

            fill_and_save_user(user_id, full_name, photo_path)

        except Exception as ex:
            error_msg = f"{getattr(user, 'turniket_id', 'N/A')} | {getattr(user, 'full_name', 'N/A')} | ❌ Umumiy xato: {ex}"
            logger.error(error_msg)
            write_log(ERROR_LOG, error_msg)

    print("✅ Test rejimdagi 3 ta foydalanuvchi tugadi.")

if __name__ == "__main__":
    asyncio.run(main())
    driver.quit()
    print("🔚 Dastur yakunlandi.")
