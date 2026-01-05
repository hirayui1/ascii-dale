# Classes

class Player:
    def __init__(self, x, y, clazz):
        self.x = x
        self.y = y
        self.clazz = clazz
        self.old_char = '.'

class Warrior:
    def __init__(self, name, hp=10, dmg=5):
        self.name = name
        if (hp > 0 and hp < 1000):
            self.hp = hp
        else:
            hp = 10
        if (dmg > 0 and dmg < 15):
            self.dmg = dmg
        else:
            dmg = 5

    def bonk(self, target):
        return target.take_damage(self.dmg)

    def take_damage(self, dmg):
        if (self.hp > 0):
            self.hp = self.hp - dmg
            if self.hp <= 0:
                print(f"{self.name:<3} took {dmg} dmg and died.")
                return True # true if this dmg kills
            else:
                print(f"{self.name:<5} lost {dmg} hp. Current hp: {self.hp}")
                return False # false if still alive
        else:
            print(f"Your target is already dead, stop beating {self.name}'s corpse, you monstul!")

class Archer:
    def __init__(self, name, hp=8, m_dmg=10, r_dmg=6, range_treshold=2):
        self.name = name
        self.hp = hp
        self.m_dmg = m_dmg
        self.r_dmg = r_dmg
        self.range_treshold = range_treshold
        
    def hit (self, target, cur_range):
        if cur_range <= 2:
            self.bonk(target)
        else:
            self.shoot(target)
    
    def shoot(self, target):
        print(f"Shooting {target.name} for {self.r_dmg} dmg.")
        target.take_damage(self.r_dmg)

    def bonk(self, target):
        print(f"Bonking {target.name} for {self.m_dmg} dmg.")
        return target.take_damage(self.m_dmg) # return true if target dies as a result

    def take_damage(self, dmg):
        if (self.hp > 0):
            self.hp = self.hp - dmg
            print(f"{self.name} has taken {dmg} damage.")
            if self.hp <= 0:
                print(f"{self.name} has died.")
                return True # true if died as a result of taking damage
            return False # false if still alive after taking damage
        else:
            print(f"Your target is already dead, stop beating {self.name}'s corpse, you monstul!")

## ENEMY

class Bat(Warrior):
    def __init__(self, hp=6, dmg=2, name="Bat"):
        self.hp = hp
        self.dmg = dmg
        self.name = name

        print("You have found a bat!")
        print("\\/O\\/")

class Slime(Warrior):
    def __init__(self, hp=3, dmg=3, name="Slime"):
        self.hp = hp
        self.dmg = dmg
        self.name = name

        print("It's a wobbly slime!")
        print (" ___")
        print ("(___)")

class Sponder(Warrior):
    def __init__(self, hp=4, dmg=6, name="Sponder"):
        self.hp = hp
        self.dmg = dmg
        self.name = name

        print("You see a crawling sponder. Kill it before it lays eggs!")
        print("/\\o/\\")

class Golem(Warrior):
    def __init__(self, hp=25, dmg=7, name="Golem"):
        self.hp = hp
        self.dmg = dmg
        self.name = name

        print("You've encounter the boss of this area. May fortune favor you!")
        print("  O ")
        print("-/ \\-")
        print(" |_|")
        print("/   \\")

def fight_to_death(target1, target2):
    print(f"Commencing a fight to death between {target1.name} and {target2.name}.\n")
    time.sleep(1)
    while True:
        if target1.bonk(target2):
            break
        time.sleep(1)
        if target2.bonk(target1):
            break
        time.sleep(1)

#TODO: remove these    
from colorama import Fore, Back, Style, init

COLORS = {
    '@': Style.BRIGHT + Fore.GREEN,   # green player
    'T': Fore.YELLOW,   # yelo tresha
    'M': Style.DIM + Fore.YELLOW,   # yelo tresha
    'W': Style.BRIGHT + Fore.LIGHTBLACK_EX,   # yelo tresha
}

RESET = '\033[0m'

def print_map(map):
    for line in map:
        for char in line:
            print(COLORS.get(char, ''), char, RESET, sep='', end='')
            # print(char, end="")
        print()

