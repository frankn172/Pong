import pygame
import sys
import random
from pygame.sprite import Sprite
from pygame.sprite import Group


class Ball(Sprite):
    def __init__(self, settings, screen, left_paddle):
        super(Ball, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(0, 0, settings.ball_width, settings.ball_height)
        self.rect.centery = self.screen_rect.centery
        self.rect.centerx = self.screen_rect.centerx
        self.x = int(self.rect.x)
        self.y = int(self.rect.y)
        self.color = settings.ball_color
        self.speed = settings.ball_speed
        self.radius = settings.ball_radius

    def collision_left_right(self, stats, sb, left_paddle, right_paddle):
        return self.rect.colliderect(left_paddle.rect) or self.rect.colliderect(right_paddle.rect)

    def collision_top_bottom(self, top_paddle, bottom_paddle, top_left, bottom_right):
        return self.rect.colliderect(top_paddle.rect) or self.rect.colliderect(bottom_paddle.rect) \
               or self.rect.colliderect(top_left.rect) or self.rect.colliderect(bottom_right.rect)

    def check_horizontal_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.top <= 0)

    def check_vertical_edges(self):
        return (self.rect.bottom >= 800) or (self.rect.top <= 0)

    def update(self, settings):
        self.x += settings.ball_x_direction * settings.ball_speed
        self.y -= settings.ball_y_direction * settings.ball_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_ball(self):
        pygame.draw.circle(self.screen, self.color, (self.rect.centerx, self.rect.centery), self.radius)


