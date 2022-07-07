import pickle
from turtle import width
from django import conf
import neat
import pygame
import os 
import random
import time

# initializing the pygame.
pygame.init()

# variable for height and width of screen
WIDTH, HEIGHT = 700, 500
GEN = 0
# setting font for the score. 
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
TIME_FONT = pygame.font.SysFont("comicsans", 20)

# Creating Window and setting caption for it.
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong game")

curr_dir = os.path.curdir

# Images
PRE_WINDOW_IMAGE = pygame.image.load(os.path.join(curr_dir, 'IMG//1.png'))
MIDDLE_WINDOW_IMAGE_2 = pygame.image.load(os.path.join(os.curdir, 'IMG//2.png'))
MIDDLE_WINDOW_IMAGE_1 = pygame.image.load(os.path.join(curr_dir, 'IMG//3.png'))
PLAY_AGAIN = pygame.image.load(os.path.join(curr_dir, 'IMG//playagain.png'))
RIGHT_WIN= pygame.image.load(os.path.join(curr_dir, 'IMG//rightwin.png'))
LEFT_WIN= pygame.image.load(os.path.join(curr_dir, 'IMG//leftwin.png'))

# sounds
HIT = pygame.mixer.Sound(os.path.join(os.curdir,'sound//hit.wav'))
POINT = pygame.mixer.Sound(os.path.join(os.curdir,'sound//point.wav'))

# COLOR IN RGB
WHITE = (255,255,255)
BLACK = (0,0,0)

# Fram Per Second.
FPS = 60

# Winning Score
WINNING_SCORE = 10

# Class for creating paddles
class Paddle:
    COLOR = WHITE
    VELOCITY = 4
    width = 20
    height = 100
    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
    
    def move(self, up=True):
        # if up is true we have to subtract velocity to move the paddle up
        if up:
            self.y-= self.VELOCITY
        else:
            self.y+= self.VELOCITY
        if self.y <= 0  or self.y + self.height >= HEIGHT:
            return False
        return

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

# class ball for creating ball object.
class Ball:
    COLOR = WHITE
    radius = 7
    MAX_VEL = 5
    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.x_vel = self.MAX_VEL * random.choice((1,-1))
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x+= self.x_vel
        self.y+= self.y_vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel*= -1
        self.y_vel = 0


# function for pre-game window.
def pre_window(win):
    win.fill(BLACK)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 3
        win.blit(PRE_WINDOW_IMAGE, (0,0))
        pygame.display.update()

def middle_window(win, img):
    win.fill(BLACK)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
        win.blit(img, (0,0))
        pygame.display.update()

