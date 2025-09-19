import time, pyautogui

def test_write_fields():
    # Person ID
    # time.sleep(2)
    # pyautogui.click(800, 400, duration=0.3)
    # time.sleep(1)
    # pyautogui.write("20250001")  # Person ID
    #
    # # Name
    # pyautogui.click(800, 440, duration=0.3)
    # time.sleep(1)
    # pyautogui.write("Aliyev Vali")  # Full Name
    #
    # # Photo (file tanlash)20250001
    # pyautogui.click(1170, 440, duration=0.3)
    # time.sleep(1)
    # pyautogui.write(r"20251212.jpg")  # File path
    # pyautogui.press("enter")

    # OK
    pyautogui.click(49, 192, duration=0.3)  # OK
    time.sleep(2)  # modal yopilishini kutish
    # pyautogui.click(1230, 845, duration=0.3)

if __name__ == "__main__":
    print("⏳ Test boshlanmoqda...")
    test_write_fields()
    print("✅ Maydonlar to‘ldirildi!")

# pyautogui.click(1100, 840, duration=0.3) # Person ID
# pyautogui.write("20250001")  # Person ID
# pyautogui.click(800, 440, duration=0.3) # Name
# pyautogui.write("Aliyev Vali")  # Full Name
# pyautogui.click(1170, 440, duration=0.3) # Photo
# pyautogui.write(r"20251212.jpg")  # File path
# pyautogui.press("enter")
# pyautogui.click(1170, 440, duration=0.3) # Photo
