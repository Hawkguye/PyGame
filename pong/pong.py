import pygame as pg
import math
import random
from sys import exit

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Pong Game')
clock = pg.time.Clock()

pg.font.init()
font = pg.font.SysFont('ariel', 50)
ball_speed = 5

hit_sound = pg.mixer.Sound("hit.wav")
point_sound = pg.mixer.Sound("point.wav")

def getRandomDegree():
    degree = random.uniform(math.pi / 8, math.pi * 3 / 8)
    degree += random.randint(0, 3) * (math.pi / 2)
    return degree

def playHitSound():
    pg.mixer.Sound.play(hit_sound)
def playPointSound():
    pg.mixer.Sound.play(point_sound)

class Paddle:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.geekRect = pg.Rect(posx, posy, width, height)
        self.geek = pg.draw.rect(screen, self.color, self.geekRect)
    
    def display(self):
        self.geek = pg.draw.rect(screen, self.color, self.geekRect)

    def update(self, yFac):
        self.posy += self.speed * yFac
        if self.posy < 0:
            self.posy = 0
        if self.posy + self.height > SCREEN_HEIGHT:
            self.posy = SCREEN_HEIGHT - self.height
        self.geekRect = pg.Rect(self.posx, self.posy, self.width, self.height)

    def getRect(self):
        return self.geekRect

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        degree = getRandomDegree()
        self.Vx = math.cos(degree)
        self.Vy = math.sin(degree)
        self.ball = pg.draw.circle(screen, color, (posx, posy), radius)

    def display(self):
        self.ball = pg.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.Vx
        self.posy += self.speed * self.Vy

        if self.posy <= 0 or self.posy >= SCREEN_HEIGHT:
            self.Vy *= -1
            self.speed += 0.2
            playHitSound()

        if self.posx <= 0:
            return -1
        if self.posx >= SCREEN_WIDTH:
            return 1
        return 0
    
    def hit(self):
        self.Vx *= -1
        self.speed += 0.5
        playHitSound()

    def reset(self):
        self.posx = SCREEN_WIDTH / 2
        self.posy = SCREEN_HEIGHT / 2
        degree = getRandomDegree()
        self.Vx = math.cos(degree)
        self.Vy = math.sin(degree)
        self.speed = ball_speed

    def getRect(self):
        return self.ball

paddle_height = 80
paddle_a = Paddle(20, SCREEN_HEIGHT / 2 - paddle_height / 2, 10, paddle_height, 10, "white")
paddle_b = Paddle(SCREEN_WIDTH - 30, SCREEN_HEIGHT / 2 - paddle_height / 2, 10, paddle_height, 10, "white")
ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 10, ball_speed, "white")

paddle_a_facy, paddle_b_facy = 0, 0
score_a, score_b = 0, 0
lastHit = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                paddle_a_facy = -1
            if event.key == pg.K_s:
                paddle_a_facy = 1
            if event.key == pg.K_UP:
                paddle_b_facy = -1
            if event.key == pg.K_DOWN:
                paddle_b_facy = 1
        if event.type == pg.KEYUP:
            if event.key == pg.K_w or event.key == pg.K_s:
                paddle_a_facy = 0
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                paddle_b_facy = 0

    screen.fill("black") 
    pg.draw.line(screen, "white", (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT), 8)

    # detect collision
    if pg.Rect.colliderect(paddle_a.getRect(), ball.getRect()) and lastHit != -1:
        ball.hit()
        lastHit = -1
    if pg.Rect.colliderect(paddle_b.getRect(), ball.getRect()) and lastHit != 1:
        ball.hit()
        lastHit = 1

    # update paddles
    paddle_a.update(paddle_a_facy)
    paddle_b.update(paddle_b_facy)

    # update balls and points
    point = ball.update()
    if point == -1:
        score_b += 1
    if point == 1:
        score_a += 1
    if point:
        ball.reset()
        lastHit = 0
        playPointSound()

    paddle_a.display()
    paddle_b.display()
    ball.display()

    # score text display
    score_text = font.render(str(score_a) + "  :  " + str(score_b), True, "white")
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (SCREEN_WIDTH / 2, 40)
    screen.blit(score_text, score_text_rect)

    pg.display.update()
    dt = clock.tick(60) / 1000