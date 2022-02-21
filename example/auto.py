import time
import traceback
import logging
from pynput.keyboard import Listener, KeyCode, Key
import pyautogui as pg
import mouseLib
import cv2 as cv
import numpy as np

timne_upgrade = 1
hasUpgrItem = False
hasMaterials = False
firstClick = False

delay=0.2
start_key=KeyCode(char='s')

# images
button_down_image = 'button_down.png'
button_ok_image = 'button_ok.png'
material_image = 'material.png'
weapon_image = 'weapon.png'
materials_image = 'materials.png'
upgr_item_image = 'upgr_item.png'

def move_and_click(pos, dir = 'center'):
    global firstClick
    if dir == 'left':
        point = [pos.left + 50, pos.top + 50]
    else:
        point = pg.center(pos)
    mouseLib.move(point[0], point[1])

    if firstClick == False:
        time.sleep(0.2)
        pg.mouseDown(button='left')
        pg.mouseUp(button='left')
        time.sleep(0.2)
        pg.mouseDown(button='left')
        firstClick = True
    else:
        time.sleep(0.2)
        pg.mouseDown(button='left')
        time.sleep(0.2)
        pg.mouseUp(button='left')


def play_auto():
    try:
        global hasUpgrItem, hasMaterials
        for index in range(timne_upgrade):
            # take screenshot using pyautogui
            screen = pg.screenshot()
            needle_img = cv.imread('albion_cabbage.jpg', cv.IMREAD_UNCHANGED)

            if hasUpgrItem == False:
                upgrItemPos = pg.locateOnScreen(upgr_item_image)
                if upgrItemPos == None:
                    hasUpgrItem = True
                else:
                    weaponPos = pg.locateOnScreen(weapon_image)
                    if weaponPos == None:
                        pass
                    else:
                        move_and_click(weaponPos)
                        move_and_click(upgrItemPos, 'left')

            if hasMaterials == False:
                materialsPos = pg.locateOnScreen(materials_image)
                if materialsPos == None:
                    hasMaterials = True
                else:
                    materialPos = pg.locateOnScreen(material_image)
                    if materialPos == None:
                        pass
                    else:
                        move_and_click(materialPos)
                        move_and_click(materialsPos, 'left')

            if hasMaterials and hasUpgrItem:
                buttonOkPos = pg.locateOnScreen(button_ok_image)
                if buttonOkPos == None:
                    print('Can not find button ok!!!')
                else:
                    move_and_click(buttonOkPos)
                hasMaterials = False
                hasUpgrItem = False
            else:
                print('Can not upgrade!!!')
                break

    except Exception as e:
        logging.error(traceback.format_exc())

def on_press(key):
    try:
        print('key {0} pressed'.format(key.char))
        if key == start_key:
            play_auto()
    except AttributeError:
        print('special key {0} pressed'.format(key))
    

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()