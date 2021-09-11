import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_DOWN, K_UP, K_ESCAPE, K_SPACE
import time
# from random import randint
import random

blue = (111, 247, 54)
box_size = 20
scr_width = 640
scr_height = 480
board_width = 10


S_template = [
    ['.....',
     '.....',
     '..cc.',
     '.cc..',
     '.....'],
    ['.....',
     '..c..',
     '..cc.',
     '...c.',
     '.....'],
    ['.....',
     '.....',
     '..cc.',
     '.cc..',
     '.....'],
    ['.....',
     '..c..',
     '..cc.',
     '...c.',
     '.....']]
Z_template = [
    ['.....',
     '.....',
     '.cc..',
     '..cc.',
     '.....'],
    ['.....',
     '...c.',
     '..cc.',
     '..c..',
     '.....'],
    ['.....',
     '.....',
     '.cc..',
     '..cc.',
     '.....'],
    ['.....',
     '...c.',
     '..cc.',
     '..c..',
     '.....']]
O_template = [
    ['.....',
     '.....',
     '..cc.',
     '..cc.',
     '.....'],
    ['.....',
     '.....',
     '..cc.',
     '..cc.',
     '.....'],
    ['.....',
     '.....',
     '..cc.',
     '..cc.',
     '.....'],
    ['.....',
     '.....',
     '..cc.',
     '..cc.',
     '.....']]
I_template = [
    ['..c..',
     '..c..',
     '..c..',
     '..c..',
     '.....'],
    ['.....',
     '.....',
     'cccc.',
     '.....',
     '.....'],
    ['..c..',
     '..c..',
     '..c..',
     '..c..',
     '.....'],
    ['.....',
     '.....',
     'cccc.',
     '.....',
     '.....']]
J_template = [[
    '.....',
    '.....',
    '...c.',
    '...c.',
    '..cc.'],
    [
    '.....',
    '.....',
    '.....',
    '.c...',
    '.ccc.'],
    [
    '.....',
    '.....',
    '.cc..',
    '.c...',
    '.c...'],
    [
    '.....',
    '.....',
    '.ccc.',
    '...c.',
    '.....']]
L_template = [[
    '.....',
    '.....',
    '.c...',
    '.c...',
    '.cc..'],
    [
    '.....',
    '.....',
    '.....',
    '.ccc.',
    '.c...'],
    [
        '.....',
    '.....',
    '..cc.',
    '...c.',
    '...c.'],
    [
    '.....',
    '.....',
    '.....',
    '...c.',
    '.ccc.']]
T_template = [[
    '.....',
    '.....',
    '.....',
    '..c..',
    '.ccc.'],
    [
    '.....',
    '.....',
    '.c...',
    '.cc..',
    '.c...'],
    [
    '.....',
    '.....',
    '.....',
    '.ccc.',
    '..c..'],
    [
    '.....',
    '.....',
    '...c.',
    '..cc.',
    '...c.']]


def availSh():
    return {
        's': {'temp': S_template, 'fill': (91, 45, 249), 'border': (60, 5, 247)},
        'z': {'temp': Z_template, 'fill': (194, 77, 165), 'border': (194, 37, 155)},
        'o': {'temp': O_template, 'fill': (51, 182, 217), 'border': (42, 132, 156)},
        'i': {'temp': I_template, 'fill': (36, 187, 146), 'border': (28, 138, 108)},
        'j': {'temp': J_template, 'fill': (115, 48, 68), 'border': (89, 37, 52)},
        'l': {'temp': L_template, 'fill': (177, 157, 34), 'border': (128, 113, 23)},
        't': {'temp': T_template, 'fill': (103, 14, 136), 'border': (69, 9, 92)}
    }


def run_tetris_game():
    pygame.init()  # começa o joguito
    screen = pygame.display.set_mode((scr_width, scr_height))  # cria a janela
    pygame.display.set_caption('Meu Tetris')  # Titulo
    game_matrix = create_game_matrix()
    piece = create_piece()
    nxt = create_piece()
    lt = time.time()  # ultima atualização
    score = 0
    hold = None
    color_bg = (50, 50, 50)
    while True:
        screen.fill(color_bg)

        if (time.time() - lt > 0.5):  # A cada 500ms
            piece['row'] += 1
            lt = time.time()

        draw_moving_piece(screen, piece)
        pygame.draw.rect(
            screen,
            blue,
            [100, 50, 10 * 20 + 10, 20 * 20 + 10], 5)

        draw_board(screen, game_matrix)
        x = gameover(game_matrix, screen)
        if x['matrix'] != '':
            game_matrix = x['matrix']
            score = x['score']
        draw_score(screen, score)
        draw_info(screen, nxt, 'next')
        if hold:
            draw_info(screen, hold, 'hold')

        piece, hold = move_piece(game_matrix, piece, nxt, hold)
        if (not isvalidposition(game_matrix, piece, adjR=1)):
            # if (piece['row'] == 19 or game_matrix[piece['row']+1][piece['col']] != '.'):
            game_matrix = update_game_matrix(game_matrix, piece)
            lines_removed = removeCompleteLine(game_matrix)
            score += lines_removed
            piece = nxt
            nxt = create_piece()
        pygame.display.update()

        for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()


