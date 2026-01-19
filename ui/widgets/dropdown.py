import pygame
from ui.widgets.button import Button

class Dropdown(Button):
    def __init__(self, pos, width, options, font, base_color, hovering_color, text_input="", on_select=None):
        super().__init__(image=None, pos=pos, text_input=text_input, font=font,
                         base_color=base_color, hovering_color=hovering_color)
        self.width = width
        self.options = options  # list of strings
        self.expanded = False
        self.option_buttons = []
        self.on_select = on_select  # callback function when an option is clicked

        self.create_option_buttons()

    def create_option_buttons(self):
        """Create a Button instance for each option, stacked vertically."""
        self.option_buttons = []
        for i, option in enumerate(self.options):
            btn = Button(
                image=None,
                pos=(self.x_pos, self.y_pos + (i + 1) * (self.rect.height + 5)),
                text_input=option,
                font=self.font,
                base_color=self.base_color,
                hovering_color=self.hovering_color
            )
            self.option_buttons.append(btn)

    def update(self, screen):
        """Draw the dropdown header and, if expanded, all options."""
        super().update(screen)  # Draw the main button
        if self.expanded:
            for btn in self.option_buttons:
                btn.update(screen)

    def handle_event(self, event, mouse_pos):
        """Handle clicks to expand/collapse and select options."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.checkForInput(mouse_pos):
                # Toggle expanded
                self.expanded = not self.expanded
            elif self.expanded:
                for btn in self.option_buttons:
                    if btn.checkForInput(mouse_pos):
                        self.text_input = btn.text_input  # update main button text
                        self.text = self.font.render(self.text_input, True, self.base_color)
                        self.expanded = False
                        if self.on_select:
                            self.on_select(btn.text_input)

        # Update hover colors
        self.changeColor(mouse_pos)
        if self.expanded:
            for btn in self.option_buttons:
                btn.changeColor(mouse_pos)
    
    def total_height(self):
        """Return the height this dropdown occupies (expanded or collapsed)"""
        if self.expanded:
            return self.rect.height + len(self.option_buttons) * (self.rect.height + 5)
        return self.rect.height