# Function for displaying wining window.
def winning_window(win, win_img, high = None):
    win.fill(BLACK)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
        if high == None:
            win.blit(win_img, (0, HEIGHT// 2 - win_img.get_height()))
        else:
            time_text = SCORE_FONT.render(f'Time Played: {get_time(high[1])}', 1, WHITE)
            high_text = SCORE_FONT.render(f'Max survival Time: {get_time(high[0])}', 1, WHITE)
            win.blit(time_text,(WIDTH// 2 - time_text.get_width()//2, HEIGHT//2 - time_text.get_height()-30))
            win.blit(high_text,(WIDTH// 2 - high_text.get_width()//2, HEIGHT//2 - 20))
        win.blit(PLAY_AGAIN, (0, HEIGHT - 10 - PLAY_AGAIN.get_height()))
        pygame.display.update()

# Function which is going to return the velocity in y factor.
def get_y_velocity(ball, paddle):
    paddle_middle = paddle.y + Paddle.height/2
    diff = paddle_middle - ball.y
    reduction_factor = (Paddle.height/2)/Ball.MAX_VEL
    y_vel = diff/reduction_factor
    return -y_vel


# Function for handling all type of collisions
def handle_collision(Left_paddle, Right_paddle, ball):
    if ball.y + Ball.radius + 1 >= HEIGHT or ball.y - Ball.radius - 1 <= 0:
        ball.y_vel*= -1
        HIT.play()

    if ball.x_vel < 0:
        if (ball.y >= Left_paddle.y and ball.y <= Left_paddle.y + Left_paddle.height
            and ball.x  - Ball.radius <= Left_paddle.x + Left_paddle.width): 
            ball.x_vel*= -1
            ball.y_vel = get_y_velocity(ball, Left_paddle)
            HIT.play()
    else:
        if (ball.y >= Right_paddle.y and ball.y <= Right_paddle.y + Right_paddle.height and ball.x + Ball.radius >= Right_paddle.x):
            ball.x_vel*= -1
            ball.y_vel = get_y_velocity(ball, Right_paddle)
            HIT.play()


# Function for handling the movement of the paddles.
def handle_movement(Left_paddle, Right_paddle,right_output, keys):
    if keys[pygame.K_w] and Left_paddle.y - Left_paddle.VELOCITY >= 2:
        Left_paddle.move(up=True)
    
    if keys[pygame.K_s] and Left_paddle.y + Left_paddle.height + Left_paddle.VELOCITY <= HEIGHT - 2:
        Left_paddle.move(up=False)

    if right_output != None:
        if right_output == 0:
            Right_paddle.move(up = False)
        elif right_output == 2 and Right_paddle.y - Right_paddle.VELOCITY >= 0:
            Right_paddle.move(up = True)
    else:
        if keys[pygame.K_UP] and Right_paddle.y - Right_paddle.VELOCITY >= 2:
            Right_paddle.move(up=True)
        
        if keys[pygame.K_DOWN] and Right_paddle.y + Right_paddle.height + Right_paddle.VELOCITY <= HEIGHT - 2:
            Right_paddle.move(up=False)
    

# Function for drawing different things on the screen.
def draw(win, paddles, ball, left_score=None, right_score=None, time=None, high=None):

    # filling screen with the black screen.
    win.fill(BLACK)
    if left_score != None and right_score != None:
        left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
        right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
        win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
        win.blit(right_score_text, ((WIDTH - WIDTH//4) - right_score_text.get_width()//2, 20))

    # Drawing the paddle on the screen 
    for paddle in paddles:
        paddle.draw(WINDOW)

    # drawing the mid line:
    for i in range(10,HEIGHT,HEIGHT//20):
        if i%2==1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 10, i, 10, HEIGHT//20))
    
    # drawing the ball.
    ball.draw(win)
    
    if time != None:
        time_text = TIME_FONT.render(f'Time: {get_time(time)}', 1, WHITE)
        high_text = TIME_FONT.render(f'Max survival Time: {get_time(high)}', 1, WHITE)
        win.blit(time_text,(33, 20))
        win.blit(high_text,(33,HEIGHT - 30))
        

    # Updating the window after drawing.
    pygame.display.update()

def get_time(seconds):
    sec = seconds % 60
    mint = (seconds//60)%60
    hour = seconds // 3600
    time = f'{hour:02}:{mint:02}:{sec:02}'
    return time

# Main function of the program.
def main(genemo = None, config = None):
    if genemo:
        net = neat.nn.FeedForwardNetwork.create(genemo,config)
    run = True
    # clock for setting FPS.
    clock = pygame.time.Clock()
    # creating the paddles.
    Left_paddle = Paddle(10, HEIGHT//2 - Paddle.height//2)
    Right_paddle = Paddle(WIDTH - Paddle.width - 10, HEIGHT//2 - Paddle.height//2)
    # Creating ball.
    ball = Ball(WIDTH//2, HEIGHT//2)

    # variable for storing the score.
    left_score = 0
    right_score = 0
    while run:
        # Iterating through all the events happing on the screen.
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        # for drawing all the elements on the screen
        draw(WINDOW, [Left_paddle,Right_paddle], ball, left_score, right_score)
        # for movement of the paddles.
        if genemo:
            right_output = net.activate((Right_paddle.y,ball.y, abs(Right_paddle.x  - ball.x)))
            right = right_output.index(max(right_output))
        else: 
            right = None 
        handle_movement(Left_paddle, Right_paddle,right, pygame.key.get_pressed())
        ball.move()

        # handling the collision by using handling collision Function.
        handle_collision(Left_paddle, Right_paddle, ball)

        # Handling the score increment.
        if ball.x - Ball.radius < 0:
            right_score+= 1
            POINT.play()
            ball.reset()
        elif ball.x + Ball.radius > WIDTH:
            left_score+= 1
            POINT.play()
            ball.reset()
        
        # if any player reaches the winning score make won = true and intialize winning text.
        if right_score >= WINNING_SCORE:
            return RIGHT_WIN
        elif left_score >= WINNING_SCORE:
            return LEFT_WIN


def survival_main(genemo, config, high):
    net = neat.nn.FeedForwardNetwork.create(genemo,config)
    run = True
    # clock for setting FPS.
    clock = pygame.time.Clock()
    # creating the paddles.
    Left_paddle = Paddle(10, HEIGHT//2 - Paddle.height//2)
    Right_paddle = Paddle(WIDTH - Paddle.width - 10, HEIGHT//2 - Paddle.height//2)
    # Creating ball.
    ball = Ball(WIDTH//2, HEIGHT//2)
    start = time.time()
    while run:
        # Iterating through all the events happing on the screen.
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        # for drawing all the elements on the screen
        dur = int(time.time() - start)
        if dur > high:
            high = dur 
        draw(WINDOW, [Left_paddle,Right_paddle], ball,time = dur,high = high)
        
        
        right_output = net.activate((Right_paddle.y,ball.y, abs(Right_paddle.x  - ball.x)))
        right = right_output.index(max(right_output))
        handle_movement(Left_paddle, Right_paddle,right, pygame.key.get_pressed())
        
        ball.move()
        # handling the collision by using handling collision Function.
        handle_collision(Left_paddle, Right_paddle, ball)
        # Handling the score increment.
        if ball.x - Ball.radius < 0:
            POINT.play()
            return (high,dur)
        elif ball.x + Ball.radius > WIDTH:
            POINT.play()
            return high


if __name__ == '__main__':
    local_path = os.path.dirname(__file__)
    config_path = os.path.join(local_path, "config.txt")
    config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    file = open('BEST-PADDLE.bin','rb')
    paddle = pickle.load(file)
    while True:
        choice = pre_window(WINDOW)
        if choice == 2:
            middle_window(WINDOW,MIDDLE_WINDOW_IMAGE_2)
            win_img = main(paddle,config)
            score = None
        if choice == 1:
            middle_window(WINDOW,MIDDLE_WINDOW_IMAGE_1)
            win_img = main(None, None)
            score = None
        if choice == 3:
            high = 0
            with open('highscore.txt', 'r') as f:
                high = f.read()
            middle_window(WINDOW,MIDDLE_WINDOW_IMAGE_2)
            score = survival_main(paddle, config, int(high))
            with open('highscore.txt', 'w') as f:
                f.write(str(score[0]))
            win_img = None
            print(score)
        winning_window(WINDOW, win_img, score)