import pygame
from app.properties import Properties as Props

class Unit(pygame.sprite.Sprite):
    def __init__(self):
        self.movement = None
        self.cost = None
        self.range = None
        self.tile = None
        self.defeats = None
        self.loses_to = None




class Archer(Unit):
    def __init__(self, tile):
        Unit.__init__(self)
        self.movement = 1
        self.cost = 4
        self.range = 2
        self.tile = tile
        self.image = pygame.image.load('images/bow.png')
        self.defeats = [Swordsman, Spearman, Horseman]
        self.loses_to = [Swordsman, Spearman, Horseman]


class Swordsman(Unit):
    def __init__(self, tile):
        Unit.__init__(self)
        self.movement = 1
        self.cost = 3
        self.range = 1
        self.tile = tile
        self.image = pygame.image.load('images/sword.png')
        self.defeats = [Spearman]
        self.loses_to = [Archer, Horseman]


class Spearman(Unit):
    def __init__(self, tile):
        Unit.__init__(self)
        self.movement = 1
        self.cost = 3
        self.range = 1
        self.tile = tile
        self.image = pygame.image.load('images/spear.png')
        self.defeats = [Horseman]
        self.loses_to = [Swordsman, Archer]


class Horseman(Unit):
    def __init__(self, tile):
        Unit.__init__(self)
        self.movement = 2
        self.cost = 3
        self.range = 1
        self.tile = tile
        self.image = pygame.image.load('images/horseman1.png')
        self.defeats = [Swordsman]
        self.loses_to = [Spearman, Archer]







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


        if not self.enabled:
            background_color = Props.grey
        else:
            background_color = self.highlighted_color if self.is_highlighted else self.color
        rect = pygame.draw.rect(surface, background_color, pygame.Rect(self.x, self.y, self.width, self.height), 2)
        self.draw_content(rect, surface)

    def update(self, event):
        self._update_highlight_state(event)
        self._update_click_state(event)

    def _update_click_state(self, event):
        if not self.enabled:
            self.is_clicked = False
            return

        if self._is_mouse_over_button(event) and event.type == pygame.MOUSEBUTTONDOWN:
            self.is_clicked = True
        else:
            self.is_clicked = False

    def _update_highlight_state(self, event):
        if self._is_mouse_over_button(event):
            self.is_highlighted = True
        else:
            self.is_highlighted = False

    def set_visibility(self, visible=True):
        self.visible = visible

    def set_enabled(self, enabled=True):
        self.enabled = enabled

    def _is_mouse_over_button(self, event):
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
    def __init__(self):
        self.unit_in_tile = None


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


class ColoredBoardTile(BoardTile):
    def __init__(self, top_right, top_left, left, bot_left, bot_right, right, tile_color):
        super(ColoredBoardTile, self).__init__()

        self.top_left = top_left
        self.top_right = top_right
        self.right = right
        self.bot_right = bot_right
        self.bot_left = bot_left
        self.left = left
        self.tile_color = tile_color
        self.rect = pygame.Rect(top_left[0], top_left[1], top_right[0] - top_left[0], bot_left[1] - top_left[1])

    def draw(self, background, is_base_tile=False):
        if self.contains(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            currently_highlighted_tile = True
        else:
            currently_highlighted_tile = False
        draw_color = Props.grey if currently_highlighted_tile else self.tile_color
        if is_base_tile(current_tile):
            draw_color = Props.black
        pygame.draw.polygon(background, draw_color, self.get_tile_coordinates(), 0)
        pygame.draw.polygon(background, Props.grey, self.get_tile_coordinates(), 2)

class ImageBoardTile(BoardTile):
    def __init__(self, top_right, top_left, left, bot_left, bot_right, right, image, image_highlighted, base_image):
        super(ImageBoardTile, self).__init__()

        self.top_left = top_left
        self.top_right = top_right
        self.right = right
        self.bot_right = bot_right
        self.bot_left = bot_left
        self.left = left
        self.image = pygame.transform.scale(image, (int(self.right[0]-self.left[0]), int(self.bot_right[1]-self.top_right[1])))
        self.image_highlighted = pygame.transform.scale(image_highlighted, (int(self.right[0]-self.left[0]), int(self.bot_right[1]-self.top_right[1])))
        self.base_image = pygame.transform.scale(base_image, (int(self.right[0]-self.left[0]), int(self.bot_right[1]-self.top_right[1])))

    def draw(self, screen, is_base_tile=False):

        if is_base_tile:
            screen.blit(self.base_image, (int(self.left[0]), int(self.top_left[1])))
        else:
            if self.contains(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                screen.blit(self.image_highlighted, (int(self.left[0]), int(self.top_left[1])))
            else:
                screen.blit(self.image, (int(self.left[0]), int(self.top_left[1])))

            if self.unit_in_tile is not None:
                screen.blit(self.unit_in_tile, (int(self.left[0]), int(self.top_left[1])))


        pygame.draw.polygon(screen, Props.grey, self.get_tile_coordinates(), 2)