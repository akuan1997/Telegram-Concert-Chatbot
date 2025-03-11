import pyautogui

# 獲取滑鼠當前的位置
x, y = pyautogui.position()

print(f"滑鼠當前位置: X={x}, Y={y}")