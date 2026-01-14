import pygame
from ui.windows.windows import WINDOWS

def main():
    pygame.init()

    info = pygame.display.Info()
    SCREEN_W, SCREEN_H = info.current_w, info.current_h
    SCREEN = [SCREEN_W, SCREEN_H]

    # Start with the main menu
    next_window = "MAIN_MENU"
    running = True

    while running:
        # Every window has its own loop and must return next widnow
        window_func = WINDOWS[next_window]
        next_window = window_func(SCREEN)

        if next_window == "QUIT":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()