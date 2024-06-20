import pygame

from button import Button

pygame.init()

BG_IMG = pygame.image.load("assets/menu-bg.png")
BUTTON_IMG = pygame.image.load("assets/button.png")
BUTTON_IMG2 = pygame.image.load("assets/button2.png")
FONT_100 = pygame.font.SysFont("arialblack", 100)
FONT_60 = pygame.font.SysFont("arialblack", 60)


class Menu:
    def __init__(self, window, menu_booleans):
        self.window = window
        self.menu_booleans = menu_booleans


    def main_menu(self):
        while self.menu_booleans["is_show_menu"]:
            self.window.blit(BG_IMG, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            MENU_TEXT = FONT_100.render("MAIN MENU", True, "#f1f4c6")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(BUTTON_IMG, (640, 320), "START", FONT_60, "#f1f4c6", "white")
            OPTIONS_BUTTON = Button(BUTTON_IMG, (640, 450), "OPTIONS", FONT_60, "#f1f4c6", "white")
            QUIT_BUTTON = Button(BUTTON_IMG, (640, 580), "QUIT", FONT_60, "#f1f4c6", "white")

            self.window.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(mouse_pos)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(mouse_pos):
                        self.menu_booleans["is_show_menu"] = False
                    if OPTIONS_BUTTON.checkForInput(mouse_pos):
                        pass
                    if QUIT_BUTTON.checkForInput(mouse_pos):
                        pygame.quit()
                        quit()

            pygame.display.flip()

    def next_level_menu(self, current_level, current_score):
        while self.menu_booleans["is_show_next_level_menu"]:
            self.window.blit(BG_IMG, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            mesaj = "Finished level " + str(current_level)
            MENU_TEXT = FONT_100.render(mesaj, True, "#f1f4c6")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            mesaj2 = "Score: " + str(current_score)
            MENU_TEXT2 = FONT_60.render(mesaj2, True, "#f1f4c6")
            MENU_RECT2 = MENU_TEXT2.get_rect(center=(640, 300))

            NEXT_BUTTON = Button(BUTTON_IMG2, (640, 420), "NEXT LEVEL", FONT_60, "#f1f4c6", "white")
            SAVE_QUIT_BUTTON = Button(BUTTON_IMG2, (640, 550), "SAVE & QUIT", FONT_60, "#f1f4c6", "white")

            self.window.blit(MENU_TEXT, MENU_RECT)
            self.window.blit(MENU_TEXT2, MENU_RECT2)

            for button in [NEXT_BUTTON, SAVE_QUIT_BUTTON]:
                button.changeColor(mouse_pos)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NEXT_BUTTON.checkForInput(mouse_pos):
                        self.menu_booleans["is_show_next_level_menu"] = False
                    if SAVE_QUIT_BUTTON.checkForInput(mouse_pos):
                        pygame.quit()
                        quit()

            pygame.display.flip()

    def end_screen(self, final_score):
        while self.menu_booleans["is_show_end_screen"]:
            self.window.blit(BG_IMG, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            mesaj = "CONGRATULATIONS!"
            MENU_TEXT = FONT_100.render(mesaj, True, "#f1f4c6")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            mesaj2 = "You have completed all levels"
            MENU_TEXT2 = FONT_60.render(mesaj2, True, "#f1f4c6")
            MENU_RECT2 = MENU_TEXT2.get_rect(center=(640, 300))

            mesaj3 = "Final score: " + str(sum(final_score))
            MENU_TEXT3 = FONT_60.render(mesaj3, True, "#f1f4c6")
            MENU_RECT3 = MENU_TEXT3.get_rect(center=(640, 400))

            QUIT_BUTTON = Button(BUTTON_IMG, (640, 600), "QUIT", FONT_60, "#f1f4c6", "white")

            self.window.blit(MENU_TEXT, MENU_RECT)
            self.window.blit(MENU_TEXT2, MENU_RECT2)
            self.window.blit(MENU_TEXT3, MENU_RECT3)

            for button in [QUIT_BUTTON]:
                button.changeColor(mouse_pos)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if QUIT_BUTTON.checkForInput(mouse_pos):
                        pygame.quit()
                        quit()

            pygame.display.flip()
