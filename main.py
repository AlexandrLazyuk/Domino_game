#!/usr/bin/env python

#------------------IMPORTS------------------------
import pygame
from pygame.locals import *
from random import randrange
from sys import exit
from time import sleep
from computer import *
from Tile import *
from os import path

#------------------Constants----------------------
main_window_resolution = (1024, 768)

HIDE_TILE_COLOR = (140,95,22)

INNER_COLOR = (159, 127, 87)
OUTER_COLOR = (109, 72, 31)

#-------------------Variables--------------------------
__PASS__ = 0
NUMBER_OF_PLAYERS = 2

HUMAN_TILES = []
COMPUTER_TILES = []

PLAYED_TILES = []

REPLAY_BUTTON_PLACE = [0, 0]
EXIT_BUTTON_PLACE = [0, 0]
PASS_BUTTON_PLACE = [0, 0]

TOTAL_X = {"left":0, "right":0}
TOTAL_Y = {"up":0, "down":0}

this_is_first_DOWN_tile = 1
this_is_first_LEFT_tile = 1
this_is_first_UP_tile = 1
this_is_first_RIGHT_tile = 1

GAME_OVER = 0

BOTH_SIDES = 0

ARGUMENTATIVE_TILE = None
ARGUMENTATIVE_RESULT = None

PASS_BUTTON_STATUS = 0

#----------------------------------------------------------------------------

def seticon(iconname):
    """
    give an iconname, a bitmap sized 32x32 pixels, black (0,0,0) will be alpha channel

    the windowicon will be set to the bitmap, but the black pixels will be full alpha channel

    can only be called once after pygame.init() and before somewindow = pygame.display.set_mode()
    """
    icon=pygame.Surface((32,32))
    icon.set_colorkey((0,0,0))
    rawicon=pygame.image.load(iconname)
    for i in range(0,32):
        for j in range(0,32):
            icon.set_at((i,j), rawicon.get_at((i,j)))
    pygame.display.set_icon(icon)

#----------------------------------------------------------------------------

def generate_tiles():
    """ generate_tiles()
        this function takes nothing and returns a complete dominos list of 28 elements
    each element of this list is a "tuple".
    """
    # TODO (DONE) make two loops instead of this mess :D
    temp = []
    for i in range(0,7):
        for j in range(i,7):
            temp.append((i,j))
    return temp

#----------------------------------------------------------------------------

def distribute_tiles(tiles_set, players_count):
    """
    distribute_tiles(tiles_set, players_count)
        Takes a complete dominos list and returns a list of lists
        each list contains 7 tiles as Tuples.
        WARNING! "players_count" should be less than 4.

        in this function we faced type of lists called list of lists
        for more clarify i will put example
        >>> count = 3
        >>> list = [[] for x in range(count)]
        >>> print list
        [[], [], []]
        this list were contain 3 lists each list for one player :D
    """
    #check the validity of the number of players
    if players_count > 4 :
        raise ValueError

    #create an empty list of lists, to hold the players' tiles
    final_list=[ [] for x in range(players_count) ]

    #fill the "final_list" with random tiles
    for i in range(0, 7):
        for j in range(players_count):
            random_number = randrange(0, len(tiles_set))
            # TODO (DONE) use the 'pop' method instead of the following active two lines
            final_list[j].append(tiles_set.pop(random_number))

    return final_list

#----------------------------------------------------------------------------

def draw_bg(screen):
    """
    draw_bg()
        drawing the board background
    """

    #load all images
    pass_button = pygame.image.load("images/deactive_pass.png")
    replay_button = pygame.image.load("images/normal_replay.png")
    exit_button = pygame.image.load("images/normal_exit.png")
    computer_tiles_background = pygame.image.load("images/computer_tiles_background.png")
    human_tiles_background = pygame.image.load("images/human_tiles_background.png")
    center_image = pygame.image.load("images/center_image.png")

    #create and draw the center rectangle
    center_rectangle_start = (0, main_window_resolution[1]/4)
    center_rectangle_size = (main_window_resolution[0], main_window_resolution[1]/2)
    center_rectangle = Rect(center_rectangle_start, center_rectangle_size)
    pygame.draw.rect(screen, INNER_COLOR, center_rectangle)

    #draw the center image
    center_image_X = (main_window_resolution[0] - 780) / 2
    center_image_Y = (main_window_resolution[1] - 280) / 2
    screen.blit(center_image, (center_image_X, center_image_Y))

    #Draw the upper and lower rectangles
    upper_rectangle_start = (0, 0)
    upper_rectangle_size = (main_window_resolution[0], main_window_resolution[1]/4)

    lower_rectangle_Y = main_window_resolution[1] - main_window_resolution[1]/4
    lower_rectangle_start = (0, lower_rectangle_Y)
    lower_rectangle_size = (main_window_resolution[0], main_window_resolution[1]/4)

    upper_rectangle = Rect(upper_rectangle_start, upper_rectangle_size)
    lower_rectangle = Rect(lower_rectangle_start, lower_rectangle_size)

    pygame.draw.rect(screen, OUTER_COLOR, upper_rectangle)
    pygame.draw.rect(screen, OUTER_COLOR, lower_rectangle)

    #draw the background behind tiles
    X_start = (main_window_resolution[0]- 565) / 2

    computer_tiles_background_Y = (main_window_resolution[1] / 8) - 60
    human_tiles_background_Y = main_window_resolution[1] - (main_window_resolution[1]/8) - 60

    screen.blit(computer_tiles_background, (X_start, computer_tiles_background_Y))
    screen.blit(human_tiles_background, (X_start, human_tiles_background_Y))

    #draw the buttons
    REPLAY_BUTTON_PLACE[0] = ((main_window_resolution[0] - 565) / 2 - 81) /2
    EXIT_BUTTON_PLACE[0] = ((main_window_resolution[0] - 565) / 2 - 81) /2

    REPLAY_BUTTON_PLACE[1] = human_tiles_background_Y + 25
    EXIT_BUTTON_PLACE[1] = REPLAY_BUTTON_PLACE[1] + 40

    PASS_BUTTON_PLACE[0] = ((main_window_resolution[0]- 565)/2 + 565) + ((main_window_resolution[0]- 565)/2 - 99)/2
    PASS_BUTTON_PLACE[1] = human_tiles_background_Y + 37

    screen.blit(replay_button, (REPLAY_BUTTON_PLACE[0], REPLAY_BUTTON_PLACE[1]))
    screen.blit(exit_button, (EXIT_BUTTON_PLACE[0], EXIT_BUTTON_PLACE[1]))
    screen.blit(pass_button, (PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1]))

    #refresh the pygame display
    pygame.display.update()

