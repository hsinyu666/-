import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 10  # 10x10 格子
CELL_SIZE = 40
BOARD_WIDTH = GRID_SIZE * CELL_SIZE
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Find the Aircraft Head")

# 加載背景圖片
background_image = pygame.image.load("background_1.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 顏色定義
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

# 隨機生成飛機
def generate_plane():
    head_x, head_y = random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 3)
    rotation = random.choice([0, 90, 180, 270])
    plane_head = (head_x, head_y)
    plane_body = []
    plane_tail = []

    if rotation == 0:  # 飛機朝上
        plane_body = [(head_x - 1, head_y + 1), (head_x, head_y + 1), (head_x + 1, head_y + 1)]
        plane_tail = [(head_x, head_y + 2)]
    elif rotation == 90:  # 飛機朝右
        plane_body = [(head_x + 1, head_y - 1), (head_x + 1, head_y), (head_x + 1, head_y + 1)]
        plane_tail = [(head_x + 2, head_y)]
    elif rotation == 180:  # 飛機朝下
        plane_body = [(head_x - 1, head_y - 1), (head_x, head_y - 1), (head_x + 1, head_y - 1)]
        plane_tail = [(head_x, head_y - 2)]
    elif rotation == 270:  # 飛機朝左
        plane_body = [(head_x - 1, head_y + 1), (head_x - 1, head_y), (head_x - 1, head_y - 1)]
        plane_tail = [(head_x - 2, head_y)]

    return plane_head, plane_body, plane_tail, rotation

# 繪製棋盤和統計資訊
def draw_board(revealed, planes, steps, remaining_planes):
    # 繪製背景圖片
    window.blit(background_image, (0, 0))

    # 繪製棋盤
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(BOARD_X + x * CELL_SIZE, BOARD_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # 如果這個格子被揭示
            if revealed[y][x]:
                is_plane_part = False
                for plane_head, plane_body, plane_tail, rotation in planes:
                    if (x, y) == plane_head:
                        pygame.draw.rect(window, RED, rect)
                        is_plane_part = True
                    elif (x, y) in plane_body or (x, y) in plane_tail:
                        pygame.draw.rect(window, BLUE, rect)
                        is_plane_part = True
                if not is_plane_part:
                    pygame.draw.rect(window, WHITE, rect)
            else:
                pygame.draw.rect(window, GREY, rect)

            pygame.draw.rect(window, BLACK, rect, 1)

    # 顯示統計資訊
    font = pygame.font.Font(None, 30)
    steps_text = font.render(f"Steps: {steps}", True, BLACK)
    remaining_text = font.render(f"Planes Left: {remaining_planes}", True, BLACK)
    window.blit(steps_text, (10, 10))
    window.blit(remaining_text, (200, 10))

# 顯示 Game Over 畫面
def game_over_screen():
    while True:
        window.fill(WHITE)

        # 顯示 Game Over 信息
        font = pygame.font.Font(None, 60)
        game_over_text = font.render("Game Over", True, BLACK)  # 改為黑色
        window.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))

        # 繪製 Restart 按鈕
        restart_button = pygame.Rect(120, 300, 160, 70)  # 放大按鈕框
        pygame.draw.rect(window, GREEN, restart_button)
        restart_text = font.render("Restart", True, WHITE)
        window.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2, 
                                   restart_button.y + (restart_button.height - restart_text.get_height()) // 2))

        # 繪製 Exit 按鈕
        exit_button = pygame.Rect(320, 300, 160, 70)  # 放大按鈕框
        pygame.draw.rect(window, RED, exit_button)
        exit_text = font.render("Exit", True, WHITE)
        window.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, 
                                exit_button.y + (exit_button.height - exit_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    main()  # 重新開始遊戲
                    return
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


# 主遊戲邏輯
def main():
    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    steps = 0
    planes = [generate_plane(), generate_plane()]
    found_plane_heads = [False, False]
    remaining_planes = len(planes)

    while True:
        window.blit(background_image, (0, 0))  # 繪製背景圖片
        draw_board(revealed, planes, steps, remaining_planes)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                x = (mx - BOARD_X) // CELL_SIZE
                y = (my - BOARD_Y) // CELL_SIZE

                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and not revealed[y][x]:
                    revealed[y][x] = True
                    steps += 1

                for idx, (plane_head, plane_body, plane_tail, rotation) in enumerate(planes):
                    if (x, y) == plane_head and not found_plane_heads[idx]:
                        found_plane_heads[idx] = True
                        remaining_planes -= 1
                        if remaining_planes == 0:
                            game_over_screen()  # 切換到 Game Over 畫面
                            return

        pygame.display.update()

# 啟動遊戲
if __name__ == "__main__":
    main()
