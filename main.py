import pygame
from sys import exit as sys_exit
from random import randint

class Paddle:
    def __init__(self):
        self.paddle_rect = pygame.Rect(0,0,20,100)
        self.score = 0

    def update(self):
        pygame.draw.rect(screen, "Black", self.paddle_rect)
        self.movement()
        pygame.draw.rect(screen, "White", self.paddle_rect)

class PlayerPaddle(Paddle):
    def __init__(self):
        super().__init__()
        self.paddle_rect.center = (20, 250)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.paddle_rect.top > 0:
            self.paddle_rect.y -= 3
        if keys[pygame.K_s] and self.paddle_rect.bottom < 500:
            self.paddle_rect.y += 3

class ComputerPaddle(Paddle):
    def __init__(self):
        super().__init__()
        self.paddle_rect.center = (780, 250)

    def movement(self):
        pass

class Ball:
    def __init__(self):
        self.ball_rect = pygame.Rect(0,0,10,10)
        self.ball_rect.center = (400, 250)
        self.velocity_x = 6
        self.velocity_y = randint(0,3)

    def update(self, paddle_rect, paddle_rect_2):
        pygame.draw.rect(screen, "Black", self.ball_rect)
        self.movement()
        self.collision(paddle_rect, paddle_rect_2)
        pygame.draw.rect(screen, "White", self.ball_rect)

    def collision(self, paddle_rect, paddle_rect_2):
        if self.ball_rect.colliderect(paddle_rect) or self.ball_rect.colliderect(paddle_rect_2):
            self.velocity_x = -self.velocity_x
            self.velocity_y = -self.velocity_y
        if self.ball_rect.top < 0 or self.ball_rect.bottom > 500:
            self.velocity_y = -self.velocity_y

    def movement(self):
        self.ball_rect.x -= self.velocity_x
        self.ball_rect.y -= self.velocity_y

    def reset_and_tally_score(self):
        if self.ball_rect.right < 0:
            self.ball_rect.center = (400, 250)
            self.velocity_y = randint(0,3)
            return 1

pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Pong")
FPS = 60
fpsclock = pygame.time.Clock()
score_font = pygame.font.Font("Fonts\ARIAL.TTF", 30)

player_paddle = PlayerPaddle()
computer_paddle = ComputerPaddle()
ball = Ball()

while True:
    player_paddle.update()
    computer_paddle.update()
    ball.update(player_paddle.paddle_rect, computer_paddle.paddle_rect)

    #score
    score_surf = score_font.render(f"FPS:{int(fpsclock.get_fps())}",True, "White","Black")
    score_rect = score_surf.get_rect(topright = (800, 0))
    screen.blit(score_surf, score_rect)

    pygame.draw.aaline(screen, "White", (400,0), (400,500))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys_exit()
    pygame.display.update()
    fpsclock.tick(60)