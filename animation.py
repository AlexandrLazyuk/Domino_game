#!/usr/bin/env python
import pygame
from pygame.locals import *


class Animate(object):
    
    def __init__(self,tile,start_mov,end_move,screen,bg):
        
        self._tile = tile
        self._start_move = start_mov
        self._end_move = end_move
        
        start_mov = [0,0]
        
        Tile_Moved = self._tile.get_rect()
        
        while True:
            
            Tile_Moved = Tile_Moved.move(start_mov)
            if Tile_Moved[0] < end_move:
                start_mov[0] += .01
                
            else:
                Tile_Moved[0] == end_move
            
            screen.blit(bg,Tile_Moved)
            pygame.display.update()
            