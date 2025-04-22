import pyautogui
import time
import random
import json
from datetime import datetime

# TODO:
# - refactor code, re-organize (should I even bother?)
# - force the program to click until the image is gone
# - do elite dungeon the entire account (is this a good idea?)

# BUG:
# - Need to fix confidence of image when farming AF

from dataclasses import dataclass

@dataclass
class MousePos:
    x: int
    y: int

# Load data
with open("./json/alt.json", "r") as f:
    alt_data = json.load(f)
with open("./json/main.json", "r") as f:
    main_data = json.load(f)
with open("./json/farm.json", "r") as f:
    farm_data = json.load(f)

last_click_time = None  # Stores the timestamp of the last click

def main():
    print('Starting...')
    pyautogui.FAILSAFE = True
    time.sleep(3)
    
    start_time = time.time()  # Start timer
    
    open_menu()
    # 47.35 mins
    for char in alt_data:
        # search_char(char['imgUrl'])
        print(char['imgUrl'])
        open_change_character(char['imgUrl'])
        do_daily_alt(char['doElite'], char['eliteLvl'], char['doCdd'])
        
    for char in main_data:
        # search_char(char['imgUrl'])
        print(char['imgUrl'])
        open_change_character(char['imgUrl'])
        do_daily_main(char['gemColor'])
    
    
    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time

    print(f"Execution time: {elapsed_time:.4f} seconds")
    
    do_overnight_farming_af()
    
def random_position(minX, minY, maxX, maxY):
    x = random.randint(minX, maxX)  # Random x within range
    y = random.randint(minY, maxY)  # Random y within range
    return x, y  # Return as an array

def click(): 
    rand = random.uniform(0.1, 0.25)
    pyautogui.mouseDown()
    time.sleep(rand)
    pyautogui.mouseUp()
    return

def human_pause(): 
    rand = random.uniform(0.584, 1.282)
    time.sleep(rand)
    return

def locate(imgUrl: str):
    try:
        pos = pyautogui.locateOnScreen(imgUrl, confidence=0.75)
        x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
        pyautogui.moveTo(x, y)
        return True
    except pyautogui.ImageNotFoundException:
        return False
    
def wait_n_click(image_path: str, timeout: float = 300.0, interval: float = 1, confidence: float = 0.85, wait: float = 0.5) -> bool:
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout:
            return False  # Timeout reached, exit loop
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=confidence)  # Adjust confidence if needed
            x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
            pyautogui.moveTo(x, y)
            human_pause()
            time.sleep(wait)
            click()
            return True  # Image found, exit loop
        except pyautogui.ImageNotFoundException:
            pass
        # pyautogui.moveRel(100, 100)
        time.sleep(interval)  # Wait before checking again
        
def search_char(image_path: str, timeout: float = 300.0, interval: float = 0.25) -> bool:
    start_time = time.time()
    width, height = pyautogui.size()
    pyautogui.moveTo(width / 2 - 40, height / 2)
    time.sleep(2)
    while True:
        if time.time() - start_time > timeout:
            return False  # Timeout reached, exit loop
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=0.95)  # Adjust confidence if needed
            x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
            pyautogui.moveTo(x, y)
            human_pause()
            click()
            return True  # Image found, exit loop
        except pyautogui.ImageNotFoundException:
            pass
        pyautogui.scroll(1)
        time.sleep(interval)  # Wait before checking again
    
def put_cursor_away():
    pyautogui.moveTo(random.randint(499, 1416),random.randint(3, 93), 2)
    return
        
def open_menu(): 
    wait_n_click('./imgs/buttons/menu.png')
    return

def open_dungeons(): 
    wait_n_click('./imgs/buttons/dungeons.png')
    return

def open_elite_dungeon(elite_lvl: int | None):
    wait_n_click('./imgs/buttons/elite-dungeon.png')
    if (elite_lvl == 200):
        wait_n_click('./imgs/buttons/elite-dungeon-200.png')
    elif (elite_lvl == 190):
        wait_n_click('./imgs/buttons/elite-dungeon-190.png')
    wait_n_click('./imgs/buttons/elite-dungeon-create-room.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/elite-dungeon-start.png')
    wait_n_click('./imgs/buttons/elite-dungeon-go-to-menu.png')
    wait_n_click('./imgs/buttons/back.png')
    return

def open_daily_dungeon():
    wait_n_click('./imgs/buttons/daily-dungeon.png')
    wait_n_click('./imgs/buttons/enter.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/daily-dungeon-exit.png')
    return

def open_mail(): 
    wait_n_click('./imgs/buttons/mail.png')
    wait_n_click('./imgs/buttons/mail-personal.png')
    wait_n_click('./imgs/buttons/mail-receive.png', timeout=2)
    wait_n_click('./imgs/buttons/confirm.png', timeout=2)
    wait_n_click('./imgs/buttons/close.png')
    return

def open_tasks(): 
    wait_n_click('./imgs/buttons/tasks.png')
    wait_n_click('./imgs/buttons/tasks-get-all.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/tasks-get-all.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/close.png')
    return

