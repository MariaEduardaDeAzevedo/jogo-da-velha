from game import start_button
import pygame
import time
from pygame import font
from celare import gitignore

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)


def center_pos(rect, height):
    return (300 - ((rect[0] + rect[2])//2), height)

pygame.init()
pygame.font.init()

FONT = pygame.font.Font("assets/font.ttf", 70)

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
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(nickname) > 2:
                nickname = list(nickname)
                nickname.pop(-2)
                nickname = "".join(nickname)
            elif len(nickname.strip()) <= 10:
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

    start_button(window, "JOGAR", 380, me, ia, nickname.strip(), 10)

    pygame.display.flip()
    clock.tick(60)