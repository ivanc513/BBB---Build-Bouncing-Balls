import pygame
from ui.widgets.button import Button

class Dropdown(Button):
    def __init__(self, pos, width, options, font, base_color, hovering_color, text_input="", on_select=None, spacing=5):
        super().__init__(None, pos, text_input, font, base_color, hovering_color)
        self.width = width
        self.options = options  # list of Buttons or Dropdowns
        self.expanded = False
        self.on_select = on_select
        self.spacing = spacing
        self.layout_options()

    def layout_options(self, top_y=None):
        """Position children relative to left-aligned x_pos"""
        if top_y is None:
            top_y = self.y_pos

        y_offset = self.rect.height + self.spacing

        for option in self.options:
            # LEFT-aligned: x_pos is the left edge
            option.x_pos = self.x_pos
            option.y_pos = top_y + y_offset
            option.update_rect()  # make sure rect matches

            # If child is dropdown, recursively layout
            if isinstance(option, Dropdown):
                option.layout_options(option.y_pos)

            # Increment offset by height
            y_offset += option.total_height() + self.spacing

    def update(self, screen):
        super().update(screen)
        if self.expanded:
            for option in self.options:
                option.update(screen)

    def handle_event(self, event, mouse_pos):
        toggled = False

        # Toggle dropdown on header click
        if event.type == pygame.MOUSEBUTTONDOWN and self.checkForInput(mouse_pos):
            self.expanded = not self.expanded
            toggled = True

        # Pass events to children only if expanded
        if self.expanded:
            for option in self.options:
                if option.handle_event(event, mouse_pos):
                    toggled = True
                # Leaf buttons
                if isinstance(option, Button) and not isinstance(option, Dropdown):
                    if option.checkForInput(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
                        if self.on_select:
                            self.on_select(option.text_input)
                        toggled = True

        self.changeColor(mouse_pos)
        if self.expanded:
            for option in self.options:
                option.changeColor(mouse_pos)

        return toggled

    def total_height(self):
        if not self.expanded:
            return self.rect.height
        height = self.rect.height
        for option in self.options:
            height += option.total_height() + self.spacing
        return height