def move_piece(game_matrix, piece, nxt, hold):
    for event in pygame.event.get():
        if (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.key == K_LEFT) and isvalidposition(game_matrix, piece, adjC=- 1):
                piece['col'] -= 1
            elif (event.key == K_RIGHT) and isvalidposition(game_matrix, piece, adjC=1):
                piece['col'] += 1
            elif (event.key == K_DOWN) and isvalidposition(game_matrix, piece, adjR=1):
                piece['row'] += 1
            elif (event.key == K_SPACE):
                tmp = {
                    'rot': 0,
                    'row': 0,
                    'col': 2,
                    'shape': piece['shape']
                }
                piece = hold if hold else nxt
                hold = tmp
                del tmp
            elif (event.key == K_UP):
                curr = piece['rot']
                piece['rot'] = (curr + 1) if curr < 3 else (0)
                if not isvalidposition(game_matrix, piece):
                    piece['rot'] = curr
    return piece, hold


def draw_score(screen, score):
    font = pygame.font.Font('freesansbold.ttf', 18)
    scoreSurf = font.render('Score: %s' % score, True, (255, 255, 255))
    screen.blit(scoreSurf, (640 - 150, 20))


def draw_info(screen, piece, tipo):
    name, y = ('Next', 50) if tipo == 'next' else ('On hold', 80)
    font = pygame.font.Font('freesansbold.ttf', 18)
    drawSurf = font.render(f'{name}:', True, (255, 255, 255))
    draw_mini(piece, screen, tipo)

    screen.blit(drawSurf, (490, y))


def isvalidposition(game_matrix, piece, adjC=0, adjR=0):
    piece_matrix = availSh()[piece['shape']]['temp'][piece['rot']]
    for r in range(5):
        for c in range(5):
            if piece_matrix[r][c] == '.':
                continue
            if not isOnBoard(piece['row'] + r + adjR, piece['col'] + c + adjC):
                return False
            if game_matrix[piece['row'] + r + adjR][piece['col'] + c + adjC] != '.':
                return False
    return True

    # if not(col >= 0 and col < 10 and row < 20):
    #     return False
    # if game_matrix[row][col] != '.':
    #     return False
    # return True


def isOnBoard(row, column):
    return column >= 0 and column < 10 and row < 20


def gameover(game_matrix, screen):
    retorno = {}
    retorno['matrix'] = ''
    retorno['score'] = ''

    for c in range(10):
        if (game_matrix[1][c] == 'c'):
            gameOverFont = pygame.font.Font('freesansbold.ttf', 72)
            gameOverSurf = gameOverFont.render('Game Over', True, (0, 255, 0))
            gameOverRect = gameOverSurf.get_rect()
            gameOverRect.midtop = (320, 10)
            screen.blit(gameOverSurf, gameOverRect)
            pygame.display.flip()
            retorno['matrix'] = create_game_matrix()
            retorno['score'] = 0
            time.sleep(5)
            return retorno
    return retorno


def removeCompleteLine(game_matrix):
    lines_removed = 0
    for row in range(20):
        if "." not in game_matrix[row][:10]:
            for rowToMove in range(row, 0, -1):
                for col in range(10):
                    game_matrix[rowToMove][col] = game_matrix[rowToMove - 1][col]
            for x in range(10):
                game_matrix[0][x] = '.'
            lines_removed += 1
    return lines_removed


def create_piece():
    return {
        'rot': 0,
        'row': 0,
        'col': 2,
        'shape': random.choice(list(availSh().keys()))
    }


def draw_board(screen, matrix):
    gmc = 10
    gmr = 20
    for r in range(gmr):
        for c in range(gmc):
            if (matrix[r][c] != '.'):
                draw_single_piece(screen, r, c, (200, 200, 200), (220, 220, 220))
            # gameover(matrix, screen)


def draw_moving_piece(screen, piece):
    p = availSh()[piece['shape']]
    shToDraw = p['temp'][piece['rot']]
    for r in range(5):
        for c in range(5):
            if shToDraw[r][c] != '.':
                draw_single_piece(
                    screen, piece['row'] + r, piece['col'] + c, p['fill'], p['border'])


def update_game_matrix(matrix, piece):
    p = availSh()[piece['shape']]['temp'][0]
    for r in range(5):
        for c in range(5):
            if p[r][c] != '.':
                matrix[piece['row'] + r][piece['col'] + c] = 'c'
    return matrix


def draw_single_piece(screen, mcr, mcc, color, scolor):
    origx = 100 + 5 + (mcc * 20 + 1)
    origy = 50 + 5 + (mcr * 20 + 1)
    pygame.draw.rect(screen, scolor, [origx, origy, 20, 20])
    pygame.draw.rect(screen, color, [origx, origy, 18, 18])


def draw_mini(piece, screen, tipo='next'):
    y = 20 if tipo == 'next' else 75
    p = availSh()[piece['shape']]
    shToDraw = p['temp'][piece['rot']]
    for r in range(5):
        for c in range(5):
            if shToDraw[r][c] != '.':
                pygame.draw.rect(screen, p['border'], [560 + (c * 10), y + (r * 10), 10, 10])
                pygame.draw.rect(screen, p['fill'], [560 + (c * 10), y + (r * 10), 8, 8])


def create_game_matrix(cols=10, rows=20):
    return [['.' for c in range(cols)] for r in range(rows)]


if __name__ == '__main__':
    run_tetris_game()
