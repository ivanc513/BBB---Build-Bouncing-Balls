import pygame
from widgets.ui.button import Button

class HighlightButton(Button):
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, highlight_color=(200, 200, 255)):
        super().__init__(image, pos, text_input, font, base_color, hovering_color)
        self.highlight_color = highlight_color
        self.selected = False  # highlight state

    def changeColor(self, position):
        """Highlight text on hover or if selected."""
        if self.selected:
            color = self.highlight_color
        elif self.rect.collidepoint(position):
            color = self.hovering_color
        else:
            color = self.base_color

        self.text = self.font.render(self.text_input, True, color)
        self.update_rect()