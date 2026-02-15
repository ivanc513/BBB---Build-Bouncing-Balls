import pygame
from ui.widgets.button import Button
from ui.widgets.sliderbutton import SliderButton

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
        if top_y is None:
            top_y = self.y_pos

        y_offset = self.rect.height + self.spacing

        for option in self.options:
            option.x_pos = self.x_pos
            option.y_pos = top_y + y_offset
            option.update_rect()

            # Special horizontal placement for sliders
            if isinstance(option, SliderButton):
                option.attach_to_right_of(option.rect)

            # Recurse dropdowns
            if isinstance(option, Dropdown):
                option.layout_options(option.y_pos)

            # ALWAYS use total_height
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

        if self.expanded:
            for option in self.options:
                option.handle_event(event, mouse_pos)

                # Only fire selection for normal buttons
                if isinstance(option, Button) and not isinstance(option, Dropdown) and not isinstance(option, SliderButton):
                    if option.checkForInput(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
                        if self.on_select:
                            self.on_select(option.text_input)
                        toggled = True

        self.changeColor(mouse_pos)
        if self.expanded:
            for option in self.options:
                option.changeColor(mouse_pos)

        return toggled
    
    def change_text(self, new_text):
        self.font.render(new_text, True, self.base_color)

    def total_height(self):
        if not self.expanded:
            return self.rect.height
        height = self.rect.height
        for option in self.options:
            height += option.total_height() + self.spacing
        return height