def move(player, key, map):
    old_x, old_y = player.x, player.y
    if key == 'w' and player.x > 0 and map[player.x - 1][player.y] != 'M' and map[player.x - 1][player.y] != 'W':
        player.x -= 1 # update player position
    elif key == 'a' and player.y > 0 and map[player.x][player.y - 2] != 'M' and map[player.x][player.y - 2] != 'W':
        player.y -= 2
    elif key == 's' and player.x < len(map) - 1 and map[player.x + 1][player.y] != 'M' and map[player.x + 1][player.y] != 'W': # len - 1
        player.x += 1
    elif key == 'd' and player.y < len(map[player.x]) - 2 and map[player.x][player.y + 2] !='M' and map[player.x][player.y + 2] != 'W': # len - 2 because the end of the line is ". . . ." and we only care about every second dot
        player.y += 2
    else:
        return

    map[old_x][old_y] = player.old_char # change map 
    print(f"\033[{old_x+1};{old_y+1}H{COLORS.get(player.old_char, '')}{player.old_char}", RESET, end="")  # reprint old spot
    player.old_char = map[player.x][player.y] # update/hold current spot's char
    map[player.x][player.y] = '@' # put player to current spot
    sys.stdout.flush() # flush above print near player movement
    print(f"\033[{player.x+1};{player.y+1}H{COLORS.get('@', '')}@", RESET, end="") # print player to current spot
    sys.stdout.flush() 

def monster_random():
    BAT_PROB = 0.4
    SLIME_PROB = 0.2
    SPONDER_PROB = 0.3 

    if random.random() < BAT_PROB:
        return Bat()
    elif random.random() < SPONDER_PROB:
        return Sponder()
    elif random.random() < SLIME_PROB:
        return Slime()
    else:
        return Golem()
    
# TODO: make these enemies appear only in the caves

def random_fight(player, map):
    if random.random() < 0.02:
        os.system("cls")
        fight_to_death(player.clazz, monster_random())
        time.sleep(3)
        if player.clazz.hp < 1:
            print("Game Over.")
            sys.exit()
        os.system("cls")
        print_map(map)

def change_map(player, old_map, map_type):
    if map_type == 'C':
        map = gen_cave(16, 16)
        old_x, old_y = player.x, player.y
        player.x, player.y = 0, 0
        older_char = player.old_char
        player.old_char = 'E'
        game_loop(player, map) # TODO: make a way that if you gain something inside, player outside also does
        player.old_char = 'c'
        player.x, player.y = old_x, old_y
        os.system("cls")
        print_map(old_map)

### Trying to make pynput work, starting from importing
from pynput import keyboard
from pynput.keyboard import Key
import os
import time

last_key = None
running = True

def game_loop(player, map):
    global last_key, running

    os.system("cls")
    print_map(map)

    def on_press(key):
        global last_key
        try:
            last_key = key.char
        except AttributeError:
            last_key = key

    def on_release(key):
        global running
        if key == keyboard.Key.esc:
            running = False
            return False

    listener=keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
    listener.start()

    while running:
        if last_key is not None:
            key = last_key
            last_key = None

            if key == '0':
                os.system("cls")
                break

            move(player, key, map)
            
            if player.old_char == 'E': # we put this after move() because thats when old_char gets updated
                os.system("cls")
                break
            change_map(player, map, player.old_char)
            random_fight(player, map)
        time.sleep(0.02)
    
    listener.stop()

# def game_loop(player, map):
#     os.system("cls")
#     print_map(map)
#     while True:
#         if msvcrt.kbhit():
#             key = msvcrt.getch().decode()
#             if key == '0':
#                 os.system("cls")
#                 break
#             move(player, key, map)
#             if player.old_char == 'E': # we put this after move() because thats when old_char gets updated
#                 os.system("cls")
#                 break
#             change_map(player, map, player.old_char)
#             random_fight(player, map)
#         time.sleep(0.02)

def find_start(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if (map[i][j] == '@'):
                return i, j
    return len(map) / 2, len(map[0]) / 2 # start at the middle of the map if player not found

import msvcrt # TODO: graduate from this, only works on win (tried blessed, it sucks)
import time, os, sys, random
from map_generator import * # default customizable map_generator
from colorama import just_fix_windows_console

# TODO: change cursor repaint logic so that it doesn't break if screen is not big enough
# probably curses-python

def main():
    just_fix_windows_console()
    init()
    print("\033[?25l", end="") # hides the cursor
    try:
        file = open("assets/overworld.map") # starting map
        lines = file.read() 
        map = [list(line) for line in lines.split('\n')]
        x, y = find_start(map)
        player = Player(x, y, Warrior("Potat the Lost", 35))
        game_loop(player, map)
    finally:
        print("\033[?25h", end="")
main()

###CAVE PART - this is cool

#MONSTERS

#TODO: a box with encounter appears on the right side of the map without closing it? @ frozen while it open
#TODO: log showing what has happened - you entered a cave, you met an enemy - on the side. SEE, I DIDN'T FORGET
#TODO: maybe add small pics showing enemy during encounter - bat = \/O\/ - maybe sponder = /\o/\
#TODO: a randomizer that will choose an enemy for encounter
#TODO: break terminal into small compartments using curses, and implement inventory into one of them.