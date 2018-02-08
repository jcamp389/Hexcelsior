import pygame
from app.properties import Properties as Props
from app.sprites import LabelButton
from app.utils import Utils
from app.states import States


class Menu(object):
    def __init__(self, screen, surface, music):
        self.screen = screen
        self.surface = surface
        self.music = music

        intro_screen_background = pygame.image.load('images/Intro_Screen_Background.jpg')
        self.intro_screen_background = pygame.transform.scale(intro_screen_background, (Props.SCREENLENGTH, Props.SCREENHEIGHT))

        self.title = pygame.image.load("images/Hexcelsior.png")

        self.exit_button = LabelButton("EXIT GAME", Props.SCREENLENGTH * .45, Props.SCREENHEIGHT * .3, 80, 40, Props.white)
        self.play_button = LabelButton("PLAY GAME", Props.SCREENLENGTH * .45, Props.SCREENHEIGHT * .2, 80, 40, Props.white)

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.exit_button, self.play_button, self.music.music_button)

    def display_toggle_music(self, surface, screen):
        self.toggle_music_button.draw(surface, screen)

    def refresh(self):
        self.screen.blit(self.intro_screen_background, (0, 0))
        self.screen.blit(self.title, (Props.SCREENLENGTH * .22, Props.SCREENHEIGHT * .05))
        self.exit_button.draw(self.screen)
        self.play_button.draw(self.screen)
        Utils.display_xy(self.screen)
        self.music.music_button.draw(self.screen)

    def process_user_input(self, event):
        state = States.MENU

        self.buttons.update(event)

        if self.exit_button.is_clicked:
            state = States.QUIT
        elif self.play_button.is_clicked:
            state = States.BOARD_GAME
        elif self.music.music_button.is_clicked:
            self.music.toggle_music()

        return state
