import pygame
import random
import math
import time

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
COLORS = [RED, BLUE, GREEN, YELLOW]
ANGLE_STEP = 10  # Шаг поворота пушки
MAX_ANGLE = 75 # Максимальный угол поворота пушки
MIN_ANGLE = -75 #Минимальный угол поворота пушки

# Создаем окно игры
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Shooter Game")
clock = pygame.time.Clock()

# Класс для больших шариков
class BigBall:
    def __init__(self):
        self.radius = 25
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.color = random.choice(COLORS)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        # Отскок от границ
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.vx *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def collides(self, x, y, radius):
        distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return distance < self.radius + radius


# Класс для маленьких шариков (снарядов)
class SmallBall:
    def __init__(self, x, y, angle, speed=10):
        self.radius = 10
        self.x = x
        self.y = y
        self.vx = speed * math.cos(math.radians(angle))
        self.vy = speed * math.sin(math.radians(angle))
        self.color = WHITE

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


# Пушка
cannon_x = 10
cannon_y = HEIGHT // 2
cannon_width = 20
cannon_height = 80
cannon_angle = 0
small_balls = []
big_balls = []
score = 0
start_time = time.time()
MAX_BIG_BALLS = 5

def draw_cannon():
    original_cannon = pygame.Surface((cannon_width, cannon_height), pygame.SRCALPHA)
    original_cannon.fill(WHITE)
    rotated_cannon = pygame.transform.rotozoom(original_cannon, cannon_angle, 1) # масштабируем на 1, чтобы сохранить размер
    rect = rotated_cannon.get_rect(center=(cannon_x + cannon_width // 2, cannon_y))
    screen.blit(rotated_cannon, rect)

def game_loop():
    global cannon_angle, small_balls, big_balls, score, start_time, ANGLE_STEP

    running = True
    while len(big_balls) < MAX_BIG_BALLS:
        big_balls.append(BigBall())
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cannon_angle = min(cannon_angle + ANGLE_STEP, MAX_ANGLE)
                if event.key == pygame.K_DOWN:
                    cannon_angle = max(cannon_angle - ANGLE_STEP, MIN_ANGLE)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Вычисляем координаты узкого конца пушки с учетом поворота
                cannon_center_x = cannon_x + cannon_width // 2
                cannon_center_y = cannon_y
                small_ball_x = cannon_center_x + (cannon_height // 2) * math.sin(math.radians(cannon_angle))
                small_ball_y = cannon_center_y - (cannon_height // 2) * math.cos(math.radians(cannon_angle))
                small_balls.append(SmallBall(small_ball_x, small_ball_y, cannon_angle))


        # Обновление позиций
        for ball in big_balls:
            ball.update()
        for ball in small_balls:
            ball.update()

        # Проверка столкновений
        for i in range(len(small_balls) - 1, -1, -1):
            for j in range(len(big_balls) - 1, -1, -1):
                if big_balls[j].collides(small_balls[i].x, small_balls[i].y, small_balls[i].radius):
                    score += 1
                    big_balls.pop(j)
                    small_balls.pop(i)
                    while len(big_balls) < MAX_BIG_BALLS:
                        big_balls.append(BigBall())
                    break

        # Отрисовка
        screen.fill(BLACK)
        for ball in big_balls:
            ball.draw()
        for ball in small_balls:
            ball.draw()
        draw_cannon()
        draw_text(f"Счет: {score}", 700, 50)

        # Проверка времени
        if time.time() - start_time > 60:
            running = False

        pygame.display.flip()
    return score


def draw_text(text, x, y, color=WHITE, size=36):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def main():
    score = game_loop()
    draw_text(f"Игра окончена! Ваш счет: {score}", WIDTH // 2, HEIGHT // 2, WHITE, 48)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()

if __name__ == "__main__":
    main()