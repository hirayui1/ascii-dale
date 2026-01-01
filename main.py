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
        #print(f"Warrior {name} with {hp} health points and {dmg} damage has been successfully created.")

    def print_woriur(self):
        print("You have encoutered a mighty warrior!")
        print(" O ")
        print("/|\\")
        print("/ \\")              

    def bonk(self, target):
        target.take_damage(self.dmg)

    def take_damage(self, dmg):
        if (self.hp > 0):
            self.hp = self.hp - dmg
            if self.hp <= 0:
                print(f"{self.name:<3} took {dmg} dmg and died.")
            else:
                print(f"{self.name:<5} lost {dmg} hp. Current hp: {self.hp}")
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
        target.take_damage(self.m_dmg)

    def take_damage(self, dmg):
        if (self.hp > 0):
            self.hp = self.hp - dmg
            print(f"{self.name} has taken {dmg} damage.")
            if self.hp <= 0:
                print(f"{self.name} has died.")
        else:
            print(f"Your target is already dead, stop beating {self.name}'s corpse, you monstul!")

def fight_to_death(target1, target2):
    print(f"Commencing a fight to death between {target1.name} and {target2.name}.\n")
    time.sleep(1)
    while target1.hp > 0 and target2.hp > 0:
        target1.bonk(target2)
        time.sleep(1)
        target2.bonk(target1)
        time.sleep(1)


class Player:
    def __init__(self, x, y, clazz):
        self.x = x
        self.y = y
        self.clazz = clazz
        self.old_char = '.'

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
    sys.stdout.flush() 
    player.old_char = map[player.x][player.y] # update/hold current spot's char
    map[player.x][player.y] = '@' # put player to current spot
    print(f"\033[{player.x+1};{player.y+1}H{COLORS.get('@', '')}@", RESET, end="") # print player to current spot
    sys.stdout.flush() 

def random_fight(player, map):
    if random.random() < 0.005:
        os.system("cls")
        fight_to_death(player.clazz, Warrior("enemy"))
        time.sleep(3)
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


def game_loop(player, map):
    os.system("cls")
    print_map(map)
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode()
            if key == '0':
                os.system("cls")
                break
            move(player, key, map)
            if player.old_char == 'E': # we put this after move() because thats when old_char gets updated
                os.system("cls")
                break
            change_map(player, map, player.old_char)
            #random_fight(player, map)
        time.sleep(0.02)

def find_start(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if (map[i][j] == '@'):
                return i, j
    return len(map) / 2, len(map[0]) / 2 # start at the middle of the map if player not found

import msvcrt # TODO: graduate from this, it breaks cross-platform capability (its windows specific)
import time, os, sys, random
from map_generator import * # default customizable map_generator
from colorama import just_fix_windows_console
from blessed import Terminal

# TODO: change cursor repaint logic so that it doesn't break if screen is not big enough
def main():
#     term = Terminal()
#     with term.cbreak(), open("assets/overworld.map") as f: # runs while True in the context of blessed.Terminal
#         map = [list(line) for line in f.read().split('\n')]
#         x, y = find_start(map)
#         player = Player(x, y, Warrior("Potat the Lost", 35))
#         game_loop(player, map, term)
#         while True:
#             key = term.inkey(timeout=0.2)
#             if key == 'w':
#                 print("Move up!")
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

class Bat:
    def __init__(self, hp=6, att=2, name="Bat"):

        self.hp = hp
        self.att = att
        self.name = name
    print("You have found a bat!")
    print("\\/O\\/")

#TODO: a box with encounter appears on the right side of the map without closing it? @ frozen while it open
#TODO: log showing what has happened - you entered a cave, you met an enemalso on the side. SEE, I DIDN'T FORGET
#TODO: maybe add small pics showing enemy during encounter - bat = \/O\/