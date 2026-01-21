import pygame
from ui.widgets.button import Button

class CheckBox(Button):
    def __init__(
        self,
        pos,
        size=26,
        label="",
        font=None,
        base_color="#d7fcd4",
        hovering_color="White",
        check_color=(0, 255, 0)
    ):
        self.size = size
        self.checked = False
        self.check_color = check_color

        # Create box surface
        box_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (200, 200, 200), box_surface.get_rect(), 2)

        super().__init__(
            image=box_surface,
            pos=pos,
            text_input=label,
            font=font,
            base_color=base_color,
            hovering_color=hovering_color
        )

        # Offset label to the right of the box
        self.text_rect.midleft = (self.rect.right + 10, self.rect.centery)

    def toggle(self):
        self.checked = not self.checked

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.checkForInput(event.pos):
                self.toggle()

    def update(self, screen):
        # Draw box
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        # Draw checkmark
        if self.checked:
            pygame.draw.line(
                screen, self.check_color,
                self.rect.topleft, self.rect.bottomright, 3
            )
            pygame.draw.line(
                screen, self.check_color,
                self.rect.topright, self.rect.bottomleft, 3
            )

        # Draw label
        screen.blit(self.text, self.text_rect)