def open_change_character(img_url: str):
    wait_n_click('./imgs/buttons/change-character.png')
    search_char(img_url)
    wait_n_click('./imgs/buttons/change-character-change.png')
    return

def open_guild(do_elite: bool):
    wait_n_click('./imgs/buttons/guild.png', wait=1.5)
    if do_elite:
        wait_n_click('./imgs/buttons/guild-claim.png', timeout=2)
    else:
        time.sleep(1)
        
    wait_n_click('./imgs/buttons/close.png')
    
    if do_elite:
        pyautogui.press('esc')
    return

def do_daily_alt(do_elite: bool, elite_lvl: int | None, do_cdd: bool):
    open_menu()
    open_guild(do_elite)
    if do_elite:
        open_mail()
        open_menu()
    open_dungeons() 
    if do_elite:
        open_elite_dungeon(elite_lvl)     
    if do_cdd:
        open_daily_dungeon()
    else: 
        wait_n_click('./imgs/buttons/close.png')
    open_mail()
    open_menu()
    if do_elite:
        open_tasks()
    return

def open_elite_dungeon_main():
    wait_n_click('./imgs/buttons/elite-dungeon.png')

    # Do chaos first
    wait_n_click('./imgs/buttons/elite-dungeon-create-room.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/elite-dungeon-start.png')
    wait_n_click('./imgs/buttons/elite-dungeon-go-to-menu-chaos.png')
    
    # Do 200 later
    wait_n_click('./imgs/buttons/elite-dungeon-200.png', wait=1)
    wait_n_click('./imgs/buttons/elite-dungeon-create-room.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/elite-dungeon-start.png')
    wait_n_click('./imgs/buttons/elite-dungeon-go-to-menu.png')
    
    wait_n_click('./imgs/buttons/back.png')
    return

def open_daily_dungeon_main(gemColor: str):
    # Get the weekday number
    # 0 = Monday, 6 = Sunday
    weekday_number = datetime.today().weekday()
    wait_n_click('./imgs/buttons/daily-dungeon.png')
    
    # Do chaos first
    wait_n_click('./imgs/buttons/enter.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/daily-dungeon-go-to-menu.png')
    
    # Do normal later
    wait_n_click('./imgs/buttons/daily-dungeon-hell.png')
    # Check if it's weekend or not
    if weekday_number in [5, 6]:
        if gemColor == "cyan":
            wait_n_click('./imgs/buttons/daily-dungeon-cyan.png')
        elif gemColor == "yellow":
            wait_n_click('./imgs/buttons/daily-dungeon-yellow.png')
        wait_n_click('./imgs/buttons/daily-dungeon-option-2.png')
        wait_n_click('./imgs/buttons/daily-dungeon-enter-special.png')
    else:
        wait_n_click('./imgs/buttons/daily-dungeon-enter-normal.png')
        wait_n_click('./imgs/buttons/daily-dungeon-minus.png')

    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/daily-dungeon-go-to-menu.png')
    wait_n_click('./imgs/buttons/back.png')
    return

def open_dimension_invasion():
    wait_n_click('./imgs/buttons/dimension-invasion.png')
    wait_n_click('./imgs/buttons/quick-party-search.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/dimension-invasion-go-to-menu.png', 600)
    wait_n_click('./imgs/buttons/back.png')
    return

def open_mini_dungeon():
    wait_n_click('./imgs/buttons/mini-dungeon.png')
    wait_n_click('./imgs/buttons/mini-dungeon-final-result-exit.png', timeout=2)
    wait_n_click('./imgs/buttons/mini-dungeon-auto-select.png')
    wait_n_click('./imgs/buttons/enter.png')
    wait_n_click('./imgs/buttons/enter.png')
    put_cursor_away()
    wait_n_click('./imgs/buttons/mini-dungeon-final-result-exit.png', timeout=900, wait=5)
    wait_n_click('./imgs/buttons/ab-confirm.png', wait=2)
    # locate_n_click('./imgs/buttons/elite-dungeon-go-to-menu.png') # this works too, just in case
    return

def open_tasks_main(): 
    wait_n_click('./imgs/buttons/tasks.png')
    wait_n_click('./imgs/buttons/tasks-get-all.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/tasks-get-all.png', timeout=2)
    wait_n_click('./imgs/buttons/confirm.png', timeout=2)
    wait_n_click('./imgs/buttons/tasks-daily-hunt.png')
    wait_n_click('./imgs/buttons/tasks-daily-hunt-get-all.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/close.png')
    return

def open_daily_quest():
    wait_n_click('./imgs/buttons/daily-quest.png')
    wait_n_click('./imgs/buttons/daily-quest-progress.png')
    wait_n_click('./imgs/buttons/daily-quest-1.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-2.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-3.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-4.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-5.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-6.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/confirm.png', timeout=1200, wait=4)
    return

# 1585 600

