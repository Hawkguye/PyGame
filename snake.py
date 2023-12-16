import pygame as pg
import random
import queue
from time import sleep
from sys import exit

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_WIDTH = 30
GRID_WIDTH = SCREEN_WIDTH // CELL_WIDTH # 20
GRID_HEIGHT = SCREEN_HEIGHT // CELL_WIDTH

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Snake')
clock = pg.time.Clock()

pg.font.init()
big_font = pg.font.SysFont('comic sans', 100)
small_font = pg.font.SysFont('tahona', 30)

isRunning = False
grid = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
snake_speed = 5

def GameOver():
    screen.fill("black")

    text = big_font.render("GAME OVER", True, "green")
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.4)
    screen.blit(text, text_rect)

    score_text = small_font.render("LENGTH: " + str(snake.length), True, "white")
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.6)
    screen.blit(score_text, score_text_rect)
    pg.display.update()

    sleep(2)
    
class Snake:
    def __init__(self, posx, posy, width, Vx, Vy):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.Vx = Vx
        self.Vy = Vy
        self.length = 3
        self.cells = []
        for i in range(2, -1, -1):
            cellx, celly = posx - Vx * i, posy - Vy * i
            self.cells.append((cellx, celly))
            grid[cellx][celly] = 1

    def changeDir(self, facX, facY):
        if self.Vx == facX * -1 or self.Vy == facY * -1:
            return
        self.Vx = facX
        self.Vy = facY

    def update(self):
        ifEat = False
        self.posx += self.Vx
        self.posy += self.Vy

        # boundary control
        if self.posx < 0:
            self.posx = GRID_HEIGHT - 1
        if self.posy < 0:
            self.posy = GRID_WIDTH - 1
        self.posx %= GRID_HEIGHT
        self.posy %= GRID_WIDTH
#        print(str(self.posx) + ", " + str(self.posy))

        # collision detection
        if grid[self.posx][self.posy] == 2:
            ifEat = True
            global snake_speed
            if snake_speed != 10:
                snake_speed += 0.1
            self.length += 1
            food.touch()
        if grid[self.posx][self.posy] == 1:
            GameOver()
            return False

        self.cells.append((self.posx, self.posy))
        grid[self.posx][self.posy] = 1

        if not ifEat:
            (cellx, celly) = self.cells[0]
            for i in range(len(self.cells) - 1):
                self.cells[i] = self.cells[i+1]
            self.cells.pop()
            grid[cellx][celly] = 0

        return True

    def display(self):
        for (cellx, celly) in self.cells:
            pg.draw.rect(screen, "white", (cellx * CELL_WIDTH, celly * CELL_WIDTH, (CELL_WIDTH - 0.5), (CELL_WIDTH - 0.5)))

def getFoodPos():
    posx = random.randint(0, GRID_HEIGHT-1)
    posy = random.randint(0, GRID_WIDTH-1)
    if grid[posx][posy] != 0:
        return getFoodPos()
    return posx, posy

class Food:
    def __init__(self):
        self.posx, self.posy = getFoodPos()
        grid[self.posx][self.posy] = 2

    def update(self):
        pg.draw.circle(screen, "red", (self.posx * CELL_WIDTH + CELL_WIDTH // 2, self.posy * CELL_WIDTH + CELL_WIDTH // 2), CELL_WIDTH/2)

    def touch(self):
        self.posx, self.posy = getFoodPos()
        grid[self.posx][self.posy] = 2



while True:
    if not isRunning:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    isRunning = True
                    for i in range(SCREEN_HEIGHT):
                        for j in range(SCREEN_WIDTH):
                            grid[i][j] = 0
                    snake = Snake(GRID_HEIGHT // 2, GRID_WIDTH // 2, CELL_WIDTH, 1, 0)
                    food = Food()
                    keys = queue.Queue(0)
                    tick = 0
        
        screen.fill("black")
        pong_text = big_font.render("SNAKE", True, "white")
        pong_text_rect = pong_text.get_rect()
        pong_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.4)
        screen.blit(pong_text, pong_text_rect)

        click_text = small_font.render("PRESS SPACE TO START", True, "white")
        click_text_rect = click_text.get_rect()
        click_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.6)
        screen.blit(click_text, click_text_rect)
        pg.display.update()
        clock.tick(60)

    if isRunning:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    keys.put("up")
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    keys.put("down")
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    keys.put("left")
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    keys.put("right")
        if tick == 0:
            try:
                move = keys.get(False)
                print(move)
                if move == "up":
                    snake.changeDir(0, -1)
                if move == "down":
                    snake.changeDir(0, 1)
                if move == "left":
                    snake.changeDir(-1, 0)
                if move == "right":
                    snake.changeDir(1, 0)
            except:
                pass
            
            # for i in range(20):
            #     for j in range(20):
            #         print(grid[i][j], end=" ")
            #     print()

            screen.fill("black")

            isRunning = snake.update()
            if not isRunning:
                continue
        
            food.update()
            snake.display()

            pg.display.update()
        
        clock.tick(60)
        tick = (tick+1) % (60 // snake_speed)