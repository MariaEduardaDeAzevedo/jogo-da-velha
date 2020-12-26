from game import about_button, start_button, play_sound, center_pos
import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)

pygame.init()
pygame.font.init()
pygame.mixer.init()

FONT = pygame.font.Font("assets/font.ttf", 70)
FONT_MIN = pygame.font.Font("assets/font.ttf", 30)

window = pygame.display.set_mode([600,600])

running = True
clock = pygame.time.Clock()

nickname = " "

me = "X"
ia = "O"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            play_sound("minimize_001")
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(nickname) > 2:
                nickname = list(nickname)
                nickname.pop(-2)
                nickname = "".join(nickname)
                play_sound("error_001")
            elif len(nickname.strip()) <= 10:
                play_sound("bong_001")
                if len(nickname) > 1:
                    nickname = list(nickname)
                    nickname.pop(-1)
                    nickname = "".join(nickname)
                nickname += event.unicode
                nickname += " "
            
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                if me == "X":
                    me = "O"
                    ia = "X"
                else:
                    me = "X"
                    ia = "O"

    window.fill(BLACK)

    title = FONT.render("JOGO DA VELHA", True, WHITE)
    title_pos = center_pos(title.get_rect(), 10)
    window.blit(title, title_pos)

    nickname_label = FONT.render("SEU NOME", True, WHITE)
    nickname_label_pos = center_pos(nickname_label.get_rect(), 100)
    window.blit(nickname_label, nickname_label_pos)

    nickname_render = FONT.render(nickname, True, BLACK)
    nickname_rect = nickname_render.get_rect()
    nickname_pos = center_pos(nickname_rect, 180)
    pygame.draw.rect(window, WHITE, (nickname_pos[0], 180, nickname_rect[2], nickname_rect[3]))
    window.blit(nickname_render, nickname_pos)

    choice_render = FONT.render(f"JOGUE COM {me}", True, WHITE)
    window.blit(choice_render, center_pos(choice_render.get_rect(), 280))

    my_name = FONT_MIN.render(f"DESENVOLVIDO POR MARIA EDUARDA DE AZEVEDO", True, WHITE)
    window.blit(my_name, center_pos(my_name.get_rect(), 560))

    start_button(window, "JOGAR", 380, me, ia, nickname.strip(), 10)
    about_button(window, 450, 10)

    pygame.display.flip()
    clock.tick(60)