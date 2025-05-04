import pygame
import sys
import random
from enum import Enum
from collections import namedtuple
import numpy as np

# --- Constants ---
BLOCK_SIZE = 20
SPEED = 20  

WHITE = (255, 255, 255)
RED   = (200,   0,   0)
BLUE1 = (  0,   0, 255)
BLUE2 = (  0, 100, 255)
BLACK = (  0,   0,   0)

# --- Helper types ---
class Direction(Enum):
    RIGHT = 1
    LEFT  = 2
    UP    = 3
    DOWN  = 4

Point = namedtuple('Point', 'x, y')

# --- Game class ---
class SnakeGameAI:
    def __init__(self, w=640, h=480):
        pygame.init()
        self.font = pygame.font.SysFont('arial', 25)
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # start in the center, using integer division
        self.direction = Direction.RIGHT
        self.head = Point(self.w // 2, self.h // 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)
        ]
        self.score = 0
        self.frame_iteration = 0
        self._place_food()

    def _place_food(self):
        # safer than recursion if board is crowded
        while True:
            x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            food = Point(x, y)
            if food not in self.snake:
                self.food = food
                break

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hit walls
        if pt.x < 0 or pt.x > self.w - BLOCK_SIZE or pt.y < 0 or pt.y > self.h - BLOCK_SIZE:
            return True
        # hit itself
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        # draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        # draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        # draw score
        text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, (0, 0))
        pygame.display.flip()

    def _move(self, action):
        # action is [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]            # no change
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = clock_wise[(idx + 1) % 4]  # turn right
        else:  # [0,0,1]
            new_dir = clock_wise[(idx - 1) % 4]  # turn left

        self.direction = new_dir

        x, y = self.head
        if   self.direction == Direction.RIGHT: x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:  x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:  y += BLOCK_SIZE
        elif self.direction == Direction.UP:    y -= BLOCK_SIZE

        self.head = Point(x, y)

    def play_step(self, action):
        self.frame_iteration += 1
        # handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # move snake
        self._move(action)
        self.snake.insert(0, self.head)

        # check for collision
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # check for food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    def show_start_screen(self):
        """Draws a ‘press any key to start’ screen and waits for input."""
        self.display.fill(BLACK)
        msg = self.font.render("Press any key to start", True, WHITE)
        x = (self.w - msg.get_width())  // 2
        y = (self.h - msg.get_height()) // 2
        self.display.blit(msg, (x, y))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    game = SnakeGameAI()
    # game.show_start_screen()   # Uncomment for user access to game

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                ##Basic Key directions 
                ##Ensuring snake cannot go in opposite direction 
                    ## e.g Going left and trying to go right
                if event.key == pygame.K_LEFT and game.direction != Direction.RIGHT:
                    game.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and game.direction != Direction.LEFT:
                    game.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and game.direction != Direction.DOWN:
                    game.direction = Direction.UP
                elif event.key == pygame.K_DOWN and game.direction != Direction.UP:
                    game.direction = Direction.DOWN

        reward, game_over, score = game.play_step([1, 0, 0])

        if game_over:
            print('Game over! Final score:', score)
            pygame.quit()
            break
