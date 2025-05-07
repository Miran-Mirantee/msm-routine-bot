from util import wait_n_click, search_n_scroll_n_click, search_char, put_cursor_away, locate, click, wait, wait_n_match_n_click
import time

def do_sf():
    wait_n_click('./imgs/buttons/forged.png')
    wait_n_click('./imgs/buttons/sf-enhance.png')
    wait_n_click('./imgs/sf/checkbox.png')
    wait_n_click('./imgs/sf/checkbox.png')
    wait_n_click('./imgs/sf/checkbox.png')
    wait_n_click('./imgs/sf/weapon_only.png')
    
    time.sleep(0.5)
    
    while True:
        res = wait_n_match_n_click('./imgs/sf/lv1_unique.png', confidence=1)
        count = 0
        stars = 0
        have_reach_12 = False
        
        while res and stars < 18 and count < 15:
            if stars == 12:
                have_reach_12 = True    
                
            wait_n_click('./imgs/sf/enhance.png')
            wait_n_click('./imgs/sf/confirm_scroll.png', timeout=1.5)
            put_cursor_away(1370, 1900, 940, 989, 0)
            wait('./imgs/sf/confirm.png')
            if locate('./imgs/sf/succeeded.png'):
                stars += 1
            elif locate('./imgs/sf/failed.png'):
                stars -= 1
            elif locate('./imgs/sf/destroyed.png'):
                wait_n_click('./imgs/sf/confirm.png', wait=2)
                put_cursor_away(1370, 1900, 940, 989, 0)
                break
            
            if have_reach_12:
                count += 1
                print(count, stars)
              
            # print(stars)
            wait_n_click('./imgs/sf/confirm.png')
            put_cursor_away(1370, 1900, 940, 989, 0)
        
        if res == False:
            print('gg, we done')
            break   
    
    wait_n_click('./imgs/buttons/close.png')
    put_cursor_away(duration=0.5)
    wait_n_click('./imgs/buttons/close-menu.png')