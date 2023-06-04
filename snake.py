import pygame
import time, random
from pygame.math import Vector2

pygame.init()
cell_size = 40
cell_number = 20
COLOUR = (0, 102, 0)
WHITE = (255,255,255)
GREEN = (51, 204, 51)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
running = True
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

game_font = pygame.font.Font(None,25)
screen = pygame.display.set_mode((cell_size * cell_number + 1, cell_size * cell_number + 1))
pygame.display.set_caption("Snake Hunt")

class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.position.x * cell_size), int(self.position.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, RED, fruit_rect)
        pygame.draw.rect(screen, (128, 0, 0), fruit_rect, 2)
        
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        self.bodies = [Vector2(10,6), Vector2(10,7), Vector2(10,8)]
        self.direction = Vector2(0,0)
        self.new_block = False

    def draw_snake(self):
        for body in self.bodies:
            x_pos = int(body.x * cell_size)
            y_pos = int(body.y * cell_size)
            body_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, GREEN, body_rect)
            pygame.draw.rect(screen, COLOUR, body_rect, 2)

    def move(self):
        if self.new_block == True:
            bodies_copy = self.bodies[:]
            bodies_copy.insert(0,bodies_copy[0] + self.direction)
            self.bodies = bodies_copy[:]
            self.new_block = False
        else:
            bodies_copy = self.bodies[:-1]
            bodies_copy.insert(0,bodies_copy[0] + self.direction)
            self.bodies = bodies_copy[:]

    def breed(self):
        self.new_block = True

    def reset(self):
        self.bodies = [Vector2(10,6), Vector2(10,7), Vector2(10,8)]
        self.direction = Vector2(0,0)

class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move()
        self.collison()
        self.illegal()
    def draw_things(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.score()

    def collison(self):
        if self.fruit.position == self.snake.bodies[0]:
            self.fruit.randomize()
            self.snake.breed()
        
        for body in self.snake.bodies[1:]:
            if body == self.fruit.position:
                self.fruit.randomize()

    def illegal(self):
        if not 0 <= self.snake.bodies[0].x < cell_number or not 0 <= self.snake.bodies[0].y < cell_number :
            self.game_over()

        for body in self.snake.bodies[1:]:
            if body == self.snake.bodies[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        self.direction = Vector2(0,0)

    def score(self):
        score_text = str(len(self.snake.bodies) - 3)
        score_surface = game_font.render(score_text, True, (255,255,255))
        score_x = int(cell_number * cell_size - 60)
        score_y = int(cell_number * cell_size - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect )

main = MAIN()

while running:
    clock.tick(60)
    screen.fill(BLACK)
    main.draw_things()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SCREEN_UPDATE:
            main.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main.snake.direction != Vector2(0,1):
                main.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and main.snake.direction != Vector2(0,-1):
                main.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT and main.snake.direction != Vector2(1,0):
                main.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT and main.snake.direction != Vector2(-1,0):
                main.snake.direction = Vector2(1,0)

    pygame.display.flip()

pygame.quit()