#----------------------------------------------------------------------------

def draw_tiles(screen):
    """
    draw_tiles()
        this function draws both computer's and human's tiles
    """
    #Print the human Tiles on the screen
    for i in range(len(HUMAN_TILES)):
        current_tile = HUMAN_TILES[i][0]
        current_position = HUMAN_TILES[i][1]
        temp_tile = Tile(current_tile[0], current_tile[1], screen, current_position[0], current_position[1])
        temp_tile.show_vertical()

    #Print the Computer Tiles (up-side-down)
    # TODO (DONE) changing the Computer tiles image
    for i in range(len(COMPUTER_TILES)):
        current_position = COMPUTER_TILES[i][1]
        temp_tile = Tile(9, 8, screen, current_position[0], current_position[1])
        temp_tile.show_vertical()

#----------------------------------------------------------------------------

def initialize(screen):
    """
    initialize(screen)
        This function takes a "display" and creates the tiles sets for
        the players then displays them on the "display"
    """
    #Generate two random Tile lists
    complete_tiles_set = generate_tiles()
    both_players_tiles = distribute_tiles(complete_tiles_set, NUMBER_OF_PLAYERS)

    #Constructing the Human Tiles list
    identifier = 0

    x_start = (main_window_resolution[0]- 565) / 2 + 25
    x_end = x_start + 514
    y_start = main_window_resolution[1] - (main_window_resolution[1]/8) - 34

    for i in range(x_start, x_end, 80):
        HUMAN_TILES.append([both_players_tiles[0][identifier], (i, y_start)])
        identifier += 1


    #Constructing the Computer Tiles list
    identifier = 0
    y_start = (main_window_resolution[1] / 8) -34

    for i in range(x_start, x_end, 80):
        COMPUTER_TILES.append([both_players_tiles[1][identifier], (i, y_start)])
        identifier += 1


    #draw the background and dominos tiles on the screen
    draw_bg(screen)
    draw_tiles(screen)

#----------------------------------------------------------------------------

def clicked_on_tile(mouse_position, tile_position):
    """
    clicked_on_tile(mouse_position, tile_position)
        takes two positions as "tuples", and returns True if the
        mouse is on the tile, and returns False otherwise.
    """
    if mouse_position[0] > tile_position[0]\
    and mouse_position[0] < (tile_position[0] + 34)\
    and mouse_position[1] > tile_position[1]\
    and mouse_position[1] < (tile_position[1] + 68) :
        return True
    else :
        return False

#----------------------------------------------------------------------------

def tile_check(tile):

    right = 0
    left = 0
    right_flip = 0
    left_flip = 0

    #If this is the first tile to be played
    if len(PLAYED_TILES) == 0 :
        return tile, None

    #check if the tile can be played on the right
    if tile[0] == PLAYED_TILES[-1][0][1] :
        right = 1

    elif tile[1] == PLAYED_TILES[-1][0][1] :
        right = 1
        right_flip = 1

    #check if the tile can be played on the left
    if tile[1] == PLAYED_TILES[0][0][0] :
        left = 1

    elif tile[0] == PLAYED_TILES[0][0][0] :
        left = 1
        left_flip = 1


    #If the tile can be played on both sides
    if (right == 1) and (left == 1) :

        #construct empty result list
        result = []

        #Manage the right side
        if right_flip == 1 :
            result.extend([(tile[1], tile[0]), "right"])

        else :
            result.extend([tile, "right"])

        #Manage the left side
        if left_flip == 1 :
            result.extend([(tile[1], tile[0]), "left"])

        else :
            result.extend([tile, "left"])

        #return the result
        return result


    #If the tile can be played on the right side only
    elif right == 1 :
        if right_flip == 1 :
            return (tile[1], tile[0]), "right"
        else :
            return tile, "right"

    #If the tile can be played on the left side only
    elif left == 1 :
        if left_flip == 1 :
            return (tile[1], tile[0]), "left"
        else :
            return tile, "left"

    #If the tile isn't suitable
    else :
        return None

