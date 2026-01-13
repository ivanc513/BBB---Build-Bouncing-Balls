import pygame
import sys
from ui.widgets.button import Button
from tests.simulation import simulation_test

def main_menu(screen):
    pygame.display.set_caption("Menu")
    [width, height] = pygame.display.get_window_size()

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = pygame.font.Font("ui/assets/OpenSans.ttf", 150).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(width/2, height/10))

        NEW_BUTTON = Button(image=None, pos=(width/2, 3 * height/10), 
                            text_input="NEW SIMULATION", font = pygame.font.Font("ui/assets/OpenSans.ttf", 75), 
                            base_color="#d7fcd4", hovering_color="White")
        LIBRARY_BUTTON = Button(image=None, pos=(width/2, 4.5 * height/10), 
                            text_input="LIBRARY", font=pygame.font.Font("ui/assets/OpenSans.ttf", 75), 
                            base_color="#d7fcd4", hovering_color="White")
        RECORDINGS_BUTTON = Button(image=None, pos=(width/2, 6 * height/10), 
                            text_input="RECORDINGS", font=pygame.font.Font("ui/assets/OpenSans.ttf", 75), 
                            base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(width/2, 7.5 * height/10), 
                            text_input="QUIT", font=pygame.font.Font("ui/assets/OpenSans.ttf", 75), 
                            base_color="#d7fcd4", hovering_color="White")
                            
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [NEW_BUTTON, LIBRARY_BUTTON, RECORDINGS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NEW_BUTTON.checkForInput(MENU_MOUSE_POS):
                    simulation_test()
                if LIBRARY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("Library not implemented") 
                if RECORDINGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("Recordings not implemented")                
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()