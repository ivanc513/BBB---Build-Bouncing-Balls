from ui.widgets.button import Button

import pygame

class SliderButton(Button):
    def __init__(self, image, pos, text_input, font, base_color, hovering_color,
                 min_value, max_value, start_value, width=200):

        super().__init__(image, pos, text_input, font, base_color, hovering_color)

        # Range
        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value

        # Slider visuals
        self.slider_width = width
        self.slider_height = 6
        self.knob_radius = 10
        
        # Drag state
        self.dragging = False

        # Build slider geometry
        self._build_slider()

    # -----------------------------------------------------

    def _build_slider(self):
        """Creates track + knob rects"""
        # slider sits under text
        y_offset = self.rect.height // 2 + 15

        self.track_rect = pygame.Rect(
            self.rect.centerx - self.slider_width // 2,
            self.rect.centery + y_offset,
            self.slider_width,
            self.slider_height
        )

        self._update_knob_from_value()

    # -----------------------------------------------------

    def _update_knob_from_value(self):
        percent = (self.value - self.min_value) / (self.max_value - self.min_value)
        knob_x = self.track_rect.left + percent * self.slider_width

        self.knob_rect = pygame.Rect(0, 0, self.knob_radius*2, self.knob_radius*2)
        self.knob_rect.center = (knob_x, self.track_rect.centery)

    def _update_value_from_mouse(self, mouse_x):
        percent = (mouse_x - self.track_rect.left) / self.slider_width
        percent = max(0, min(1, percent))
        self.value = self.min_value + percent * (self.max_value - self.min_value)
        self._update_knob_from_value()

    # -----------------------------------------------------

    def update(self, screen):
        super().update(screen)

        # draw slider track
        pygame.draw.rect(screen, (120,120,120), self.track_rect)

        # draw knob
        pygame.draw.circle(screen, (220,220,220), self.knob_rect.center, self.knob_radius)

        # draw value text
        value_text = self.font.render(f"{int(self.value)}", True, self.base_color)
        value_rect = value_text.get_rect(midleft=(self.track_rect.right + 10, self.track_rect.centery))
        screen.blit(value_text, value_rect)

    # -----------------------------------------------------

    def handle_event(self, event, mouse_pos=None):
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        # CLICK: start dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(mouse_pos) or self.track_rect.collidepoint(mouse_pos):
                self.dragging = True
                self._update_value_from_mouse(mouse_pos[0])
                return True

        # RELEASE: stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                return True

        # DRAG: update value continuously
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._update_value_from_mouse(mouse_pos[0])
                return True

        return False
    
    def attach_to_right_of(self, parent_rect, padding=15):
        """Position slider to the right of a dropdown option"""
        self.x_pos = parent_rect.right + padding + self.slider_width // 2
        self.y_pos = parent_rect.centery - self.rect.height // 2

        self.update_rect()
        self._build_slider()
        
    def total_height(self):
        gap = 20
        slider_height = self.knob_radius * 2
        padding = 6

        return self.rect.height + gap + slider_height + padding
    
    def _build_slider(self):
        gap = 20  # space between label and slider

        # slider always sits BELOW the label
        track_y = self.rect.bottom + gap

        self.track_rect = pygame.Rect(
            self.rect.centerx - self.slider_width // 2,
            track_y,
            self.slider_width,
            self.slider_height
        )

        self._update_knob_from_value()
        
    def update_rect(self):
        super().update_rect()
        self._build_slider()   # rebuild slider after rect moves