#----------------------------------------------------------------------------

def play(tile, screen, place = None):
    """
    play(tile, screen, place)
        this function takes a tile as a "tuple", display
        and a place ("left" or "right"). then draws the tile on the screen.

        example for the x_position to the last tile played on the left
        >>> b=[[(0,1),(100,200)],[(0,2),(300,400)],[(0,3),(500,600)]]
        >>> print b[0][1][0]
        100

        example for the y_position to the last tile played on the left
        >>> print b[0][1][1]
        200

        example for the x_position to the last tile played on the right
        >>> print b[-1][1][0]
        500

        example for the y_position to the last tile played on the right
        >>> print b[-1][1][1]
        600
    """

    #Initialize the flag that determines the orientation of the tile
    orientation = "horizontal"
    #Initialize the flag that determines if the tile would be painted reversed
    reverse_tile = 0

    #Initialize the place of the tile
    tile_x = 0
    tile_y = 0

    #make python recognize these variables as global
    global this_is_first_DOWN_tile
    global this_is_first_LEFT_tile
    global this_is_first_UP_tile
    global this_is_first_RIGHT_tile

    #set a variables determines if the tile is DUO or not
    tile_is_DUO = 0

    if tile[0] == tile[1] :
        tile_is_DUO = 1

    #check if this tile is the first tile to be played
    if len(PLAYED_TILES) == 0 :

        #check if the tile is DUO, then place it in the right place
        if tile_is_DUO:
            tile_x = main_window_resolution[0]/2 - 17
            tile_y = main_window_resolution[1]/2 - 34
            orientation = "vertical"

        else :
            tile_x = main_window_resolution[0]/2 - 34
            tile_y = main_window_resolution[1]/2 - 17

        #append the tile to the PLAYED_TILES list
        PLAYED_TILES.append([tile,(tile_x, tile_y)])

    #if the tile is going to be played in the left direction
    elif place == "left" :

        #make some variables to ease understanding the code
        previous_tile = PLAYED_TILES[0][0]
        previous_position = PLAYED_TILES[0][1]

        previous_tile_is_DUO = 0

        if previous_tile[0] == previous_tile[1] :
            previous_tile_is_DUO = 1

        #PLAY TO THE LEFT DIRECTION
        if TOTAL_X["left"] < main_window_resolution[0]/2 - 150 :

            if tile_is_DUO :
                TOTAL_X["left"] += 36
                orientation = "vertical"
                tile_x = previous_position[0] - 36
                tile_y = previous_position[1] - 17

            else :
                if previous_tile_is_DUO :
                    TOTAL_X["left"] += 70
                    tile_x = previous_position[0] - 70
                    tile_y = previous_position[1] + 17

                else :
                    TOTAL_X["left"] += 70
                    tile_x = previous_position[0] - 70
                    tile_y = previous_position[1]

        #reached the left end of the window
        else :

            #PLAY TO THE UP DIRECTION
            if TOTAL_Y["up"] < main_window_resolution[1]/4 -110 :

                #this is the first tile going to be played UP
                if this_is_first_UP_tile :
                    this_is_first_UP_tile = 0

                    #previous tile is DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["up"] += 104  #34 + 70
                        orientation = "vertical"
                        tile_x = previous_position[0]
                        tile_y = previous_position[1] - 70

                    #previous tile is NOT DUO
                    else :
                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] - 36
                            tile_y = previous_position[1] - 17

                            #act like the next tile will be the first UP,
                            #because if it didn't, the computer would think that
                            #this tile was horizontal, which causes calculation error
                            this_is_first_UP_tile = 1

                        else :
                            TOTAL_Y["up"] += 87  #17 + 70
                            orientation = "vertical"
                            tile_x = previous_position[0]
                            tile_y = previous_position[1] - 70

                #this is NOT the first tile that is going to be played UP
                else :

                    #previous tile is DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["up"] += 70
                        orientation = "vertical"
                        tile_x = previous_position[0] + 17
                        tile_y = previous_position[1] - 70

                    #previous tile is NOT DUO
                    else :
                        if tile_is_DUO :
                            TOTAL_Y["up"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] - 36

                        else :
                            TOTAL_Y["up"] += 70
                            orientation = "vertical"
                            tile_x = previous_position[0]
                            tile_y = previous_position[1] - 70

            #PLAY TO THE RIGHT DIRECTION
            else :

                #this is the first tile to be played RIGHT
                if this_is_first_RIGHT_tile :
                    this_is_first_RIGHT_tile = 0

                    #the previous tile was DUO
                    if previous_tile_is_DUO :
                        tile_x = previous_position[0] + 70
                        tile_y = previous_position[1]
                        reverse_tile = 1

                    #the previous tile was NOT DUO
                    else :
                        if tile_is_DUO :
                            TOTAL_Y["up"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] - 36

                            #act like the next tile will be the first UP,
                            #because if it didn't, the computer would think that
                            #this tile was horizontal, which causes calculation error
                            this_is_first_RIGHT_tile = 1

                        else :
                            #we will add 36 to TOTAL_Y["up"] because if we didn't, next
                            #time it would be considered "first time right" again
                            TOTAL_Y["up"] += 36
                            tile_x = previous_position[0] + 36
                            tile_y = previous_position[1]
                            reverse_tile = 1

                #this is NOT the first tile to be played RIGHT
                else :

                    #the previous tile was DUO
                    if previous_tile_is_DUO :
                        tile_x = previous_position[0] + 36
                        tile_y = previous_position[1] + 17
                        reverse_tile = 1

                    #the previous tile was NOT DUO
                    else :

                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] + 70
                            tile_y = previous_position[1] - 17

                        else :
                            tile_x = previous_position[0] + 70
                            tile_y = previous_position[1]
                            reverse_tile = 1

        #APPEND THE PLAYED TILE TO THE PLAYED_TILES LIST
        PLAYED_TILES.insert(0, [tile, (tile_x, tile_y)])


    #if the tile is going to be played in the right direction
    elif place == "right" :

        #make some variables to ease understanding the code
        previous_tile = PLAYED_TILES[-1][0]
        previous_position = PLAYED_TILES[-1][1]

        previous_tile_is_DUO = 0

        if previous_tile[0] == previous_tile[1] :
            previous_tile_is_DUO = 1

        #PLAY TO THE RIGHT DIRECTION
        if TOTAL_X["right"] < main_window_resolution[0]/2 - 150 :

            #if this tile is DUO
            if tile_is_DUO :
                TOTAL_X["right"] += 36
                orientation = "vertical"
                tile_x = previous_position[0] + 70
                tile_y = previous_position[1] - 17

            #if this tile is NOT DUO
            else :

                if previous_tile_is_DUO :
                    TOTAL_X["right"] += 70
                    tile_x = previous_position[0] + 36
                    tile_y = previous_position[1] + 17

                else :
                    TOTAL_X["right"] += 70
                    tile_x = previous_position[0] + 70
                    tile_y = previous_position[1]

        #reached the right end of the window
        else :

            #PLAY TO DOWN DIRECTION
            if TOTAL_Y["down"] < main_window_resolution[1]/4 - 110 :

                #this is the first tile to be played in the DOWN direction
                if this_is_first_DOWN_tile :
                    this_is_first_DOWN_tile = 0

                    #if the previous tile was DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 104  #34 + 70
                        orientation = "vertical"
                        tile_x = previous_position[0]
                        tile_y = previous_position[1] + 70

                    #if the previous tile was NOT DUO
                    else :

                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] + 70
                            tile_y = previous_position[1] - 17

                            #act like the next tile will be the first DOWN,
                            #because if it didn't, the computer would think that
                            #this tile was horizontal, which causes calculation error
                            this_is_first_DOWN_tile = 1

                        else :
                            TOTAL_Y["down"] += 87  #17 + 70
                            orientation = "vertical"
                            tile_x = previous_position[0] + 34
                            tile_y = previous_position[1] + 36

                #this is NOT the first tile to be played in the DOWN direction
                else :

                    #if the previous tile was DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 70
                        orientation = "vertical"
                        tile_x = previous_position[0] + 17
                        tile_y = previous_position[1] + 36

                    #if the previous tile was NOT DUO
                    else :

                        if tile_is_DUO :
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] + 36

                        else :
                            TOTAL_Y["down"] += 70
                            orientation = "vertical"
                            tile_x = previous_position[0]
                            tile_y = previous_position[1] + 70

            #PLAY TO LEFT DIRECTION (REVERSED TILES)
            else :

                #if this tile is the first tile to be played LEFT
                if this_is_first_LEFT_tile :
                    this_is_first_LEFT_tile = 0

                    #if the previous tile was DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 36
                        tile_x = previous_position[0] - 70
                        tile_y = previous_position[1]
                        reverse_tile = 1

                    ##if the previous tile was NOT DUO
                    else :

                        if tile_is_DUO :
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] + 70

                            #act like the next tile will be the first LEFT,
                            #because if it didn't, the computer would think that
                            #this tile was vertical, which causes calculation error
                            this_is_first_LEFT_tile = 1

                        else :
                            #we will add 36 to TOTAL_Y["up"] because if we didn't, next
                            #time it would be considered "first time right" again
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 70
                            tile_y = previous_position[1] + 34
                            reverse_tile = 1

                #if this tile is NOT the first tile to be played LEFT
                else :

                    #if the previous tile was DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 36
                        tile_x = previous_position[0] - 70
                        tile_y = previous_position[1] + 17
                        reverse_tile = 1

                    #if the previous tile was NOT DUO
                    else :

                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] - 36
                            tile_y = previous_position[1] - 17

                        else :
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 70
                            tile_y = previous_position[1]
                            reverse_tile = 1

        #ADD THE PLAYED TILE TO THE PLAYED_TILES LIST
        PLAYED_TILES.append([tile,(tile_x, tile_y)])


    #if the programmer didn't pass the place variable, raise an exception
    else :
        raise ValueError

    #Create a Tile object
    if reverse_tile :
        temp_tile = Tile(tile[1], tile[0], screen, tile_x, tile_y)
    else :
        temp_tile = Tile(tile[0], tile[1], screen, tile_x, tile_y)

    #show the tile according to it's suitable orientation
    if orientation == "horizontal" :
        temp_tile.show_horizontal()

    else :
        temp_tile.show_vertical()

