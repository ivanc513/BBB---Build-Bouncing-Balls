import pygame
from ui.windows.windows import WINDOWS

def main():
    pygame.init()

    info = pygame.display.Info()
    SCREEN_W, SCREEN_H = info.current_w, info.current_h
    SCREEN = [SCREEN_W, SCREEN_H]

    # Start with the main menu
    state = {
        "window" : "MAIN_MENU",
        "world" : None
    }
    running = True

    while running:
        # Every window has its own loop and must return next widnow
        window_func = WINDOWS[state["window"]]
        result = window_func(SCREEN, state)

        if result["next"] == "QUIT":
            running = False
        else:
            state["window"] = result["next"]
            state["world"] = result.get("world", state["world"])

    pygame.quit()

if __name__ == "__main__":
    main()