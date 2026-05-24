import pygame
import random
import time

#関数ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
#テトリミノの描画
def draw_tetrimino(tetrimino_position, tetrimino_shape, tetrimino_color):
    for row_index, row in enumerate(tetrimino_shape):
        for col_index, col in enumerate(row):
            if col:
                pygame.draw.rect(screen, tetrimino_color, (tetrimino_position[0] * block_size + col_index * block_size, tetrimino_position[1] * block_size + row_index * block_size, block_size, block_size))


#テトリミノの当たり判定
def check_collision(new_position, tetrimino_shape):
    x_pos, y_pos =new_position[0], new_position[1]
    for row_index, row in enumerate(tetrimino_shape):
        for col_index, col in enumerate(row):
            if col:
                #ボードの外に出たら移動しない
                    if col_index + x_pos < 0 or \
                        col_index + x_pos >= block_x_num or \
                        row_index + y_pos >= block_y_num or \
                        board[row_index + y_pos][col_index + x_pos]:   #boardに0以外が入っている場合
                            return True
    return False

 #盤面の描画
def draw_board():
    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if col == 0:
                pygame.draw.rect(screen, LINE_COLOR, (col_index * block_size, row_index * block_size, block_size, block_size), 1)
            else:
                color = TETRIMINOS[col]["color"]
                pygame.draw.rect(screen, color, (col_index * block_size, row_index * block_size, block_size, block_size))
#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
pygame.init()

#盤面の設定
block_size = 40
block_x_num = 10
block_y_num = 20
board = [[0 for _ in range(block_x_num)] for _ in range(block_y_num)]

#ウィンドウの設定
screen_width = block_size * block_x_num
screen_height = block_size * block_y_num
screen = pygame.display.set_mode((screen_width, screen_height))

#FPSの設定
FPS = 60
clock = pygame.time.Clock()

#色の設定
BG_COLOR = (0, 50, 50)
LINE_COLOR = (30, 30, 30)

#テトリミノの設定
TETRIMINOS = {
    "I": {"shape": [[1, 1, 1, 1]],"color": (0, 255, 255)},
    "L": {"shape": [[0, 0, 1],[1, 1, 1]],"color": (0, 0, 255)},
    "J": {"shape": [[1, 0, 0],[1, 1, 1]],"color": (255, 128, 0)},
    "O": {"shape": [[1, 1],[1, 1]],"color": (255, 255, 0)},
    "S": {"shape": [[0, 1, 1],[1, 1, 0]],"color": (0, 255, 0)},
    "Z": {"shape": [[1, 1, 0],[0, 1, 1]],"color": (255, 0, 0)},
    "T": {"shape": [[0, 1, 0],[1, 1, 1]],"color": (128, 0, 128)}
}

tetrimino_position = [3, 0]
tetrimino_key = random.choice(list(TETRIMINOS.keys()))
tetrimino_shape = TETRIMINOS[tetrimino_key]["shape"]
tetrimino_color = TETRIMINOS[tetrimino_key]["color"]

current_time = 0
pre_time = 0
fall_speed = 0.5

#メインループ=========================================================================================================
run = True
while run:

    #背景の塗りつぶし
    screen.fill(BG_COLOR)

    #盤面の描画
    draw_board()

    #テトリミノの描画
    draw_tetrimino(tetrimino_position, tetrimino_shape, tetrimino_color)

    #イベントの取得
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            dx = 0
            dy = 0

            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_RIGHT:
                dx =1
            if event.key == pygame.K_LEFT:
                dx = -1
            if event.key == pygame.K_DOWN:
                dy = 1
            if event.key == pygame.K_UP:
                while not check_collision((tetrimino_position[0], tetrimino_position[1] + 1), tetrimino_shape):
                    tetrimino_position[1] += 1

            #左回転
            if event.key == pygame.K_a:
                new_shape = [list(row) for row in zip(*tetrimino_shape)][::-1]
                if not check_collision(tetrimino_position, new_shape):
                    tetrimino_shape = new_shape


            #右回転
            if event.key == pygame.K_s:
                new_shape = [list(row) for row in zip(*tetrimino_shape[::-1])]
                if not check_collision(tetrimino_position, new_shape):
                    tetrimino_shape = new_shape

            #テトリミノの位置の更新
            new_position = [tetrimino_position[0] + dx, tetrimino_position[1] + dy]
            if not check_collision(new_position, tetrimino_shape):
                tetrimino_position = new_position

    #自由落下
    current_time = time.time()
    if (current_time - pre_time) > fall_speed:
        pre_time = current_time

        #テトリミノが最下段ではない場合
        if not check_collision((tetrimino_position[0], tetrimino_position[1] + 1), tetrimino_shape):
            tetrimino_position[1] += 1

        #テトリミノが最下段についた場合
        else:
            for row_index, row in enumerate(tetrimino_shape):
                for col_index, col in enumerate(row):
                    if col:
                        board[tetrimino_position[1] + row_index][tetrimino_position[0] + col_index] = tetrimino_key


            #ラインの削除
            new_board = [row for row in board if not all(row)]
            remove_count = block_y_num - len(new_board)
            for _ in range(remove_count):
                new_board.insert(0, [0 for _ in range(block_x_num)])
            board = new_board

            #テトリミノの新規作成
            tetrimino_position = [3, 0]
            tetrimino_key = random.choice(list(TETRIMINOS.keys()))
            tetrimino_shape = TETRIMINOS[tetrimino_key]["shape"]
            tetrimino_color = TETRIMINOS[tetrimino_key]["color"]

            #リトライ　(boardの新規作成)
            if check_collision(tetrimino_position, tetrimino_shape):
                print("Game Over")
                board = [[0 for _ in range(block_x_num)] for _ in range(block_y_num)]

    #更新
    pygame.display.update()
    clock.tick(FPS)

#====================================================================================================================

pygame.quit()