#----------------------------------------------------------------------------

def computer_play(auto_player, screen):

    #identify __PASS__ as global variable
    global __PASS__

    playedtile_sound = path.join('sounds', 'playedtile.wav')
    playedtile_soundtrack = pygame.mixer.Sound(playedtile_sound)
    playedtile_soundtrack.set_volume(0.9)

    #Ask the computer to play
    chosen_tile = auto_player.play(PLAYED_TILES)

    if chosen_tile != "PASS" :
        final_tile = tile_check(chosen_tile[0])
        pygame.time.wait(1000)
        pygame.event.clear()
        play(final_tile[0], screen, final_tile[1])
        playedtile_soundtrack.play(0)
        hide_tile(chosen_tile[1][0], chosen_tile[1][1], screen)

        #set the __PASS__ flag to off
        __PASS__ = 0

        #refresh the display
        pygame.display.update()

    #if the computer said "PASS"
    else :

        #If the human said "PASS" last time, End the game
        if __PASS__ == 1 :
            END_GAME(screen)
            return

        #If the human didn't say "PASS" last time, set __PASS__ to 1
        else :
            ############
            __PASS__ = 1
            
            computer_note_x = main_window_resolution[0]/2 - 196
            computer_note_y = main_window_resolution[1]/2 - 190
            
            computer_note_img = pygame.image.load("images/computer_passed.png")
            clear_img = pygame.image.load("images/clear.png")
            
            note_sound = path.join('sounds', 'note.wav')
            note_soundtrack = pygame.mixer.Sound(note_sound)
            note_soundtrack.set_volume(0.9)
            
            note_soundtrack.play(0)
            screen.blit(computer_note_img,(computer_note_x,computer_note_y))
            pygame.display.update()
            pygame.time.wait(2000)
            screen.blit(clear_img,(computer_note_x,computer_note_y))


    #check if the human can't play.
    if not human_has_suitable_tile() :

        #if the computer passed last time, then the game is ended
        if __PASS__ == 1 :
            END_GAME(screen)

        #if the game isn't ended, change the pass button image to green
        else :
            switch_pass_button("enable", screen)

