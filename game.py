import pygame
import random
import math
import copy
import time

WHITE = (255,255,255)
BLACK = (0,0,0)

AI = "O"
ME = "X"

def minimax(board, maximizing):
    win = has_winner(board)

    if has_tie(board):
        return 0
    elif win == AI:
        return 1
    elif win == ME:
        return -1

    if maximizing:
        best_score = -(math.inf)
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    tab = copy.deepcopy(board)
                    tab[i][j] = AI 
                    score = minimax(tab, False)
                    best_score = max((score, best_score))
        return best_score

    else: 
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    tab = copy.deepcopy(board)
                    tab[i][j] = ME
                    score = minimax(tab, True)
                    best_score = min((score, best_score))
        return best_score


def get_move(board):
    best_score = -(math.inf)
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                tab = copy.deepcopy(board)
                tab[i][j] = AI
                score = minimax(tab, False)
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

pygame.init()

window = pygame.display.set_mode([600,600])
clock = pygame.time.Clock()

table = [
    [" "," "," "],
    [" "," "," "],
    [" "," "," "],
]

spaces = get_spaces()

running = True
turn = random.choice([ME, AI])
first = True
while running:
       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill(BLACK)
    
    draw_grid(window)

    if pygame.mouse.get_pressed() == (1,0,0):  
        if turn == ME:  
            cel = get_cel(spaces, pygame.mouse.get_pos())
            table[int(cel[0])][int(cel[1])] = ME
            turn = AI
            first = False

    elif turn == AI:
        cel = random_move(table) if first else get_move(copy.deepcopy(table))
        table[cel[0]][cel[1]] = AI
        turn = ME
        first = False

    draw_marked(table, spaces, window)
    print_table(table)

    if has_winner(table) != False or has_tie(table):
        running = False
        print(has_winner(table))

    clock.tick(60)    
    pygame.display.flip()
