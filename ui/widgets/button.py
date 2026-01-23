class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos, self.y_pos = pos  # center position
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        # Initial rects (center-aligned)
        if self.image:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update_rect(self):
        """Call whenever x_pos, y_pos, or text changes"""
        if self.image:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def total_height(self):
        return self.rect.height

    def handle_event(self, event, mouse_pos=None):
        return False

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
        self.update_rect()  # keep rect centered

