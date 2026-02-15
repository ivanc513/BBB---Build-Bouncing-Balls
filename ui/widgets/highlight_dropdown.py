import pygame
from ui.widgets.dropdown import Dropdown
from ui.widgets.sliderbutton import SliderButton

class HighlightDropdown(Dropdown):
    def __init__(self, pos, width, options, font, base_color, hovering_color, 
                 highlight_color=(200,200,255), text_input="", on_select=None, spacing=5):
        super().__init__(pos, width, options, font, base_color, hovering_color, text_input, on_select, spacing)
        self.highlight_color = highlight_color
        self.selected = False  # header highlight state

    def handle_event(self, event, mouse_pos):
        toggled = False

        # Toggle header
        if event.type == pygame.MOUSEBUTTONDOWN and self.checkForInput(mouse_pos):
            self.expanded = not self.expanded
            self.selected = self.expanded
            toggled = True

        # IMPORTANT: always forward events to children
        if self.expanded:
            for option in self.options:
                option.handle_event(event, mouse_pos)

                # only treat plain buttons as selectable items
                if (event.type == pygame.MOUSEBUTTONDOWN and
                    hasattr(option, "checkForInput") and
                    not isinstance(option, Dropdown) and
                    not isinstance(option, SliderButton) and
                    option.checkForInput(mouse_pos)):

                    if self.on_select:
                        self.on_select(option.text_input)
                    toggled = True

        self.changeColor(mouse_pos)

        if self.expanded:
            for option in self.options:
                if hasattr(option, "changeColor"):
                    option.changeColor(mouse_pos)

        return toggled

    def changeColor(self, mouse_pos):
        """Change text color based on header state."""
        if self.selected:
            self.current_color = self.highlight_color
        elif self.checkForInput(mouse_pos):
            self.current_color = self.hovering_color
        else:
            self.current_color = self.base_color

    def update(self, screen):
        """Draw header text in current_color, draw children if expanded."""
        text_surf = self.font.render(self.text_input, True, self.current_color)
        screen.blit(text_surf, self.rect)

        if self.expanded:
            for option in self.options:
                option.update(screen)