#----------------------------------------------------------------------------

def human_play(tile, exact_tile, screen, position, auto_player):

    global __PASS__

    playedtile_sound = path.join('sounds', 'playedtile.wav')
    playedtile_soundtrack = pygame.mixer.Sound(playedtile_sound)
    playedtile_soundtrack.set_volume(0.9)

    #play the human tile
    playedtile_soundtrack.play(0)
    play(exact_tile, screen, position)
    HUMAN_TILES.remove(tile)
    hide_tile(tile[1][0], tile[1][1], screen)

    #set the __PASS__ flag to off
    __PASS__ = 0

    #refresh the display before the computer plays
    #because the computer will sleep for one second
    pygame.display.update()

    #check if the human finished his tiles, end the game
    if len(HUMAN_TILES) == 0 :
        END_GAME(screen)

    #if the human didn't finish his tiles
    else :

        #ask the computer to play
        computer_play(auto_player, screen)

        #check if the computer finished his tiles, end the game
        if len(COMPUTER_TILES) == 0 :
            END_GAME(screen)

        #check if the human can't play.
        elif not human_has_suitable_tile() :

            #if the computer passed last time, then the game is ended
            if __PASS__ == 1 :
                END_GAME(screen)

            #if the game isn't ended, change the pass button image to green
            else :
                switch_pass_button("enable", screen)

#----------------------------------------------------------------------------

def hide_tile(x, y, screen):
    hiding_rectangle = Rect(x, y, 34, 68)
    pygame.draw.rect(screen, HIDE_TILE_COLOR, hiding_rectangle)

#----------------------------------------------------------------------------

def clear_area(x, y, width, height, screen, fill_color):
    hiding_rectangle = Rect(x, y, width, height)
    pygame.draw.rect(screen, fill_color, hiding_rectangle)

#----------------------------------------------------------------------------

def switch_pass_button(action, screen):

    #initialize the PASS_BUTTON_STATUS as global variable
    global PASS_BUTTON_STATUS

    #the action is to disable pass button
    if action == "enable" :

        #clear the place of the pass button
        clear_area(PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1], 99, 44, screen, OUTER_COLOR)

        #change the pass button image back to green
        pass_button_image = pygame.image.load("images/active_pass.png")
        screen.blit(pass_button_image, (PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1]))

        #change the PASS_BUTTON_STATUS to be enabled
        PASS_BUTTON_STATUS = 1

        #refresh the display
        pygame.display.update()


    #the action is to enable the pass button
    elif action == "disable" :

        #clear the place of the pass button
        clear_area(PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1], 99, 44, screen, OUTER_COLOR)

        #change the pass button image back to red
        pass_button_image = pygame.image.load("images/deactive_pass.png")
        screen.blit(pass_button_image, (PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1]))

        #change the PASS_BUTTON_STATUS to be disabled
        PASS_BUTTON_STATUS = 0

        #refresh the display
        pygame.display.update()


    #if the programmer didn't pass the action correctly
    else :
        raise ValueError

