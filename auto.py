import time
import traceback
import logging
from pynput.keyboard import Listener, KeyCode, Key, Controller
import pyautogui as pg
import mouse_lib
import image_lib
from tkinter import Tk, Frame, BOTH
from tkinter.ttk import Button
import cv2 as cv
import numpy as np

keyboard = Controller()

timne_upgrade = 100
retry_time = 5
scroll_time_max = 5
hasUpgrItem = False
hasMaterials = False
firstClick = False

delay=0.2
start_key=KeyCode(char='s')

# images
button_down_image = './assets/button_down.png'
button_ok_image = './assets/button_ok.png'
material_image = './assets/material.png'
weapon_image = './assets/weapon.png'
materials_image = './assets/materials.png'
upgr_item_image = './assets/upgr_item.png'
screen_image = './assets/screen.png'
action_click_image = './assets/action_click.png'
weapon_lv10_image = './assets/weapon_lv10.png'
materials_word_image = './assets/materials_word.png'
button_up_image = './assets/button_up.png'
button_down_image = './assets/button_down.png'
max_top_image = './assets/max_top.png'
max_bottom_image = './assets/max_bottom.png'

def move_to_target(pos, dir = 'center', leftAdd = 50, topAdd = 50):
    if dir == 'left':
        point = [pos['left'] + leftAdd, pos['top'] + topAdd]
    else:
        point = [pos['left'] + int(pos['width']/2), pos['top'] + int(pos['height']/2)]
    mouse_lib.move(point[0], point[1])

def do_click():
    global firstClick
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

def click_target(image_url, condition = True, threshold = 0.9):
    clicked = False
    time.sleep(0.5)
    for index in range(retry_time):
        do_click()
        time.sleep(1)
        screenShot()
        haystack_img = cv.imread(screen_image)
        actionClickPos = image_lib.detectImage(haystack_img, image_url, threshold)
        if (condition and actionClickPos != None) or (condition == False and actionClickPos == None):
            clicked = True
            break

    if clicked == False:
        print('Click Fail')
    return clicked

def press_target(key, image_url):
    pressed = False
    for index in range(retry_time):
        keyboard.press(key)
        time.sleep(1)
        screenShot()
        haystack_img = cv.imread(screen_image)
        needlePos = image_lib.detectImage(haystack_img, image_url, 0.95)
        if needlePos == None:
            pressed = True
            break

    if pressed == False:
        print('Press Fail')
    return pressed

def check_exist_image(image_url, threshold = 0.85):
    screenShot()
    haystack_img = cv.imread(screen_image)
    imagePos = image_lib.detectImage(haystack_img, image_url, threshold)
    time.sleep(1)
    if imagePos != None:
        return True
    else:
        return False

def screenShot():
    # take screenshot using pyautogui
    screenObj = pg.screenshot()
    screenObj = cv.cvtColor(np.array(screenObj), cv.COLOR_RGB2BGR)
    cv.imwrite(screen_image, screenObj)
    time.sleep(0.5)

def step_weapon(haystack_img):
    global hasUpgrItem, hasMaterials
    status = 'Next'
    if hasUpgrItem == False:
        upgrItemPos = image_lib.detectImage(haystack_img, upgr_item_image, 0.95)
        if upgrItemPos == None:
            print('UpgrItem already')
            hasUpgrItem = True
        else:
            weaponPos = image_lib.detectImage(haystack_img, weapon_image, 0.9)
            if weaponPos == None:
                status = 'Not_Found'
                return status
            else:
                move_to_target(weaponPos)
                if click_target(action_click_image, True, 0.85) == False:
                    status = 'Break'
                    return status

                isClickWeapon = False
                # check weapon lv 10 can't upgrade 
                if check_exist_image(weapon_lv10_image, 1) == True:
                    materialsWordPos = image_lib.detectImage(haystack_img, materials_word_image)
                    isClickWeapon = True
                    if materialsWordPos != None:
                        move_to_target(materialsWordPos, 'left', -50, 50)
                    else:
                        print('Error Weapon Lv 10')
                        status = 'Break'
                        return status
                else:
                    move_to_target(upgrItemPos, 'left')
                    
                if click_target(upgr_item_image, isClickWeapon) == False:
                    status = 'Break'
                    return status
                hasUpgrItem = True
    return status

def step_materials(haystack_img):
    global hasUpgrItem, hasMaterials
    status = 'Next'
    if hasMaterials == False:
        materialsPos = image_lib.detectImage(haystack_img, materials_image, 0.95)
        if materialsPos == None:
            print('Materials already')
            hasMaterials = True
        else:
            materialPos = image_lib.detectImage(haystack_img, material_image)
            if materialPos == None:
                status = 'Not_Found'
                return status
            else:
                move_to_target(materialPos)
                if click_target(action_click_image, True, 0.85) == False:
                    status = 'Break'
                    return status
                move_to_target(materialsPos, 'left')
                if click_target(materials_image, False) == False:
                    status = 'Break'
                    return status
                hasMaterials = True
    return status

