# Classes
import curses
from typing import Any
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

    def display(self, stdscr, base_row: int = 0, base_col: int = 0) -> int:
        """Display enemy message and ASCII art starting at base_row/base_col.
        Returns the last row index that was written to."""
        import curses
        # Message on the first line
        stdscr.addstr(base_row, base_col, getattr(self, 'message', ''), curses.color_pair(COLOR_DEFAULT))
        row = base_row + 1
        # Art may be multi-line; draw each line on its own row
        art_lines = getattr(self, 'art', '').split('\n') if hasattr(self, 'art') else []
        for line in art_lines:
            stdscr.addstr(row, base_col, line, curses.color_pair(COLOR_DEFAULT))
            row += 1
        stdscr.refresh()
        return row - 1

    def bonk(self, target, stdscr, x):
        return target.take_damage(self.dmg, stdscr, x) # return true if target dies as a result

    def take_damage(self, dmg, stdscr, x):
        import curses
        if self.hp <= 0:
            stdscr.addstr(x, 0, f"Your target is already dead, stop beating {self.name}'s corpse, you monstul!", curses.color_pair(COLOR_DEFAULT))
            return False
        self.hp -= dmg
        if self.hp <= 0:
            stdscr.addstr(x, 0, f"{self.name:<3} took {dmg} dmg and died.", curses.color_pair(COLOR_DEFAULT))
            return True # true if this dmg kills
        else:
            stdscr.addstr(x, 0, f"{self.name:<3} took {dmg} dmg, {self.hp} hp left.", curses.color_pair(COLOR_DEFAULT))
            return False # false if still alive

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

        self.message = "A wild bat appears!"
        self.art = "  \\/O\\/ "

class Slime(Warrior):
    def __init__(self, hp=3, dmg=3, name="Slime"):
        self.hp = hp
        self.dmg = dmg
        self.name = name

        # TODO: message and art
        self.message = "It's a wobbly slime!"
        self.art = " ___\n(___)"

class Sponder(Warrior):
    def __init__(self, hp=4, dmg=6, name="Sponder"):
        self.hp = hp
        self.dmg = dmg
        self.name = name

        self.message = "You see a crawling sponder. Kill it before it lays eggs!"
        self.art = "/\\o/\\"

class Golem(Warrior):
    def __init__(self, hp=25, dmg=7, name="Golem"):
        self.hp = hp
        self.dmg = dmg
        self.name = name

        self.message = "You've encounter the boss of this area. May fortune favor you!"
        self.art = "  O \n-/ \\-\n |_|\n/   \\"

from map_generator import * # default customizable map_generator

def fight_to_death(target1, target2, stdscr):
    # Display enemy art and message and get the last row used
    last_row = target2.display(stdscr, base_row=0)
    # Start combat messages after the art
    start_row = last_row + 1
    stdscr.addstr(start_row, 0, f"Commencing a fight to death between {target1.name} and {target2.name}.", curses.color_pair(COLOR_DEFAULT))
    stdscr.refresh()
    time.sleep(1)
    x = start_row + 1
    while True:
        if target1.bonk(target2, stdscr, x):
            stdscr.refresh()
            break
        stdscr.refresh()
        x += 1
        time.sleep(1)
        if target2.bonk(target1, stdscr, x):
            stdscr.refresh()
            break
        stdscr.refresh()
        x += 1
        time.sleep(1)

# Color pairs for curses
COLOR_PLAYER = 1
COLOR_TREASURE = 2
COLOR_MOUNTAIN = 3
COLOR_WALL = 4
COLOR_DEFAULT = 5

def init_colors():
    """Initialize curses color pairs"""
    curses.init_pair(COLOR_PLAYER, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_TREASURE, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_MOUNTAIN, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_WALL, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_DEFAULT, curses.COLOR_WHITE, curses.COLOR_BLACK)

def print_map(stdscr, map, player):
    """Draw the map on the screen using curses"""
    stdscr.clear()
    for row_idx, line in enumerate(map):
        for col_idx, char in enumerate(line):
            if row_idx < stdscr.getmaxyx()[0] and col_idx < stdscr.getmaxyx()[1]:
                color_pair = COLOR_DEFAULT
                if char == '@':
                    color_pair = COLOR_PLAYER
                elif char == 'T':
                    color_pair = COLOR_TREASURE
                elif char == 'M':
                    color_pair = COLOR_MOUNTAIN
                elif char == 'W':
                    color_pair = COLOR_WALL
                
                try:
                    stdscr.addch(row_idx, col_idx, ord(char), curses.color_pair(color_pair))
                except curses.error:
                    pass  # Ignore errors when writing outside screen bounds
    stdscr.refresh()

