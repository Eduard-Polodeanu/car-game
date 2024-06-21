import pygame

from button import Button

pygame.init()

BG_IMG = pygame.image.load("assets/menu-bg.png")
BUTTON_IMG = pygame.image.load("assets/button.png")
BUTTON_IMG2 = pygame.image.load("assets/button2.png")
BUTTON_IMG3 = pygame.image.load("assets/button3.png")

FONT_80 = pygame.font.SysFont("arialblack", 80)
FONT_54 = pygame.font.SysFont("arialblack", 54)
FONT_40 = pygame.font.SysFont("arialblack", 40)
FONT_28 = pygame.font.SysFont("arialblack", 28)
FONT_14 = pygame.font.SysFont("arialblack", 14)

COLOR = "#f1f4c6"
COLOR_HOVER = "#ffffff"

PLAY_BUTTON = Button(BUTTON_IMG, (640, 320), "START", FONT_54, COLOR, COLOR_HOVER)
OPTIONS_BUTTON = Button(BUTTON_IMG, (640, 450), "OPTIONS", FONT_54, COLOR, COLOR_HOVER)
QUIT_BUTTON = Button(BUTTON_IMG, (640, 580), "QUIT", FONT_54, COLOR, COLOR_HOVER)

NEXT_BUTTON = Button(BUTTON_IMG2, (640, 520), "NEXT LEVEL", FONT_40, COLOR, COLOR_HOVER)
QUIT_BUTTON2 = Button(BUTTON_IMG2, (640, 620), "QUIT", FONT_40, COLOR, COLOR_HOVER)
ENGINE_PERK = Button(BUTTON_IMG3, (480, 360), "Engine", FONT_14, COLOR, COLOR_HOVER)
STEERING_PERK = Button(BUTTON_IMG3, (640, 360), "Steering", FONT_14, COLOR, COLOR_HOVER)
SABOTAGE_PERK = Button(BUTTON_IMG3, (800, 360), "Sabotage", FONT_14, COLOR, COLOR_HOVER)


class Menu:
    def __init__(self, window, menu_booleans):
        self.window = window
        self.menu_booleans = menu_booleans


    def main_menu(self):
        while self.menu_booleans["show_menu"]:
            self.window.blit(BG_IMG, (0, 0))

            screen_text = FONT_80.render("MAIN MENU", True, COLOR)
            text_rect = screen_text.get_rect(center=(640, 100))
            self.window.blit(screen_text, text_rect)

            mouse_pos = pygame.mouse.get_pos()
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.change_color_hover(mouse_pos)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.check_for_click(mouse_pos):
                        self.menu_booleans["show_menu"] = False
                    if OPTIONS_BUTTON.check_for_click(mouse_pos):
                        pass
                    if QUIT_BUTTON.check_for_click(mouse_pos):
                        pygame.quit()
                        quit()

            pygame.display.flip()

    def next_level_menu(self, current_level, current_score, perks):
        while self.menu_booleans["show_nextlevel_menu"]:
            self.window.blit(BG_IMG, (0, 0))

            screen_text = FONT_80.render(("Finished level " + str(current_level)), True, COLOR)
            text_rect = screen_text.get_rect(center=(640, 100))
            screen_text2 = FONT_40.render(("Round score: " + str(current_score)), True, COLOR)
            text_rect2 = screen_text2.get_rect(center=(640, 200))
            self.window.blit(screen_text, text_rect)
            self.window.blit(screen_text2, text_rect2)
            
            mouse_pos = pygame.mouse.get_pos()
            for button in [NEXT_BUTTON, QUIT_BUTTON2]:
                button.change_color_hover(mouse_pos)
                button.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ENGINE_PERK.check_for_click(mouse_pos):
                        perks = [1, 0, 0]
                    if STEERING_PERK.check_for_click(mouse_pos):
                        perks = [0, 1, 0]
                    if SABOTAGE_PERK.check_for_click(mouse_pos):
                        perks = [0, 0, 1]
                         
                    if NEXT_BUTTON.check_for_click(mouse_pos):
                        self.menu_booleans["show_nextlevel_menu"] = False
                    if QUIT_BUTTON2.check_for_click(mouse_pos):
                        pygame.quit()
                        quit()

            if self.menu_booleans["is_perk_unlocked"]:
                screen_text3 = FONT_28.render("You can choose a free perk:", True, COLOR)
                text_rect3 = screen_text3.get_rect(center=(640, 300))
                self.window.blit(screen_text3, text_rect3)

                for button in [ENGINE_PERK, STEERING_PERK, SABOTAGE_PERK]:
                    button.change_color_hover(mouse_pos)
                    button.update(self.window)

                if sum(perks) < 1:
                    screen_text4 = FONT_14.render("No perk selected.", True, COLOR)

                if perks == [1, 0, 0]:
                    screen_text4 = FONT_14.render("Engine upgrade selected.", True, COLOR)
                if perks == [0, 1, 0]:
                    screen_text4 = FONT_14.render("Steering upgrade selected.", True, COLOR)
                if perks == [0, 0, 1]:
                    screen_text4 = FONT_14.render("Sabotage enemy selected.", True, COLOR)

                text_rect4 = screen_text4.get_rect(center=(640, 440))
                self.window.blit(screen_text4, text_rect4)

            pygame.display.flip()
        return perks
    
    def end_screen(self, final_score):
        while self.menu_booleans["show_endscreen"]:
            self.window.blit(BG_IMG, (0, 0))

            screen_text = FONT_80.render("CONGRATULATIONS!", True, COLOR)
            text_rect = screen_text.get_rect(center=(640, 100))
            screen_text2 = FONT_54.render("You have completed all levels", True, COLOR)
            text_rect2 = screen_text2.get_rect(center=(640, 300))
            screen_text3 = FONT_54.render(("Final score: " + str(sum(final_score))), True, COLOR)
            text_rect3 = screen_text3.get_rect(center=(640, 400))
            self.window.blit(screen_text, text_rect)
            self.window.blit(screen_text2, text_rect2)
            self.window.blit(screen_text3, text_rect3)

            mouse_pos = pygame.mouse.get_pos()
            QUIT_BUTTON.change_color_hover(mouse_pos)
            QUIT_BUTTON.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if QUIT_BUTTON.check_for_click(mouse_pos):
                        pygame.quit()
                        quit()

            pygame.display.flip()

    def draw_start_prompt(self):
        TEXT = FONT_28.render("Press any key to start", True, COLOR)
        TEXT_RECT = TEXT.get_rect(center=(640, 700))
        self.window.blit(TEXT, TEXT_RECT)