import pygame
from app.properties import Properties as Props
from app.menu import Menu
from app.game import Game
from app.music import Music
from app.states import States


class Main(object):
    def __init__(self):
        self.current_phase = "PLANNING PHASE"
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(Props.size)
        self.surface = pygame.Surface(self.screen.get_size())
        pygame.display.set_caption("HEXCELSIOR")

        # Our menu and game screens
        self.music = Music()
        States.MENU = Menu(self.screen, self.surface, self.music)
        self.game = Game(self.screen, self.surface, self.music)

    def process_user_input(self, state):
        for event in pygame.event.get():
            if event.type == self.music.song_end:
                print("song has ended")
                self.music.play_next_song()
            if event.type == pygame.QUIT:
                state = States.QUIT
            if state == States.MENU:
                state = States.MENU.process_user_input(event)
            elif state == States.BOARD_GAME:
                state = self.game.process_user_input(event)

        return state

    def refresh(self, state):
        if state == States.MENU:
            States.MENU.refresh()
        elif state == States.BOARD_GAME:
            self.game.refresh()

    def run(self):
        self.music.play_first_song()
        state = States.MENU
        while state != States.QUIT:
            state = self.process_user_input(state)
            self.refresh(state)
            pygame.display.flip()


if __name__ == '__main__':
    Main().run()