#----------------------------------------------------------------------------

def human_has_suitable_tile():
    """
    human_has_suitable_tile()
        this function returns True if there is any suitable
        tile to be played, in the HUMAN_TILES list.
    """

    #If this is the first tile to be played, then the human
    #has some suitable tiles. So, return True.
    if len(PLAYED_TILES) == 0 :
        return True

    left_value = PLAYED_TILES[0][0][0]
    right_value = PLAYED_TILES[-1][0][1]

    for tile in HUMAN_TILES :

        #if we found a suitable tile, stop and return True
        if (left_value in tile[0]) or (right_value in tile[0]) :
            return True

        else :
            continue

    #if the loop finished without finding any suitable tiles, return False
    return False

#----------------------------------------------------------------------------

def left_or_right(screen):

    left_image = pygame.image.load("images/left.png")
    right_image = pygame.image.load("images/right.png")

    x1 = PASS_BUTTON_PLACE[0] + 5
    y1 = PASS_BUTTON_PLACE[1] - 30

    x2 = PASS_BUTTON_PLACE[0] + 62
    y2 = PASS_BUTTON_PLACE[1] - 30

    for i in range(2) :

        screen.blit(left_image,(x1, y1))
        screen.blit(right_image,(x2, y2))

        pygame.display.update()

        pygame.time.wait(200)

        clear_area(x1, y1, 100, 22, screen, OUTER_COLOR)

        pygame.display.update()

        pygame.time.wait(200)

    screen.blit(left_image,(x1, y1))
    screen.blit(right_image,(x2, y2))

#----------------------------------------------------------------------------

def check_if_clicked_on_exit(screen, x, y, check_for_popup = 0):

    #Checking whether the user clicked on the REPLAY button
    if x > REPLAY_BUTTON_PLACE[0] and x < (REPLAY_BUTTON_PLACE[0] + 81)\
     and y > REPLAY_BUTTON_PLACE[1] and y< (REPLAY_BUTTON_PLACE[1] + 29) :

        pressed_replay = pygame.image.load("images/pressed_replay.png")
        screen.blit(pressed_replay, (REPLAY_BUTTON_PLACE[0], REPLAY_BUTTON_PLACE[1]))
        pygame.display.update()
        pygame.time.wait(100)
        RESET_GAME()


    #Checking whether the user clicked on a the EXIT button
    elif x > EXIT_BUTTON_PLACE[0] and x < (EXIT_BUTTON_PLACE[0] + 81)\
     and y > EXIT_BUTTON_PLACE[1] and y< (EXIT_BUTTON_PLACE[1] + 29) :

        pressed_exit = pygame.image.load("images/pressed_exit.png")
        screen.blit(pressed_exit,(EXIT_BUTTON_PLACE[0], EXIT_BUTTON_PLACE[1]))
        pygame.display.update()
        pygame.time.wait(100)
        exit()


    #if the user want to check on the POPUP message too
    if check_for_popup == 1 :

        #Load the highlight image
        button_highlight_img = pygame.image.load("images/on_clicked_button.png")

        #load the needed sound files
        replay_sound = path.join('sounds', 'replay.wav')
        replay_soundtrack = pygame.mixer.Sound(replay_sound)
        replay_soundtrack.set_volume(0.9)

        cancelReplay_sound = path.join('sounds', 'cancel_replay.wav')
        cancelReplay_soundtrack = pygame.mixer.Sound(cancelReplay_sound)
        cancelReplay_soundtrack.set_volume(0.9)

        #get the place of the POP UP message
        popup_x = main_window_resolution[0]/2 - 252
        popup_y = main_window_resolution[1]/2 - 173

        #if the player clicked on the exit button on the POP UP message
        if x > (popup_x + 113) and x < (popup_x + 230)\
         and y > (popup_y + 286) and y< (popup_y + 334) :
            screen.blit(button_highlight_img,(popup_x + 115,popup_y + 288))
            cancelReplay_soundtrack.play(0)
            pygame.display.update()
            pygame.time.wait(100)
            #exit the game
            exit()

        #if the player clicked on the replay button on the POP UP message
        elif x > (popup_x + 278) and x < (popup_x + 395)\
         and y > (popup_y + 288) and y< (popup_y + 336) :
            screen.blit(button_highlight_img,(popup_x + 278,popup_y + 288))
            replay_soundtrack.play(0)
            pygame.display.update()
            pygame.time.wait(500)
            #reset the game
            RESET_GAME()

#----------------------------------------------------------------------------

