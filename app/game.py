from app.properties import Properties as Props
from app.sprites import ImageBoardTile, LabelButton, ImageButton
from app.states import States
import random
import pygame
import threading
from app.utils import Utils


class Player(object):
    def __init__(self, name, number, color, base_tile):
        self.name = name
        self.number = number
        self.color = color
        self.base_tile = base_tile
        self.cost = 4
        self.units = []


class Game(object):
    def __init__(self, screen, surface, music):
        self.music = music
        self.screen = screen
        self.surface = surface
        self.board = None
        self.board_offset = (25, 25)

        self.back_button = LabelButton("Home Screen", Props.SCREENLENGTH * 0, Props.SCREENHEIGHT * 0, 80, 40, Props.white)

        self.background = pygame.image.load('images/old_paper.png')
        self.background = pygame.transform.scale(self.background, (Props.SCREENLENGTH, Props.SCREENHEIGHT))
        self.PHASE_PLANNING = 1
        self.PHASE_ACTION = 2
        self.current_phase = self.PHASE_PLANNING

        self.BOARDHEIGHT = Props.SCREENHEIGHT * .8
        self.BOARDLENGTH = Props.SCREENLENGTH * .8
        self.ready_button = LabelButton("READY", Props.SCREENLENGTH * .6, Props.SCREENHEIGHT * 0, 100, 40, Props.white)

        unit_scale_factor = int((self.BOARDHEIGHT/10) * .8)
        self.bow = ImageButton('images/bow.png', 830, 115, unit_scale_factor, unit_scale_factor, Props.black)
        self.sword = ImageButton('images/sword.png',870, 115, unit_scale_factor, unit_scale_factor, Props.black)
        self.spear = ImageButton('images/spear.png', 910, 115, unit_scale_factor, unit_scale_factor, Props.black)
        self.horseman = ImageButton('images/horseman1.png', 950, 115, unit_scale_factor, unit_scale_factor, Props.black)

        self.changephase(should_change_phase=False)
        self.board = self.board_initializer()

        self.turn_number = 1

        # we are manually going to create players for now
        player_1 = Player(name="Joel", number=1, color=Props.grey, base_tile=self.board[4][5])
        player_2 = Player(name="John", number=2, color=Props.green, base_tile=self.board[15][2])
        player_3 = Player(name="Michael", number=3, color=Props.red, base_tile=self.board[15][7])
        self.players = [player_1, player_2, player_3]

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.music.music_button, self.back_button, self.ready_button,
                         self.bow, self.sword, self.spear, self.horseman)

    def is_base_tile(self, tile):
        for player in self.players:
            if player.base_tile == tile:
                return True

        return False

    def board_initializer(self):
        count_per_column = 10
        count_per_row = count_per_column * 2
        dimensions = self.BOARDHEIGHT / count_per_column
        board_matrix = []
        for i in range(0, count_per_row):
            board_matrix.append([])
            for j in range(0, count_per_column):
                is_row_even = i % 2 == 0
                x = j * (dimensions * 1.5)
                if not is_row_even:
                    x += (dimensions * .75)
                y = i * (dimensions * .425)
                y += dimensions/2
                # Account for the board not starting in the exact top-left corner of the screen.
                x += self.board_offset[0]
                y += self.board_offset[1]
                image, image_highlighted = self.random_tile_image()
                h = ImageBoardTile((x + (dimensions * .75), y + (dimensions * .075)),
                    (x + (dimensions * .25), y + (dimensions * .075)),
                    (x, y + (dimensions * .5)),
                    (x + (dimensions * .25), y + (dimensions * .925)),
                    (x + (dimensions * .75), y + (dimensions * .925)),
                    (x + dimensions, y + (dimensions * .5)), image, image_highlighted)
                board_matrix[i].append(h)
        return board_matrix

    def random_tile_color(self):
        possible_tiles = [Props.red, Props.white, Props.green, Props.brown, Props.yellow]
        index = random.randint(0, len(possible_tiles) - 1)
        return possible_tiles[index]

    def random_tile_image(self):
        desert = pygame.image.load('images/desert_tile.png')
        desert_highlighted = pygame.image.load('images/desert_tile_highlighted.png')
        forest = pygame.image.load('images/forest_tile.png')
        forest_highlighted = pygame.image.load('images/forest_tile_highlighted.png')
        grass = pygame.image.load('images/grass_tile.png')
        grass_highlighted = pygame.image.load('images/grass_tile_highlighted.png')
        mountain = pygame.image.load('images/mountain_tile.png')
        mountain_highlighted = pygame.image.load('images/mountain_tile_highlighted.png')
        possible_tiles = [(desert, desert_highlighted),
                          (forest, forest_highlighted),
                          (grass, grass_highlighted),
                          (mountain, mountain_highlighted)]
        index = random.randint(0, len(possible_tiles) - 1)
        return possible_tiles[index]

    def refresh(self):
        self.screen.blit(self.background, (0, 0))
        self.ready_button.draw(self.screen)
        self.back_button.draw(self.screen)
        self.bow.draw(self.screen)
        self.sword.draw(self.screen)
        self.spear.draw(self.screen)
        self.horseman.draw(self.screen)
        self.board_game()
        self.display_phase()
        self.display_turn_number()
        Utils.display_xy(self.screen)
        self.music.music_button.draw(self.screen)

        if self.current_phase == self.PHASE_PLANNING:
            self.ready_button.set_visibility(visible=True)
            self.ready_button.set_enabled(enabled=True)
        else:
            self.ready_button.set_visibility(visible=False)
            self.ready_button.set_enabled(enabled=False)


    def display_phase(self):
        font = pygame.font.Font(None, 20, bold=True, italic=False)
        phase_title = "PLANNING PHASE" if self.current_phase == self.PHASE_PLANNING else "ACTION PHASE"
        phase_label = font.render(phase_title, True, Props.red)
        phase_labelpos = phase_label.get_rect()
        phase_rect = pygame.Rect(Props.SCREENLENGTH * .35, Props.SCREENHEIGHT * .01, 80, 15)
        phase_labelpos.centerx = phase_rect.centerx
        phase_labelpos.centery = phase_rect.centery
        self.screen.blit(phase_label, (phase_labelpos.centerx - 35, phase_labelpos.centery - 5))

    def display_turn_number(self):
        font = pygame.font.Font(None, 20, bold=True, italic=False)
        turn_text = "TURN " + str(self.turn_number)
        turn_label = font.render(turn_text, True, Props.black)
        turn_labelpos = turn_label.get_rect()
        turn_rect = pygame.Rect(Props.SCREENLENGTH * .35, Props.SCREENHEIGHT * .01, 80, 15)
        turn_labelpos.centerx = turn_rect.centerx
        turn_labelpos.centery = turn_rect.centery
        self.screen.blit(turn_label, (turn_labelpos.centerx - 135, turn_labelpos.centery - 5))

    def changephase(self, should_change_phase=True):
        self.timer = threading.Timer(5.0, self.changephase)
        self.timer.daemon = True
        self.timer.start()
        if should_change_phase == False:
            return
        if self.current_phase == self.PHASE_PLANNING:
            self.current_phase = self.PHASE_ACTION
        else:
            self.current_phase = self.PHASE_PLANNING
            self.turn_number += 1

    def board_game(self):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[0])):
                current_tile = self.board[i][j]
                current_tile.draw(self.background, is_base_tile=self.is_base_tile(current_tile))

    def process_user_input(self, event):
        state = States.BOARD_GAME

        self.buttons.update(event)

        if self.music.music_button.is_clicked:
            self.music.toggle_music()
        elif self.ready_button.is_clicked:
            self.timer.cancel()
            self.changephase()
        elif self.back_button.is_clicked:
            state = States.MENU

        return state
