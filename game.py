from os import link
import pygame
import random
import math
import copy
import time
import tkinter as tk
import webbrowser

pygame.font.init()
pygame.mixer.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)

FONT = pygame.font.Font("assets/font.ttf", 70)
FONT_MIN = pygame.font.Font("assets/font.ttf", 30)

def callback(url):
    webbrowser.open_new(url)

def center_pos(rect, height):
    return (300 - ((rect[0] + rect[2])//2), height)

def play_sound(sound, repeat=False):
    pygame.mixer.music.load(f"assets/audios/{sound}.ogg")
    if repeat:
        pygame.mixer.music.play(loops=-1)
    else:
        pygame.mixer.music.play()

def about():
    window = tk.Tk()
    window.geometry("600x600")

    file = open("assets/about.txt", "r")
    text = file.read()

    label = tk.Label(text=text)
    label.pack()
    
    repo = tk.Label(fg="blue", text="Código fonte")
    github = tk.Label(fg="blue", text="GitHub")
    linkedin = tk.Label(fg="blue", text="Linkedin")
    twitter = tk.Label(fg="blue", text="Twitter")

    repo.pack()
    github.pack()
    linkedin.pack()
    twitter.pack()

    repo.bind("<Button-1>", lambda e: callback("https://github.com/MariaEduardaDeAzevedo/jogo-da-velha"))
    github.bind("<Button-1>", lambda e: callback("https://github.com/MariaEduardaDeAzevedo/"))
    twitter.bind("<Button-1>", lambda e: callback("https://twitter.com/ddt_azevedo"))
    linkedin.bind("<Button-1>", lambda e: callback("https://www.linkedin.com/in/mariaeduardadeazevedo/"))

    window.mainloop()
    file.close()


def about_button(window, height, border=0):
    render = FONT.render("SOBRE", True, BLACK)
    font_rect = render.get_rect()
    middle = (font_rect[0] + font_rect[2])//2
    pos = (300-middle-border, height, font_rect[2]+2*border, font_rect[3]+border)
    pygame.draw.rect(window, BLUE, pos)
    window.blit(render, (300-middle, height))

    if pygame.mouse.get_pressed() == (1,0,0):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] in range(pos[0], pos[0]+pos[2]) and mouse_pos[1] in range(pos[1], pos[1]+pos[3]):
            play_sound("open_001")
            about()
            return False

    return True

def start_button(window, text, height, me, ai, nickname, border=0):
    render = FONT.render(text, True, BLACK)
    font_rect = render.get_rect()
    middle = (font_rect[0] + font_rect[2])//2
    pos = (300-middle-border, height, font_rect[2]+2*border, font_rect[3]+border)
    pygame.draw.rect(window, GREEN, pos)
    window.blit(render, (300-middle, height))

    if pygame.mouse.get_pressed() == (1,0,0):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] in range(pos[0], pos[0]+pos[2]) and mouse_pos[1] in range(pos[1], pos[1]+pos[3]):
            play_sound("open_001")
            game(ai, me, nickname)
            return False

    return True
            

