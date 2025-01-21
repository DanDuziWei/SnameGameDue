import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
GAME_SPEED = 15

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪食蛇')
clock = pygame.time.Clock()

# 在颜色定义部分添加新的颜色
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.type = self.random_type()
        self.color = self.get_color()
        self.randomize_position()

    def random_type(self):
        # 随机选择食物类型
        return random.choice(['normal', 'speed', 'slow', 'double', 'shorter'])

    def get_color(self):
        # 根据类型返回对应颜色
        colors = {
            'normal': RED,
            'speed': BLUE,
            'slow': YELLOW,
            'double': PURPLE,
            'shorter': GREEN
        }
        return colors[self.type]

    def randomize_position(self):
        while True:
            new_pos = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
                      random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE)
            # 确保食物不会出现在蛇身上
            if 'snake' in globals() and hasattr(snake, 'positions'):
                if new_pos not in snake.positions:
                    self.position = new_pos
                    break
            else:
                self.position = new_pos
                break

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

class Snake:
    def __init__(self, start_pos, color, player_num=1):
        self.length = 1
        self.positions = [start_pos]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = color
        self.score = 0
        self.speed = GAME_SPEED
        self.effect_timer = 0
        self.player_num = player_num

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.speed = GAME_SPEED  # 添加这行
        self.effect_timer = 0    # 添加这行
        self.color = GREEN       # 添加这行

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, 
                           (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

    def update(self):
        # 更新效果计时器
        if self.effect_timer > 0:
            self.effect_timer -= 1
            if self.effect_timer == 0:
                self.speed = GAME_SPEED
                self.color = GREEN

        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x*BLOCK_SIZE)) % WINDOW_WIDTH, 
               (cur[1] + (y*BLOCK_SIZE)) % WINDOW_HEIGHT)
        if new in self.positions[3:]:
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

def main():
    # 创建两条蛇，分别在不同位置出生
    snake1 = Snake((WINDOW_WIDTH//4, WINDOW_HEIGHT//2), GREEN, 1)
    snake2 = Snake((WINDOW_WIDTH*3//4, WINDOW_HEIGHT//2), BLUE, 2)
    food = Food()
    
    def randomize_food():
        while True:
            new_pos = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
                      random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE)
            if new_pos not in snake1.positions and new_pos not in snake2.positions:
                food.position = new_pos
                food.type = food.random_type()
                food.color = food.get_color()
                break

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 玩家1的控制（方向键）
                if event.key == pygame.K_UP and snake1.direction != DOWN:
                    snake1.direction = UP
                elif event.key == pygame.K_DOWN and snake1.direction != UP:
                    snake1.direction = DOWN
                elif event.key == pygame.K_LEFT and snake1.direction != RIGHT:
                    snake1.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake1.direction != LEFT:
                    snake1.direction = RIGHT
                # 玩家2的控制（WASD）
                elif event.key == pygame.K_w and snake2.direction != DOWN:
                    snake2.direction = UP
                elif event.key == pygame.K_s and snake2.direction != UP:
                    snake2.direction = DOWN
                elif event.key == pygame.K_a and snake2.direction != RIGHT:
                    snake2.direction = LEFT
                elif event.key == pygame.K_d and snake2.direction != LEFT:
                    snake2.direction = RIGHT

        # 更新两条蛇的位置
        if not snake1.update() or not snake2.update():
            snake1.reset()
            snake2.reset()
            food.randomize_position()

        # 检查蛇是否相撞
        if snake1.get_head_position() in snake2.positions or \
           snake2.get_head_position() in snake1.positions:
            snake1.reset()
            snake2.reset()
            food.randomize_position()

        # 处理食物效果
        for snake in [snake1, snake2]:
            if snake.get_head_position() == food.position:
                if food.type == 'normal':
                    snake.length += 1
                    snake.score += 1
                elif food.type == 'speed':
                    snake.speed = min(25, snake.speed + 5)
                    snake.score += 2
                    snake.effect_timer = 50
                elif food.type == 'slow':
                    snake.speed = max(5, snake.speed - 5)
                    snake.score += 2
                    snake.effect_timer = 50
                elif food.type == 'double':
                    snake.length += 2
                    snake.score += 3
                    snake.effect_timer = 30
                elif food.type == 'shorter':
                    if snake.length > 1:
                        snake.length -= 1
                    snake.score += 5
                    snake.effect_timer = 30
                
                randomize_food()

        screen.fill(BLACK)
        snake1.draw(screen)
        snake2.draw(screen)
        food.draw(screen)
        
        # 显示两个玩家的分数
        font = pygame.font.Font(None, 36)
        score1_text = font.render(f'玩家1得分: {snake1.score}', True, GREEN)
        score2_text = font.render(f'玩家2得分: {snake2.score}', True, BLUE)
        screen.blit(score1_text, (10, 10))
        screen.blit(score2_text, (10, 50))

        pygame.display.update()
        clock.tick(max(snake1.speed, snake2.speed))

# 定义方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

if __name__ == '__main__':
    main()