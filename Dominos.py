#!/usr/bin/env python

import pygame
from pygame.locals import *
from sys import exit
from main import *
from os import environ,path


class splashWindow(object):
 
    def __init__(self):
        """
        __init__(self)
            this function will initiate the startwindow
        """
        environ['SDL_VIDEO_CENTERED']='1'
        pygame.init()
        seticon('images/icon.png')
        start_screen = pygame.display.set_mode((498,501),NOFRAME,32)
        init_background = pygame.image.load("images/init_bg.png").convert()
        pygame.display.set_caption("Dominoes!")
        onQuite_clicked_img = pygame.image.load("images/onclicked1.png")
        onenjoy_clicked_img = pygame.image.load("images/onclicked2.png")
        
        bg_sound = path.join('sounds','bg.wav')
        soundtrack = pygame.mixer.Sound(bg_sound)
        soundtrack.set_volume(0.9)
        soundtrack.play(-1)
        
        enjoy_sound = path.join('sounds','enjoy.wav')
        enjoyTick = pygame.mixer.Sound(enjoy_sound)
        enjoyTick.set_volume(0.9)

        quit_sound = path.join('sounds','quit.wav')
        quitTick = pygame.mixer.Sound(quit_sound)
        quitTick.set_volume(0.9)
                
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                     
                if event.type == MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if x >= 172 and x <= 320 and y >= 435 and y<=480:
                        start_screen.blit(onenjoy_clicked_img,(190,438))
                        enjoyTick.play(0)
                        pygame.display.update()
                        pygame.time.wait(500)
                        main()
                    
                    if x >= 324 and x <= 423 and y >= 327 and y<=369:
                        start_screen.blit(onQuite_clicked_img,(317,322))
                        quitTick.play(1)
                        pygame.display.update()
                        exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_KP_ENTER or event.key == K_SPACE:
                        enjoyTick.play(0)
                        main()
                        
                    if event.key == K_ESCAPE:
                        quitTick.play(0)
                        exit()
                        
            
            start_screen.blit(init_background,(0,0))
            pygame.display.update()

if __name__ == '__main__':
    splashWindow()
            
        
        