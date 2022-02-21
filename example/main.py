import pyautogui as pg
import time
time.sleep(1)

# pg.moveTo(300, 300, duration=3)


button = pg.locateOnScreen('5.png')
buttonpoint = pg.center(button)
print(button)

buttonx, buttony = buttonpoint
pg.click(buttonx, buttony)
pg.click(buttonx, buttony)
pg.hotkey('7')