def check_if_clicked_on_pass(screen, auto_player, x, y):

    global __PASS__

    #Checking whether the user clicked on a the PASS button
    if x > PASS_BUTTON_PLACE[0] and x < (PASS_BUTTON_PLACE[0] + 99)\
     and y > PASS_BUTTON_PLACE[1] and y < (PASS_BUTTON_PLACE[1] + 44):

        #if the human has any suitable tiles to play, ignore him
        if human_has_suitable_tile() :

            #load the required image
            bad_pass = pygame.image.load("images/bad_pass.png")
            clear_img = pygame.image.load("images/clear.png")

            #note message coordinates
            note_x = main_window_resolution[0]/2 - 196
            note_y = main_window_resolution[1] - main_window_resolution[1]/4 -35

            #load the sound file
            note_sound = path.join('sounds', 'note.wav')
            note_soundtrack = pygame.mixer.Sound(note_sound)
            note_soundtrack.set_volume(0.9)

            #view the note and play the sound
            note_soundtrack.play(0)
            screen.blit(bad_pass,(note_x, note_y))
            pygame.display.update()
            pygame.time.wait(2000)
            screen.blit(clear_img,(note_x,note_y))

        #if the human DOESN'T have any suitable tiles to played.
        else :
            #check if the __PASS__ flag is ON, end the game
            if __PASS__ == 1 :
                END_GAME(screen)

            else :

                #set the __PASS__ flag to on
                __PASS__ = 1

                #disable the pass button
                switch_pass_button("disable", screen)

                #ask the computer to play
                computer_play(auto_player, screen)

                #check if the computer finished his tiles, end the game
                if len(COMPUTER_TILES) == 0 :
                    END_GAME(screen)

        return True

    else :
        return False

#----------------------------------------------------------------------------

def score_count(WHOS_TILE):
    tiles_length = len(WHOS_TILE)
    tiles_count = 0
    for i in range(0, tiles_length):
        tiles_count += WHOS_TILE[i][0][0]
        tiles_count += WHOS_TILE[i][0][1]
    return tiles_count

#----------------------------------------------------------------------------

def END_GAME(screen):

    #constructing game_over_bg designs
    game_over_bg = pygame.image.load("images/game_over_bg.png")
    won_game_img = pygame.image.load("images/you_won_img.png")
    lose_game_img = pygame.image.load("images/you_lose_img.png")
    game_drawn_img = pygame.image.load("images/drawn_img.png")

    # constructing x,y for the game_over_bg
    draw_x = main_window_resolution[0]/2 - 252
    draw_y = main_window_resolution[1]/2 - 173

    #identify GAME_OVER as global variable
    global GAME_OVER

    #set the GAME_OVER flag to on
    GAME_OVER = 1

    #count both human's and computer's points
    human_score = score_count(HUMAN_TILES)
    computer_score = score_count(COMPUTER_TILES)


    #if the human won
    if human_score < computer_score :

        winner_sound = path.join('sounds', 'game_over_win.wav')
        winner_soundtrack = pygame.mixer.Sound(winner_sound)
        winner_soundtrack.set_volume(0.9)

        winner_soundtrack.play(0)
        screen.blit(game_over_bg,(draw_x,draw_y))
        screen.blit(won_game_img,(draw_x + 120, draw_y + 220))

    #if the computer won
    elif human_score > computer_score :

        loser_sound = path.join('sounds', 'game_over_lose.wav')
        loser_soundtrack = pygame.mixer.Sound(loser_sound)
        loser_soundtrack.set_volume(0.9)

        loser_soundtrack.play(0)
        screen.blit(game_over_bg,(draw_x,draw_y))
        screen.blit(lose_game_img,(draw_x + 141, draw_y + 220))

    #if the game ended draw
    else :

        nonwinner_sound = path.join('sounds', 'none_winer.wav')
        nonwinner_soundtrack = pygame.mixer.Sound(nonwinner_sound)
        nonwinner_soundtrack.set_volume(0.9)

        nonwinner_soundtrack.play(0)
        screen.blit(game_over_bg,(draw_x,draw_y))
        screen.blit(game_drawn_img,(draw_x + 187, draw_y + 220))


    #constructing the font score_text and render it to the screen
    font = pygame.font.SysFont("arial", 25)
    screen.blit(font.render(str(human_score),True,(0,0,0)),(draw_x + 365,draw_y + 113))
    screen.blit(font.render(str(computer_score),True,(0,0,0)),(draw_x + 365,draw_y + 166))

#----------------------------------------------------------------------------

def RESET_GAME():

    global __PASS__
    global NUMBER_OF_PLAYERS
    global HUMAN_TILES
    global COMPUTER_TILES

    global PLAYED_TILES

    global REPLAY_BUTTON_PLACE
    global EXIT_BUTTON_PLACE
    global PASS_BUTTON_PLACE

    global TOTAL_X
    global TOTAL_Y

    global this_is_first_DOWN_tile
    global this_is_first_LEFT_tile
    global this_is_first_UP_tile
    global this_is_first_RIGHT_tile

    global GAME_OVER

    global BOTH_SIDES

    global ARGUMENTATIVE_TILE
    global ARGUMENTATIVE_RESULT

    global PASS_BUTTON_STATUS


    __PASS__ = 0
    NUMBER_OF_PLAYERS = 2

    HUMAN_TILES = []
    COMPUTER_TILES = []

    PLAYED_TILES = []

    REPLAY_BUTTON_PLACE = [0, 0]
    EXIT_BUTTON_PLACE = [0, 0]
    PASS_BUTTON_PLACE = [0, 0]

    TOTAL_X = {"left":0, "right":0}
    TOTAL_Y = {"up":0, "down":0}

    this_is_first_DOWN_tile = 1
    this_is_first_LEFT_tile = 1
    this_is_first_UP_tile = 1
    this_is_first_RIGHT_tile = 1

    GAME_OVER = 0

    BOTH_SIDES = 0

    ARGUMENTATIVE_TILE = None
    ARGUMENTATIVE_RESULT = None

    PASS_BUTTON_STATUS = 0
    main()