def update_player_position(stdscr, player, old_x, old_y, map):
    """Update only the previous and current player cells to avoid full-screen redraws."""
    import curses
    maxy, maxx = stdscr.getmaxyx()

    # Draw the character that should be at the old position
    try:
        if 0 <= old_x < maxy and 0 <= old_y < maxx:
            ch = map[old_x][old_y]
            color_pair = COLOR_DEFAULT
            if ch == '@':
                color_pair = COLOR_PLAYER
            elif ch == 'T':
                color_pair = COLOR_TREASURE
            elif ch == 'M':
                color_pair = COLOR_MOUNTAIN
            elif ch == 'W':
                color_pair = COLOR_WALL
            stdscr.addch(old_x, old_y, ord(ch), curses.color_pair(color_pair))
    except curses.error:
        pass

    # Draw the player at the new position
    try:
        if 0 <= player.x < maxy and 0 <= player.y < maxx:
            stdscr.addch(player.x, player.y, ord('@'), curses.color_pair(COLOR_PLAYER))
    except curses.error:
        pass

    stdscr.refresh()

def move(stdscr, player, key, map):
    """Handle player movement with collision detection"""
    old_x, old_y = player.x, player.y
    
    if key == 'w' and player.x > 0 and map[player.x - 1][player.y] != 'M' and map[player.x - 1][player.y] != 'W':
        player.x -= 1
    elif key == 'a' and player.y > 0 and map[player.x][player.y - 2] != 'M' and map[player.x][player.y - 2] != 'W':
        player.y -= 2
    elif key == 's' and player.x < len(map) - 1 and map[player.x + 1][player.y] != 'M' and map[player.x + 1][player.y] != 'W':
        player.x += 1
    elif key == 'd' and player.y < len(map[player.x]) - 2 and map[player.x][player.y + 2] != 'M' and map[player.x][player.y + 2] != 'W':
        player.y += 2
    else:
        return
    
    # Update map state
    map[old_x][old_y] = player.old_char
    player.old_char = map[player.x][player.y]
    map[player.x][player.y] = '@'
    
    # Update only the changed cells to reduce flicker
    update_player_position(stdscr, player, old_x, old_y, map) 

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

def random_fight(stdscr, player, map):
    """Handle random encounters during movement"""
    if random.random() < 0.005:
        stdscr.clear()
        stdscr.refresh()
        fight_to_death(player.clazz, monster_random(), stdscr)
        time.sleep(3)
        if player.clazz.hp < 1:
            stdscr.clear()
            stdscr.addstr(0, 0, "Game Over.")
            stdscr.refresh()
            time.sleep(2)
            return False
        print_map(stdscr, map, player)
    return True

def change_map(stdscr, player, map, map_type):
    """Handle map transitions (e.g., entering caves)"""
    if map_type == 'C':
        new_map = gen_cave(16, 16)
        old_x, old_y = player.x, player.y
        player.x, player.y = 0, 0
        older_char = player.old_char
        player.old_char = 'E'
        game_loop(stdscr, player, new_map)
        player.old_char = 'c'
        player.x, player.y = old_x, old_y
        print_map(stdscr, map, player)

### Trying to make pynput work, starting from importing
import os
import time

def game_loop(stdscr, player, map):
    """Main game loop using curses for input and rendering"""
    # Configure curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.timeout(20)  # 20ms timeout for input
    
    init_colors()
    print_map(stdscr, map, player)
    
    running = True
    while running:
        try:
            key = stdscr.getch()
            if key != curses.ERR:  # If a key was pressed
                if key == ord('q') or key == ord('0'):  # Quit on 'q' or '0'
                    running = False
                elif key in [ord('w'), ord('a'), ord('s'), ord('d')]:  # Movement keys
                    move(stdscr, player, chr(key), map)
                    if player.old_char == 'E':  # Exit cave
                        running = False
                    else:
                        change_map(stdscr, player, map, player.old_char)
                        if not random_fight(stdscr, player, map):
                            running = False
                elif key == ord('0'):
                    running = False
        except KeyboardInterrupt:
            running = False
    
    curses.curs_set(1)  # Show cursor again

def find_start(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if (map[i][j] == '@'):
                return i, j
    return len(map) / 2, len(map[0]) / 2 # start at the middle of the map if player not found

import time, os, sys, random, platform, curses
from colorama import just_fix_windows_console

# TODO: change cursor repaint logic so that it doesn't break if screen is not big enough
# probably curses-python

def main(stdscr):
    """Main function - wraps game initialization with curses"""
    init_colors()
    
    try:
        file = open("assets/overworld.map") # starting map
        lines = file.read() 
        map = [list(line) for line in lines.split('\n')]
        x, y = find_start(map)
        player = Player(x, y, Warrior("Potat the Lost", 35))
        game_loop(stdscr, player, map)
    except KeyboardInterrupt:
        pass
    finally:
        curses.curs_set(1)  # Show cursor

if __name__ == "__main__":
    curses.wrapper(main)

###CAVE PART - this is cool

#MONSTERS

#TODO: a box with encounter appears on the right side of the map without closing it? @ frozen while it open
#TODO: log showing what has happened - you entered a cave, you met an enemy - on the side. SEE, I DIDN'T FORGET
#TODO: maybe add small pics showing enemy during encounter - bat = \/O\/ - maybe sponder = /\o/\
#TODO: a randomizer that will choose an enemy for encounter
#TODO: break terminal into small compartments using curses, and implement inventory into one of them.