class BottomPaddle(Sprite):
    def __init__(self, settings, screen):
        super(BottomPaddle, self).__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('paddle_horizontal.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.color = settings.bottom_paddle_color
        self.height = int(settings.bottom_paddle_height)
        self.rect.centerx = 300
        self.rect.bottom = self.screen_rect.bottom
        self.center = int(self.rect.centerx)
        self.moving_left = False
        self.moving_right = False

    def update(self, settings):
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.bottom_paddle_speed
        if self.moving_right and self.rect.right < 600:
            self.center += self.settings.bottom_paddle_speed
        self.rect.centerx = self.center

    def center_bottom_paddle(self):
        self.center = self.screen_rect.midleft

    def draw_bottom_paddle(self):
        self.screen.blit(self.image, self.rect)


class LeftPaddle(Sprite):
    def __init__(self, settings, screen):
        super(LeftPaddle, self).__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('paddle_vertical.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.color = settings.left_paddle_color
        self.height = int(settings.left_paddle_height)
        self.rect.centery = self.screen_rect.centery
        self.rect.left = self.screen_rect.left
        self.center = int(self.rect.centery)
        self.moving_up = False
        self.moving_down = False

    def update(self, settings):
        if self.moving_up and self.rect.top > 0:
            self.center -= self.settings.left_paddle_speed
        if self.moving_down and self.rect.bottom < 800:
            self.center += self.settings.left_paddle_speed
        self.rect.centery = self.center

    def center_left_paddle(self):
        self.center = self.screen_rect.midleft

    def draw_left_paddle(self):
        self.screen.blit(self.image, self.rect)


class RightPaddle(Sprite):
    def __init__(self, settings, screen):
        super(RightPaddle, self).__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('paddle_vertical.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.color = settings.right_paddle_color
        self.height = int(settings.right_paddle_height)
        self.rect.centery = self.screen_rect.centery
        self.rect.right = self.screen_rect.right
        self.y = int(self.rect.centery)
        self.speed = settings.right_paddle_speed
        self.moving_up = False
        self.moving_down = False

    def update(self, settings, balls):
        for ball in balls.sprites():
            if ball.rect.centerx > settings.right_reflex:
                self.y += settings.right_paddle_y_direction * settings.right_paddle_speed / settings.computer_slow
            else:
                self.y -= settings.right_paddle_y_direction * settings.right_paddle_speed / settings.computer_slow
        self.rect.y = self.y

    def check_edges(self):
        return (self.rect.top < 0) or (self.rect.bottom > 800)

    def draw_right_paddle(self):
        self.screen.blit(self.image, self.rect)


class TopPaddle(Sprite):
    def __init__(self, settings, screen):
        super(TopPaddle, self).__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('paddle_horizontal.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.color = settings.top_paddle_color
        self.height = int(settings.top_paddle_height)
        self.rect.centerx = 900
        self.rect.top = self.screen_rect.top
        self.x = int(self.rect.x)

        self.speed = settings.top_paddle_speed
        self.moving_right = False
        self.moving_left = False

    def update(self, settings, balls):
        for ball in balls.sprites():
            if ball.rect.centerx + settings.computer_slow > self.rect.centerx:
                self.x += settings.top_paddle_x_direction * settings.top_paddle_speed
            else:
                self.x -= settings.top_paddle_x_direction * settings.top_paddle_speed
        self.rect.x = self.x

    def center_top_paddle(self):
        self.center = self.screen_rect.midright

    def check_edges(self):
        return (self.rect.left <= 600) or (self.rect.right >= 1200)

    def draw_top_paddle(self):
        self.screen.blit(self.image, self.rect)


class BottomRight(Sprite):
    def __init__(self, settings, screen):
        super(BottomRight, self).__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('paddle_horizontal.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.color = settings.bottom_right_color
        self.height = int(settings.bottom_right_height)
        self.rect.centerx = 900
        self.rect.bottom = self.screen_rect.bottom
        self.x = int(self.rect.x)
        self.speed = settings.bottom_right_speed
        self.moving_left = False
        self.moving_right = False

    def update(self, settings, balls):
        for ball in balls.sprites():
            if ball.rect.centerx + settings.computer_slow > self.rect.centerx:
                self.x += settings.bottom_right_x_direction * settings.bottom_right_speed
            else:
                self.x -= settings.bottom_right_x_direction * settings.bottom_right_speed
        self.rect.x = self.x

    def center_bottom_right(self):
        self.center = self.screen_rect.midright

    def check_edges(self):
        return (self.rect.left <= 600) or (self.rect.right >= 1200)

    def draw_bottom_right(self):
        self.screen.blit(self.image, self.rect)


class TopLeft(Sprite):
    def __init__(self, settings, screen):
        super(TopLeft, self).__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('paddle_horizontal.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.color = settings.left_paddle_color
        self.height = int(settings.top_left_height)
        self.rect.centerx = 300
        self.rect.top = self.screen_rect.top
        self.center = int(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def update(self, settings):
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.bottom_paddle_speed
        if self.moving_right and self.rect.right < 600:
            self.center += self.settings.bottom_paddle_speed
        self.rect.centerx = self.center

    def center_top_left(self):
        self.center = self.screen_rect.midleft

    def check_edges(self):
        return (self.rect.left <= 600) or (self.rect.right >= 1200)

    def draw_top_left(self):
        self.screen.blit(self.image, self.rect)


class Button:
    def __init__(self, settings, screen, message):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_message(message)

    def prep_message(self, message):
        self.message_image = self.font.render(message, True, self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)


class CenterLine(Sprite):
    def __init__(self, settings, screen):
        super(CenterLine, self).__init__()
        self.screen = screen
        self.settings = settings
        self.rect = pygame.Rect(0, 0, settings.center_line_width, settings.center_line_height)
        self.screen_rect = screen.get_rect()
        self.color = settings.center_line_color
        self.height = int(settings.left_paddle_height)
        self.rect.centery = self.screen_rect.centery
        self.rect.centerx = self.screen_rect.centerx

    def draw_center_line(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = False
        self.start_game = False
        self.player_wins = False
        self.computer_wins = False
        self.score = 0
        self.player_score = 0
        self.computer_score = 0

    def reset_stats(self):
        self.left_paddle_left = self.settings.left_paddle_limit


class Scoreboard:
    def __init__(self, settings, screen, stats, message):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.player_color = (0, 0, 255)
        self.computer_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_player_wins(message)
        self.prep_computer_wins(message)
        self.prep_player_score_label()
        self.prep_computer_score_label()
        self.prep_player_score()
        self.prep_computer_score()

    def prep_player_wins(self, message):
        winner = message
        self.player_wins_image = self.font.render(winner, True, self.player_color, self.settings.bg_color)
        self.player_wins_rect = self.player_wins_image.get_rect()
        self.player_wins_rect.centerx = self.screen_rect.centerx - 20
        self.player_wins_rect_centery = self.screen_rect.centery

    def prep_computer_wins(self, message):
        winner = message
        self.computer_wins_image = self.font.render(winner, True,
                                                    self.player_color, self.settings.bg_color)
        self.computer_wins_rect = self.computer_wins_image.get_rect()
        self.computer_wins_rect.centerx = self.screen_rect.centerx - 20
        self.computer_wins_rect.centery = self.screen_rect.centery - 40


    def prep_player_score_label(self):
        label_str = "Player Score: "
        self.player_score_label_image = self.font.render(label_str, True, self.player_color, self.settings.bg_color)
        self.player_score_label_rect = self.player_score_label_image.get_rect()
        self.player_score_label_rect.centerx = self.screen_rect.centerx - 490
        self.player_score_label_rect.top = 30

    def prep_player_score(self):
        score_str = str(self.stats.player_score)
        self.player_score_image = self.font.render(score_str, True, self.player_color, self.settings.bg_color)
        self.player_score_rect = self.player_score_image.get_rect()
        self.player_score_rect.centerx = self.screen_rect.centerx - 400
        self.player_score_rect.top = 30


    def prep_computer_score_label(self):
        label_str = "Computer Score: "
        self.computer_score_label_image = self.font.render(label_str, True, self.computer_color, self.settings.bg_color)
        self.computer_score_label_rect = self.computer_score_label_image.get_rect()
        self.computer_score_label_rect.centerx = self.screen_rect.centerx + 290
        self.computer_score_label_rect.top = 30

    def prep_computer_score(self):
        score_str = str(self.stats.computer_score)
        self.computer_score_image = self.font.render(score_str, True, self.computer_color, self.settings.bg_color)
        self.computer_score_rect = self.computer_score_image.get_rect()
        self.computer_score_rect.centerx = self.screen_rect.centerx + 400
        self.computer_score_rect.top = 30


    def show_score(self):
        self.screen.blit(self.player_score_image, self.player_score_rect)
        self.screen.blit(self.computer_score_image, self.computer_score_rect)
        self.screen.blit(self.player_score_label_image, self.player_score_label_rect)
        self.screen.blit(self.computer_score_label_image, self.computer_score_label_rect)
        self.screen.blit(self.player_wins_image, self.player_wins_rect)
        self.screen.blit(self.computer_wins_image, self.computer_wins_rect)


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.start_color = (0, 0, 0)
        self.computer_slow = 3
        self.left_paddle_width = self.screen_width / 32
        self.left_paddle_height = self.screen_height / 3
        self.left_paddle_color = 0, 0, 255
        self.left_paddle_speed = 1.5
        self.left_paddle_limit = 3
        self.center_line_width = 5
        self.center_line_height = self.screen_height
        self.center_line_color = 255, 255, 255
        self.bottom_paddle_width = self.screen_width / 5
        self.bottom_paddle_height = self.screen_height / 32
        self.bottom_paddle_color = 0, 0, 255
        self.bottom_paddle_speed = 2
        self.bottom_paddle_limit = 1
        self.top_left_width = self.screen_width / 5
        self.top_left_height = self.screen_height / 32
        self.top_left_color = 0, 0, 255
        self.top_left_speed = 2
        self.top_left_limit = 1
        self.top_paddle_width = self.screen_width / 5
        self.top_paddle_height = self.screen_height / 32
        self.top_paddle_color = 255, 0, 0
        self.top_paddle_speed = 1
        self.top_paddle_limit = 1
        self.top_paddle_x_direction = 1
        self.bottom_right_width = self.screen_width / 5
        self.bottom_right_height = self.screen_height / 32
        self.bottom_right_color = 255, 0, 0
        self.bottom_right_speed = 1
        self.bottom_right_limit = 1
        self.bottom_right_x_direction = 1
        self.right_paddle_width = self.screen_width / 32
        self.right_paddle_height = self.screen_height / 3
        self.right_paddle_color = 255, 0, 0,
        self.right_paddle_speed = 1.5
        self.right_paddle_limit = 1
        self.right_paddle_y_direction = 1
        self.right_reflex = (self.screen_width * 3) / 4
        self.ball_speed = .6
        self.ball_width = 16
        self.ball_height = 16
        self.ball_radius = 8
        self.ball_color = 60, 60, 60
        self.balls_allowed = 1
        self.ball_x_direction = 1
        self.ball_y_direction = 1
        self.points = 1
        self.player_score = 1
        self.computer_score = 1


def check_ball_edges(settings, balls):
    for ball in balls.sprites():
        if ball.check_horizontal_edges():
            change_ball_direction_horizontal(settings, balls)
            break
        elif ball.check_vertical_edges():
            change_ball_direction_vertical(settings, balls)
            break


def check_top_paddle_edges(settings, top_paddle):
    if top_paddle.check_edges():
        settings.top_paddle_x_direction *= -1


def check_bottom_right_edges(settings, bottom_right):
    if bottom_right.check_edges():
        settings.bottom_right_x_direction *= -1


def check_right_edges(settings, right_paddle):
    if right_paddle.check_edges():
        settings.right_paddle_y_direction *= -1


def change_ball_direction_horizontal(settings, balls):
    for ball in balls.sprites():
        ball.rect.x += settings.ball_speed
    settings.ball_x_direction *= -1


def change_ball_direction_vertical(settings, balls):
    for ball in balls.sprites():
        ball.rect.y -= settings.ball_speed
    settings.ball_y_direction *= -1


def update_top_paddle(settings, top_paddle):
    check_top_paddle_edges(settings, top_paddle)


def update_bottom_right(settings, bottom_right):
    check_bottom_right_edges(settings, bottom_right)


def update_right_paddle(settings, right_paddle):
    check_right_edges(settings, right_paddle)


def update_balls(settings, stats, screen, sb, left_paddle, right_paddle, bottom_paddle, top_paddle,
                 top_left, bottom_right, balls):
    balls.update(settings)
    if len(balls) == 0:
        sb.prep_computer_wins('Press Space')
    for ball in balls.copy():
        if ball.rect.left <= 0 or ball.rect.top <= 0 \
                and ball.rect.left < 600 or ball.rect.bottom >= 800 \
                and ball.rect.left < 600:
            pygame.mixer.init()
            pygame.mixer.music.load('hit.wav')
            pygame.mixer.music.play()
            x = random.randint(1, 2)
            if x % 2 == 0:
                change_ball_direction_horizontal(settings, balls)
                change_ball_direction_vertical(settings, balls)

            stats.computer_score += 1
            sb.prep_computer_score()
            balls.remove(ball)
            if stats.computer_score > 3:
                sb.prep_player_wins('Computer wins at 5!')
                pygame.time.delay(1000)
                pygame.mixer.music.load('lost.ogg')
                pygame.mixer.music.play()
            if stats.computer_score > 4:

                pygame.mixer.music.load('lost.ogg')
                pygame.mixer.music.play()

                stats.computer_score = 0
                stats.player_score = 0
                settings.ball_speed = .5
                settings.top_paddle_speed = 2
                settings.bottom_paddle_speed = 2
                settings.top_left_speed = 2
                settings.bottom_right_speed = 2
                settings.computer_slow = 5
                stats.game_active = False
                pygame.mouse.set_visible(True)

        elif ball.rect.right >= 1200 or ball.rect.right > 600\
                and ball.rect.top <= 0 or ball.rect.right > 600\
                and ball.rect.bottom >= 800:

            pygame.mixer.init()
            pygame.mixer.music.load('won.ogg')
            pygame.mixer.music.play()

            x = random.randint(1, 2)
            if x % 2 == 0:
                change_ball_direction_horizontal(settings, balls)
                change_ball_direction_vertical(settings, balls)

            stats.player_score += 1
            sb.prep_player_score()
            balls.remove(ball)
            if stats.player_score > 4:
                if settings.computer_slow > 1.25:
                    settings.computer_slow -= .25
                sb.prep_player_wins('PLAYER WINS!')
                stats.player_score = 0
                sb.prep_player_score()
                stats.computer_score = 0
                sb.prep_computer_score()

                if settings.ball_speed < 1.0:
                    settings.ball_speed += .1
                else:
                    settings.ball_speed += .02

    for ball in balls.sprites():
        if ball.collision_left_right(stats, sb, left_paddle, right_paddle):
            pygame.mixer.music.load('hit.wav')
            pygame.mixer.music.play()
            change_ball_direction_horizontal(settings, balls)

    for ball in balls.sprites():
        if ball.collision_top_bottom(top_paddle, bottom_paddle, top_left, bottom_right):
            pygame.mixer.music.load('hit.wav')
            pygame.mixer.music.play()
            change_ball_direction_vertical(settings, balls)


def check_keydown_events(event, settings, screen, left_paddle, top_left, bottom_paddle, balls, sb):
    if event.key == pygame.K_w or event.key == pygame.K_UP:
        left_paddle.moving_up = True
    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
        left_paddle.moving_down = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        bottom_paddle.moving_left = True
        top_left.moving_left = True
    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        bottom_paddle.moving_right = True
        top_left.moving_right = True
    elif event.key == pygame.K_SPACE:
        sb.prep_player_wins("")
        sb.prep_computer_wins("")
        if len(balls) < settings.balls_allowed:
            new_ball = Ball(settings, screen, left_paddle)
            balls.add(new_ball)


def check_events(settings, screen, stats, sb, play_button, left_paddle, top_left, bottom_paddle, balls):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, left_paddle, top_left, bottom_paddle, balls, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, left_paddle, top_left, bottom_paddle)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button,
                    left_paddle, balls, mouse_x, mouse_y)


def check_play_button(settings, screen, stats, sb, play_button, left_paddle, balls, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        pygame.mixer_music.stop()
        stats.computer_score = 0
        stats.player_score = 0
        sb.prep_player_score()
        sb.prep_computer_score()


def update_screen(settings, screen, stats, sb, left_paddle, right_paddle, bottom_paddle, center_line,
                  top_paddle, top_left, bottom_right, balls, play_button):
    screen.fill(settings.bg_color)
    center_line.draw_center_line()
    left_paddle.draw_left_paddle()
    right_paddle.draw_right_paddle()
    bottom_paddle.draw_bottom_paddle()
    top_paddle.draw_top_paddle()
    top_left.draw_top_left()
    bottom_right.draw_bottom_right()
    for ball in balls.sprites():
        ball.draw_ball()
    sb.show_score()
    if not stats.game_active:
        sb.prep_player_wins("")
        sb.prep_computer_wins("COMPUTER WINS!")
        screen.fill(settings.start_color)
        play_button.draw_button()
    pygame.display.flip()


def check_keyup_events(event, left_paddle, top_left, bottom_paddle):
    if event.key == pygame.K_w or event.key == pygame.K_UP:
        left_paddle.moving_up = False
    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
        left_paddle.moving_down = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        bottom_paddle.moving_left = False
        top_left.moving_left = False
    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        bottom_paddle.moving_right = False
        top_left.moving_right = False


def run_game():
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Pong")

    start_game = False

    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats, "")

    left_paddle = LeftPaddle(settings, screen)
    right_paddle = RightPaddle(settings, screen)
    bottom_paddle = BottomPaddle(settings, screen)
    top_paddle = TopPaddle(settings, screen)
    top_left = TopLeft(settings, screen)
    center_line = CenterLine(settings, screen)
    bottom_right = BottomRight(settings, screen)
    balls = Group()

    play_button = Button(settings, screen, "Play")

    while True:
        check_events(settings, screen, stats, sb, play_button, left_paddle, top_left, bottom_paddle, balls)
        if stats.game_active:
            left_paddle.update(settings)
            right_paddle.update(settings, balls)
            bottom_paddle.update(settings)
            top_paddle.update(settings, balls)
            bottom_right.update(settings, balls)
            top_left.update(settings)

            update_balls(settings, stats, screen, sb, left_paddle, right_paddle, bottom_paddle, top_paddle,
                         top_left, bottom_right, balls)

            update_top_paddle(settings, top_paddle)
            update_bottom_right(settings, bottom_right)
            update_right_paddle(settings, right_paddle)

        update_screen(settings, screen, stats, sb, left_paddle, right_paddle, bottom_paddle, center_line,
                      top_paddle, top_left, bottom_right, balls, play_button)


run_game()
