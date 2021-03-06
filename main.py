import pygame
from sys import exit as sys_exit
from random import randint

class Paddle:
    def __init__(self):
        self.paddle_rect = pygame.Rect(0,0,20,100)
        self.score = 0
    
    def movement(self):
        pass

    def update(self):
        pygame.draw.rect(screen, "Black", self.paddle_rect)
        self.movement()
        pygame.draw.rect(screen, "White", self.paddle_rect)

class PlayerPaddle(Paddle):
    def __init__(self):
        super().__init__()
        self.paddle_rect.center = (20, 250)

    def movement(self):
        global keys
        if keys[pygame.K_w] and self.paddle_rect.top > 0:
            self.paddle_rect.y -= 3
        if keys[pygame.K_s] and self.paddle_rect.bottom < 500:
            self.paddle_rect.y += 3

class ComputerPaddle(Paddle):
    def __init__(self):
        super().__init__()
        self.paddle_rect.center = (780, 250)

    def movement(self, ball_center,ball_velocity_x, ball_velocity_y):
        if self.paddle_rect.centery != ball_center[1] and ball_velocity_x < 0:
            if ball_velocity_y >= 0 and self.paddle_rect.top >= 0 and ball_center[1] < self.paddle_rect.centery:
                self.paddle_rect.y -= 3
            elif ball_velocity_y <= 0 and self.paddle_rect.bottom <= 500 and ball_center[1] > self.paddle_rect.centery:
                self.paddle_rect.y += 3

    def update(self, ball_center,ball_velocity_x, ball_velocity_y):
        pygame.draw.rect(screen, "Black", self.paddle_rect)
        self.movement(ball_center,ball_velocity_x, ball_velocity_y)
        pygame.draw.rect(screen, "White", self.paddle_rect)

class Ball:
    def __init__(self):
        self.ball_rect = pygame.Rect(0,0,10,10)
        self.ball_rect.center = (400, 250)
        self.velocity_x = 6
        self.velocity_y = randint(-2,2)

    def update(self):
        pygame.draw.rect(screen, "Black", self.ball_rect)
        self.movement()
        pygame.draw.rect(screen, "White", self.ball_rect)

    def collision(self, paddle_rect, paddle_rect_2):
        if self.ball_rect.left < 30:
            if self.ball_rect.colliderect(paddle_rect):
                if keys[pygame.K_w]:
                    self.velocity_y += 3
                if keys[pygame.K_s]:
                    self.velocity_y -= 3
                self.velocity_x = -self.velocity_x
        if self.ball_rect.right > 490:
            if self.ball_rect.colliderect(paddle_rect_2):
                self.velocity_x = -self.velocity_x
        if self.ball_rect.top < 0 or self.ball_rect.bottom > 500:
            self.velocity_y = -self.velocity_y

    def movement(self):
        self.ball_rect.x -= self.velocity_x
        self.ball_rect.y -= self.velocity_y

    def score_and_reset(self):
        if self.ball_rect.right <= -20:
            self.ball_rect.center = (400, 250)
            self.velocity_y = randint(-2, 2)
            self.velocity_x = -self.velocity_x
            return [0,1]
        if self.ball_rect.left >= 820:
            self.ball_rect.center = (400, 250)
            self.velocity_y = randint(-2, 2)
            self.velocity_x = -self.velocity_x
            return [1,0]
        else: return []

pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Pong")
FPS = 60
fpsclock = pygame.time.Clock()
score_font = pygame.font.Font("Fonts\ARIAL.TTF", 30)
text_font = pygame.font.Font("Fonts\ARIAL.TTF", 45)
game_active = False

player_paddle = PlayerPaddle()
computer_paddle = ComputerPaddle()
ball = Ball()

while True:
    keys = pygame.key.get_pressed()
    if game_active:
        player_paddle.update()
        computer_paddle.update(ball.ball_rect.center,ball.velocity_x, ball.velocity_y)
        ball.collision(player_paddle.paddle_rect, computer_paddle.paddle_rect)
        ball.update()
        return_list = ball.score_and_reset()

        if return_list:
            score_list = [player_paddle.score, computer_paddle.score]
            for i in range(0,2):
                score_list[i] =score_list[i] + return_list[i]
            player_paddle.score = score_list[0]
            computer_paddle.score = score_list[1]    

        #fps
        fps_surf = score_font.render(f"FPS:{int(fpsclock.get_fps())}",True, "White","Black")
        fps_rect = fps_surf.get_rect(topright = (800, 0))
        screen.blit(fps_surf, fps_rect)

        #score
        player_score_surf = score_font.render(f"{player_paddle.score}",True, "White", "Black")
        player_score_rect = player_score_surf.get_rect(center = (200, 125))
        screen.blit(player_score_surf, player_score_rect)

        computer_score_surf = score_font.render(f"{computer_paddle.score}",True, "White", "Black")
        computer_score_rect = computer_score_surf.get_rect(center = (600, 125))
        screen.blit(computer_score_surf, computer_score_rect)
        pygame.draw.aaline(screen, "White", (400,0), (400,500))

        if player_paddle.score == 10 or computer_paddle.score == 10:
            game_active = False

    else:
        screen.fill("Black")
        start_surf = text_font.render("Press space to start", True, "White", "Black")
        start_rect = start_surf.get_rect(center = (400, 250))

        if player_paddle.score > computer_paddle.score:
            win_surf = text_font.render("You won!", True, "White", "Black")
            win_rect = win_surf.get_rect(midbottom = start_rect.midtop)
            screen.blits(([win_surf, win_rect], [start_surf, start_rect]))
        elif player_paddle.score < computer_paddle.score:
            win_surf = text_font.render("You lost :(", True, "White", "Black")
            win_rect = win_surf.get_rect(midbottom = start_rect.midtop)
            screen.blits(([win_surf, win_rect], [start_surf, start_rect]))
        else: screen.blit(start_surf, start_rect)

        if keys[pygame.K_SPACE]:
            screen.fill("Black")
            player_paddle.score = 0
            computer_paddle.score = 0
            game_active = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys_exit()
    pygame.display.update()
    fpsclock.tick(FPS)