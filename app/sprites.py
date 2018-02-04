import pygame
from app.properties import Properties as Props


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.highlighted_color = Props.red
        self.rect = pygame.Rect(x, y, width, height)

        self.is_highlighted = False
        self.is_clicked = False
        self.visible = True
        self.enabled = True

    def draw(self, surface):
        if self.visible is False:
            return

        background_color = self.highlighted_color if self.is_highlighted else self.color
        rect = pygame.draw.rect(surface, background_color, pygame.Rect(self.x, self.y, self.width, self.height), 2)
        self.draw_content(rect, surface)

    def update(self, event):
        self.update_highlight_state(event)
        self.update_click_state(event)

    def update_click_state(self, event):
        if not self.enabled:
            self.is_clicked = False
            return

        if self.__is_mouse_over_button(event) and event.type == pygame.MOUSEBUTTONDOWN:
            self.is_clicked = True
        else:
            self.is_clicked = False

    def update_highlight_state(self, event):
        if self.__is_mouse_over_button(event):
            self.is_highlighted = True
        else:
            self.is_highlighted = False

    def set_visibility(self, visible=True):
        self.visible = visible

    def set_enabled(self, enabled=True):
        self.enabled = enabled

    def __is_mouse_over_button(self, event):
        if not hasattr(event, "pos"):
            return False

        return self.rect.left < event.pos[0] < self.rect.right and self.rect.top < event.pos[1] < self.rect.bottom


class LabelButton(Button):
    def __init__(self, title, *args, **kwargs):
        super(LabelButton, self).__init__(*args, **kwargs)

        self.title = title

    def draw_content(self, rect, screen):
        font = pygame.font.Font(None, 15, bold=True, italic=False)
        text_color = self.highlighted_color if self.is_highlighted else self.color
        label = font.render(self.title, True, text_color)
        label_pos = label.get_rect()
        label_pos.centerx = rect.centerx
        label_pos.centery = rect.centery
        screen.blit(label, label_pos)


class ImageButton(Button):
    def __init__(self, path,  x, y, width, height, color):
        super(ImageButton, self).__init__( x, y, width, height, color)

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw_content(self, rect, screen):
        screen.blit(self.image, rect.topleft)


class BoardTile(pygame.sprite.Sprite):
    def __init__(self, top_right, top_left, left, bot_left, bot_right, right, tile_color):
        pygame.sprite.Sprite.__init__(self)

        self.top_left = top_left
        self.top_right = top_right
        self.right = right
        self.bot_right = bot_right
        self.bot_left = bot_left
        self.left = left
        self.tile_color = tile_color
        self.rect = pygame.Rect(top_left[0], top_left[1], top_right[0] - top_left[0], bot_left[1] - top_left[1])

    def get_tile_coordinates(self):
        return self.top_left, self.top_right, self.right, self.bot_right, self.bot_left, self.left

    def contains(self, x, y):
        # adapted from http://www.ariel.com.au/a/python-point-int-poly.html
        coordinates = self.get_tile_coordinates()
        n = len(coordinates)
        contains_point = False

        p1x, p1y = coordinates[0]
        for i in range(n + 1):
            p2x, p2y = coordinates[i % n]
            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y-p1y) * (p2x-p1x) / (p2y-p1y) + p1x
                if p1x == p2x or x <= xinters:
                    contains_point = not contains_point
            p1x, p1y = p2x, p2y

        return contains_point

    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.top_left, self.top_right, self.right, self.bot_right, self.bot_left, self.left)