def search_n_scroll_n_click(image_path: str, mouse_pos: MousePos, direction: int = 1, timeout: float = 300.0, interval: float = 0.25, sleep: float = 0.5, stop_image_path: str | None = None) -> bool:
    start_time = time.time()
    pyautogui.moveTo(mouse_pos.x, mouse_pos.y)
    time.sleep(0.5)
    while True:
        if time.time() - start_time > timeout:
            return False  # Timeout reached, exit loop
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=0.95)  # Adjust confidence if needed
            x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
            pyautogui.moveTo(x, y)
            time.sleep(sleep)
            human_pause()
            click()
            return True  # Image found, exit loop
        except pyautogui.ImageNotFoundException:
            pass
        if stop_image_path:
            res = locate(stop_image_path)
            if res:
                return False
        pyautogui.scroll(1 * direction)
        time.sleep(interval)  # Wait before checking again

def do_daily_main(gemColor: str):
    open_menu()
    open_guild(True)
    open_mail()
    open_menu()
    open_dungeons()
    open_elite_dungeon_main()
    open_daily_dungeon_main(gemColor)
    open_dimension_invasion()
    open_mini_dungeon()
    open_menu()
    open_tasks_main()
    open_daily_quest()
    open_mail()
    open_menu()
    return

def open_af(af_image_path: str): 
    wait_n_click('./imgs/buttons/arcane-power-field.png')
    search_n_scroll_n_click(af_image_path, MousePos(1585, 600))
    
    found_no_party = locate('./imgs/buttons/af-no-party.png')

    if found_no_party:  # same as "if found_no_party == True"
        wait_n_click('./imgs/buttons/create.png')
        put_cursor_away()
        wait_n_click('./imgs/buttons/create-orange.png')
        wait_n_click('./imgs/buttons/auto-battle.png')
        put_cursor_away()
        wait_n_click('./imgs/buttons/auto-battle.png')
        wait_n_click('./imgs/buttons/start.png')
        return
    
    party_paths = [
        ('./imgs/buttons/af-party-5.png', -1),
        ('./imgs/buttons/af-party-4.png', 1),
        ('./imgs/buttons/af-party-3.png', -1),
        ('./imgs/buttons/af-party-2.png', 1),
        ('./imgs/buttons/af-party-1.png', -1),
    ]

    for path, direction in party_paths:
        if search_n_scroll_n_click(path, MousePos(1585, 600), direction, stop_image_path='./imgs/buttons/af-more-party.png'):
            break
        
    wait_n_click('./imgs/buttons/apply.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/auto-battle.png')
    put_cursor_away()
    wait_n_click('./imgs/buttons/auto-battle.png')
    wait_n_click('./imgs/buttons/start.png')
    return

def open_sf(sf_image_path: str): 
    wait_n_click('./imgs/buttons/star-force-field.png')
    search_n_scroll_n_click(sf_image_path, MousePos(1585, 600))
    
    found_no_party = locate('./imgs/buttons/af-no-party.png')

    if found_no_party:  # same as "if found_no_party == True"
        wait_n_click('./imgs/buttons/create.png')
        put_cursor_away()
        wait_n_click('./imgs/buttons/create-orange.png')
        wait_n_click('./imgs/buttons/auto-battle.png')
        put_cursor_away()
        wait_n_click('./imgs/buttons/auto-battle.png')
        wait_n_click('./imgs/buttons/start.png')
        return
    
    party_paths = [
        ('./imgs/buttons/af-party-5.png', -1),
        ('./imgs/buttons/af-party-4.png', 1),
        ('./imgs/buttons/af-party-3.png', -1),
        ('./imgs/buttons/af-party-2.png', 1),
        ('./imgs/buttons/af-party-1.png', -1),
    ]

    for path, direction in party_paths:
        if search_n_scroll_n_click(path, MousePos(1585, 600), direction, stop_image_path='./imgs/buttons/af-more-party.png'):
            break
        
    wait_n_click('./imgs/buttons/apply.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/auto-battle.png')
    put_cursor_away()
    wait_n_click('./imgs/buttons/auto-battle.png')
    wait_n_click('./imgs/buttons/start.png')
    return

def quit_this_damn_game():
    time.sleep(5)
    pyautogui.press('esc')
    put_cursor_away()
    wait_n_click('./imgs/buttons/yes.png')
    return

def turn_pc_off():
    wait_n_click('./imgs/desktop-buttons/window.png')
    wait_n_click('./imgs/desktop-buttons/power.png')
    time.sleep(1)
    # wait_n_click('./imgs/desktop-buttons/sleep.png')
    wait_n_click('./imgs/desktop-buttons/power.png')
    # wait_n_click('./imgs/desktop-buttons/sleep.png')
    click()
    return

def do_overnight_farming_af():
    open_change_character('./imgs/characters/Nyuko.png') # literally any character you don't plan on farming with
    open_menu()
    open_change_character(farm_data['imgUrl']) 
    open_menu()
    open_dungeons()
    open_af(farm_data['afImgUrl'])
    quit_this_damn_game()
    turn_pc_off()
    return

def do_overnight_farming_sf():
    # open_change_character('./imgs/characters/Nyuko.png') # literally any character you don't plan on farming with
    # open_menu()
    open_change_character(farm_data['imgUrl']) 
    open_menu()
    open_dungeons()
    open_sf(farm_data['afImgUrl'])
    quit_this_damn_game()
    turn_pc_off()
    return
    
if __name__ == "__main__":
    main()