def step_click_ok(haystack_img, force_click = False):
    global hasUpgrItem, hasMaterials
    status = 'Next'
    if force_click or (hasMaterials and hasUpgrItem):
        buttonOkPos = image_lib.detectImage(haystack_img, button_ok_image, 0.5)
        if buttonOkPos == None:
            print('Can not find button ok!!!')
        else:
            move_to_target(buttonOkPos)
            if force_click:
                do_click()
            else:
                do_click()
                # keyboard.press('z')
        hasMaterials = False
        hasUpgrItem = False
    else:
        print('Can not upgrade!!!')
        status = 'Break'
        return status
    return status

def click_clear(haystack_img):
    status = 'Fail'
    actionClickPos = image_lib.detectImage(haystack_img, action_click_image, 0.85)
    if actionClickPos != None:
        move_to_target(actionClickPos, 'left')
        # False => you can't see action_click_image
        if click_target(action_click_image, False, 0.85) == True:
            status = 'Cleared'
    else:
        status = 'No_Clear'

    if status == 'Fail':
        print('Click Clear Fail')
    else:
        step_click_ok(haystack_img, True)
    return status

def scrollBackpack(callback, threshold = 0.9):
    isChangeDirect = False
    time.sleep(0.5)
    screenShot()
    haystack_img = cv.imread(screen_image)
    time.sleep(0.5)
    maxTopPos = image_lib.detectImage(haystack_img, max_top_image, threshold)
    if maxTopPos == None:
        time.sleep(0.5)
        maxBottonPos = image_lib.detectImage(haystack_img, max_bottom_image, threshold)
        if maxBottonPos != None:
               isChangeDirect = True

    for index in range(2):
        if isChangeDirect == True:
            if index == 0:
                button_url = button_down_image
                scrollBar_url = max_bottom_image
            else:
                button_url = button_up_image
                scrollBar_url = max_top_image
        else:
            if index == 0:
                button_url = button_up_image
                scrollBar_url = max_top_image
            else:
                button_url = button_down_image
                scrollBar_url = max_bottom_image

        isFirstScan = True

        for indexScroll in range(scroll_time_max):
            screenShot()
            haystack_img = cv.imread(screen_image)
            time.sleep(1)
            scrollBarPos = image_lib.detectImage(haystack_img, scrollBar_url, threshold)
            if scrollBarPos != None:
                if isFirstScan:
                    status = callback(haystack_img)
                    if status == 'Break' or status == 'Next':
                        return 1
                break

            buttonPos = image_lib.detectImage(haystack_img, button_url, threshold)
            if buttonPos != None:
                move_to_target(buttonPos)
                do_click()
                time.sleep(1)
                screenShot()
                haystack_img = cv.imread(screen_image)
                status = callback(haystack_img)
                isFirstScan = False
                if status == 'Break' or status == 'Next':
                    return 1
            else:
                break
    return 1

def play_auto():
    try:
        global hasUpgrItem, hasMaterials
        for index in range(timne_upgrade):
            screenShot()
            haystack_img = cv.imread(screen_image)
            time.sleep(1)

            # click to clear
            statusClear = click_clear(haystack_img)
            if statusClear == 'Fail':
                break
            elif statusClear == 'Cleared':
                screenShot()
                haystack_img = cv.imread(screen_image)
                time.sleep(1)

            statusMaterials = step_materials(haystack_img)
            if statusMaterials == 'Break':
                break
            elif statusMaterials == 'Not_Found':
                scrollBackpack(step_materials)
                # screenShot again
                time.sleep(1)
                screenShot()
                haystack_img = cv.imread(screen_image)

            statusWeapon = step_weapon(haystack_img)
            if statusWeapon == 'Break':
                break
            elif statusWeapon == 'Not_Found':
                scrollBackpack(step_weapon)

            statusClickOk = step_click_ok(haystack_img)
            if statusClickOk == 'Break':
                break
            print('Done ', index)
            time.sleep(4)
        print('Done All')
    except Exception as e:
        logging.error(traceback.format_exc())


# ============== Popup ================ 
class Popup(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def startAuto(no_use):
        play_auto()

    def initUI(self):
        self.parent.title("Simple")
        self.pack(fill=BOTH, expand=1)
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=200, y=40)

        startButton = Button(self, text="Start", command=self.startAuto)
        startButton.place(x=30, y=40)

root = Tk()
root.geometry("350x120")
app = Popup(root)
root.mainloop() 


# ============== Listener keyboard ================
# def on_press(key):
#     try:
#         print('key {0} pressed'.format(key.char))
#         if key == start_key:
#             play_auto()
#     except AttributeError:
#         print('special key {0} pressed'.format(key))
    

# def on_release(key):
#     if key == Key.esc:
#         # Stop listener
#         return False

# with Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()