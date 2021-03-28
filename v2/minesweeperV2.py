# coding=utf-8
import pygame
import time
from sys import exit
from minesweeper import game_init


WIDTH = 8
HEIGHT = 8
MINES = 10
INITIAL = True
GAMEOVER = False
TIME_COUNT_BEGIN = False

if __name__ == '__main__':

    while True:
        time.sleep(0.002)

        if INITIAL:
            INITIAL = False
            GAMEOVER = False
            TIME_COUNT_BEGIN = False
            screen, face, gridgroup, time_count, mine_count, menu_bar = game_init(WIDTH, HEIGHT, MINES)

        if not GAMEOVER:

            if TIME_COUNT_BEGIN:
                time_now = time.time() - start_time
                time_count.draw((int(time_now) + 1))
            elif gridgroup.count_open > 0:
                start_time = time.time()
                TIME_COUNT_BEGIN = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == 283:
                    INITIAL = True
                elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
                    if gridgroup.rect.collidepoint(event.pos):
                        gridgroup.on_event(event, face, mine_count)
                    elif face.rect.collidepoint(event.pos):
                        if face.on_event(event) == 'RESTART':
                            INITIAL = True
                    elif menu_bar.rect.collidepoint(event.pos):
                        menu_bar.on_event(event)
                    else:
                        face.reset()
                        gridgroup.reset(event)
                        menu_bar.reset(event)

            if menu_bar.real_menu:
                if not menu_bar.q_out.empty():
                    info = menu_bar.q_out.get()
                    if info['type'] == 'change_level':
                        WIDTH = info['width']
                        HEIGHT = info['height']
                        MINES = info['mines']
                        INITIAL = True

            if gridgroup.on_mine:
                GAMEOVER = True

            if len(gridgroup.grids) - MINES == gridgroup.count_open:
                GAMEOVER = True

            pygame.display.update()
        else:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN and event.key == 283:
                INITIAL = True

            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
                if face.rect.collidepoint(event.pos):
                    if face.on_event(event) == 'RESTART':
                        INITIAL = True
                elif menu_bar.rect.collidepoint(event.pos):
                    menu_bar.on_event(event)
                else:
                    face.reset()
                    menu_bar.reset(event)

            if menu_bar.real_menu:
                if not menu_bar.q_out.empty():
                    info = menu_bar.q_out.get()
                    if info['type'] == 'change_level':
                        WIDTH = info['width']
                        HEIGHT = info['height']
                        MINES = info['mines']
                        INITIAL = True

            pygame.display.update()
