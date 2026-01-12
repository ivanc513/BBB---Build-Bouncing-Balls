import pygame
import sys
from ui.widgets.button import Button
from tests.simulation import simulation_test

def main_menu(SCREEN):
    pygame.display.set_caption("Menu")

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = pygame.font.Font("ui/assets/font.ttf", 100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        NEW_BUTTON = Button(image=pygame.image.load("ui/assets/Play Rect.png"), pos=(640, 250), 
                            text_input="NEW SIMULATION", font = pygame.font.Font("ui/assets/font.ttf", 75), 
                            base_color="#d7fcd4", hovering_color="White")
        LIBRARY_BUTTON = Button(image=pygame.image.load("ui/assets/Options Rect.png"), pos=(640, 400), 
                            text_input="LIBRARY", font=pygame.font.Font("ui/assets/font.ttf", 75), 
                            base_color="#d7fcd4", hovering_color="White")
        RECORDINGS_BUTTON = Button(image=pygame.image.load("ui/assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="RECORDINGS", font=pygame.font.Font("ui/assets/font.ttf", 75), 
                            base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("ui/assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=pygame.font.Font("ui/assets/font.ttf", 75), 
                            base_color="#d7fcd4", hovering_color="White")
                            
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [NEW_BUTTON, LIBRARY_BUTTON, RECORDINGS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
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