#----------------------------------------------------------------------------

def main():

    #identify the global variables
    global __PASS__
    global GAME_OVER
    global BOTH_SIDES
    global ARGUMENTATIVE_TILE
    global ARGUMENTATIVE_TILE_CHECK_RESULT

    #note message coordinates
    note_x = main_window_resolution[0]/2 - 196
    note_y = main_window_resolution[1] - main_window_resolution[1]/4 -35

    #Initialize PyGame
    pygame.init()

    #adding window icon
    seticon('images/icon.png')

    #create the Main window
    screen = pygame.display.set_mode(main_window_resolution,FULLSCREEN, 32)
    pygame.display.set_caption("Dominos!")

    #load the sound file
    note_sound = path.join('sounds', 'note.wav')
    note_soundtrack = pygame.mixer.Sound(note_sound)
    note_soundtrack.set_volume(0.9)

    #load needed images
    bad_tile = pygame.image.load("images/bad_tile.png")
    clear_img = pygame.image.load("images/clear.png")

    #initialize the game
    initialize(screen)
    auto_player = computer(COMPUTER_TILES)
#########################################################
#    computer_note_x = main_window_resolution[0]/2 - 196
#    #computer_note_y = main_window_resolution[1] - main_window_resolution[1]/4 -295
#    computer_note_y = main_window_resolution[1]/2 - 190
#    computer_note_img = pygame.image.load("images/computer_passed.png")
#    
#    screen.blit(computer_note_img,(computer_note_x,computer_note_y))
#    
#####################  MAIN LOOP  #######################

    while True:
        #Handling PyGame events
        event = pygame.event.wait()

        #Handling the QUIT signal
        if event.type == QUIT:
            exit()

        #if the game has ended.
        elif GAME_OVER == 1 :

            #check only on the "MOUSEBUTTONDOWN" event if it clicked on the exit button
            if event.type == MOUSEBUTTONDOWN :

                #get the mouse position
                x, y = event.pos

                #check if the user clicked on the exit or replay buttons
                check_if_clicked_on_exit(screen, x, y, 1)



        #Handling the Mouse Events IF THE PLAYER CAN PLAY ON BOTH SIDES
        elif BOTH_SIDES == 1 :

            if event.type == MOUSEBUTTONDOWN :

                #get the mouse position
                x, y = event.pos

                #check if the user clicked on the exit or replay buttons
                check_if_clicked_on_exit(screen, x, y)

                #get the place of the arrows
                x1 = PASS_BUTTON_PLACE[0] + 5
                y1 = PASS_BUTTON_PLACE[1] - 30
                x2 = PASS_BUTTON_PLACE[0] + 62
                y2 = PASS_BUTTON_PLACE[1] - 30

                #if the user chose to play to the left
                if x > x1 and x < (x1 + 30) and y > y1 and y < (y1 + 22) :

                    #clear the arrows from the screen
                    clear_area(x1, y1, 100, 22, screen, OUTER_COLOR)
                    pygame.display.update()
                    BOTH_SIDES = 0

                    human_play(ARGUMENTATIVE_TILE, ARGUMENTATIVE_RESULT[2], screen, ARGUMENTATIVE_RESULT[3], auto_player)

                #if the user chose to play to the right
                elif x > x2 and x < (x2 + 30) and y > y2 and y < (y2 + 22) :

                    #clear the arrows from the screen
                    clear_area(x1, y1, 100, 22, screen, OUTER_COLOR)
                    pygame.display.update()
                    BOTH_SIDES = 0

                    human_play(ARGUMENTATIVE_TILE, ARGUMENTATIVE_RESULT[0], screen, ARGUMENTATIVE_RESULT[1], auto_player)



        #Handling the Mouse Events IF THE GAME IS STILL RUNNING
        elif event.type == MOUSEBUTTONDOWN :

            #get the mouse position
            x,y = event.pos

            check_if_clicked_on_exit(screen, x, y)

            #Checking whether the user clicked on a the PASS button
            if check_if_clicked_on_pass(screen, auto_player, x, y):
                continue

            #check if the user clicked on a tile
            else :

                #loop over the HUMA_TILES
                for tile in HUMAN_TILES :

                    #if the human clicked on a tile
                    if clicked_on_tile(event.pos, tile[1]):

                        #check where to play the tile
                        result = tile_check(tile[0])

                        #if the user clicked on a NON-SUITABLE tile
                        if result is None :
                            note_soundtrack.play(0)
                            screen.blit(bad_tile,(note_x,note_y))
                            pygame.display.update()
                            pygame.time.wait(2000)
                            screen.blit(clear_img,(note_x,note_y))

                        #if the user clicked on a suitable
                        elif len(result) == 2 :
                            human_play(tile, result[0], screen, result[1], auto_player)

                        #if the tile can be played on both sides
                        elif len(result) == 4 :
                            BOTH_SIDES = 1
                            ARGUMENTATIVE_TILE = tile
                            ARGUMENTATIVE_RESULT = result
                            left_or_right(screen)
        
        # hit escape to exit
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit() 

        pygame.display.update()


#run the game if the module was called independently
if __name__ == "__main__":
    main()


