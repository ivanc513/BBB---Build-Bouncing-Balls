import pygame
from tests.simulation import simulation_test
from ui.windows.main_menu import main_menu

pygame.init()

info = pygame.display.Info()
SCREEN_W = info.current_w
SCREEN_H = info.current_h

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.RESIZABLE)


main_menu(screen)