def end_window(clock, winner, me, ai, nickname):
    window = pygame.display.set_mode([600,600])
    running = True
    
    if winner == me:
        play_sound("winner")
    elif winner == ai:
        play_sound("looser")
    else:
        play_sound("tie")

    while running:    
        window.fill(BLACK)
        running = start_button(window, "JOGAR NOVAMENTE", 350, me, ai, nickname, border=10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        
        text = "DEU VELHA" if not winner else f"{winner} GANHOU"
        render = FONT.render(text, True, WHITE)
        font_rect = render.get_rect()
        middle = (font_rect[0]+font_rect[2])//2
        pos = (300-middle, 200)
        

        window.blit(render, pos)
        clock.tick(60)    
        pygame.display.flip()


def minimax(board, maximizing, ai, me):
    win = has_winner(board)

    if has_tie(board):
        return 0
    elif win == ai:
        return 1
    elif win == me:
        return -1

    if maximizing:
        best_score = -(math.inf)
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    tab = copy.deepcopy(board)
                    tab[i][j] = ai 
                    score = minimax(tab, False, ai, me)
                    best_score = max((score, best_score))
        return best_score

    else: 
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    tab = copy.deepcopy(board)
                    tab[i][j] = me
                    score = minimax(tab, True, ai, me)
                    best_score = min((score, best_score))
        return best_score


def get_move(board, ai, me):
    best_score = -(math.inf)
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                tab = copy.deepcopy(board)
                tab[i][j] = ai
                score = minimax(tab, False, ai, me)
                if score > best_score:
                    best_score = score
                    best_move = (i,j)
    
    return best_move


def draw_marked(table, spaces, window):
    for i in range(3):
        for j in range(3):
            if table[i][j] == "X":
                draw_X(spaces[(i,j)], window)
            elif table[i][j] == "O":
                draw_circle(spaces[(i,j)], window)

def get_cel(spaces, pos):
    for key in spaces:
        coordinates = spaces[key]
        if pos[0] in range(coordinates[0][0], coordinates[1][0]) and pos[1] in range(coordinates[0][1], coordinates[1][1]):
            return key

def has_winner(table):
    for i in range(3):
        column = list()
        if table[i] == ["X", "X", "X"]:
            return "X"
        elif table[i] == ["O", "O", "O"]:           
            return "O"
        for j in range(3):
            column.append(table[j][i])

        if column == ["X", "X", "X"]:
            return "X"
        elif column == ["O", "O", "O"]:           
            return "O"

    k = 2
    diag_p = list()
    diag_s = list()
    for i in range(3):
        diag_p.append(table[i][i])
        diag_s.append(table[k][i])
        k -= 1

    if diag_p == ["X", "X", "X"]:
        return "X"
    elif diag_p == ["O", "O", "O"]:           
        return "O"
    if diag_s == ["X", "X", "X"]:
        return "X"
    elif diag_s == ["O", "O", "O"]:           
        return "O"

    return False


def has_tie(table):
    
    if has_winner(table):
        return False

    for i in range(3):
        if " " in table[i]:
            return False

    return True

def get_spaces():
    s = dict()

    y = 0
    h = 200
    for i in range(3):
        x = 0
        w = 200
        for j in range(3):
            s[(i,j)] = [(x,y), (w,h)]
            x += 200
            w += 200
        y += 200
        h += 200

    return s

def random_move(table):
    empty = list()

    for i in range(3):
        for j in range(3):
            if table[i][j] == " ":
                empty.append((i,j))
    
    return random.choice(empty)


def draw_grid(window):
    pygame.draw.line(window, WHITE, (0, 200), (600,200), 2)
    pygame.draw.line(window, WHITE, (0, 400), (600,400), 2)
    pygame.draw.line(window, WHITE, (200, 0), (200,600), 2)
    pygame.draw.line(window, WHITE, (400, 0), (400,600), 2)


def draw_X(coord, window):
    pygame.draw.line(window, WHITE, (coord[0][0]+50, coord[0][1]+50), (coord[1][0]-50, coord[1][1]-50), 10)
    pygame.draw.line(window, WHITE, (coord[0][0]+50, coord[0][1]+150), (coord[1][0]-50, coord[1][1]-150), 10)

def draw_circle(coord, window):
    center = (coord[0][0] + 100, coord[0][1] + 100)
    pygame.draw.circle(window, WHITE, center, 50, 10)


def print_table(table):
    print("- - -")
    for i in range(3):
        print(" ".join(table[i]))
    print("- - -")

def game(ai, me, nickname):
    window = pygame.display.set_mode([600,600])
    clock = pygame.time.Clock()

    table = [
        [" "," "," "],
        [" "," "," "],
        [" "," "," "],
    ]

    spaces = get_spaces()

    running = True
    turn = random.choice([me, ai])
    first = True
    closed = False

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                closed = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    closed = True
        
        window.fill(BLACK)
        
        draw_grid(window)

        if pygame.mouse.get_pressed() == (1,0,0):  
            if turn == me:  
                cel = get_cel(spaces, pygame.mouse.get_pos())
                if table[cel[0]][cel[1]] == " ":
                    table[int(cel[0])][int(cel[1])] = me
                    turn = ai
                    first = False
                    play_sound("confirmation_001")

        elif turn == ai:
            cel = random_move(table) if first else get_move(copy.deepcopy(table), ai, me)
            if table[cel[0]][cel[1]] == " ":        
                table[cel[0]][cel[1]] = ai
                turn = me
                first = False
                play_sound("select_001")

        draw_marked(table, spaces, window)
        print_table(table)

        if has_winner(table) != False or has_tie(table):
            running = False

        clock.tick(60)    
        pygame.display.flip()

        if running == False:
            time.sleep(1)

    if not closed:
        winner = ""
        if has_winner(table) == ai:
            winner = "COMPUTER"
        elif has_winner(table) == me:
            winner = nickname

        end_window(clock, winner, me, ai, nickname)