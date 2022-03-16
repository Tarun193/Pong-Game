import pygame

# initializing the pygame.
pygame.init()

# variable for height and width of screen
WIDTH, HEIGHT = 700, 500

# setting font for the score. 
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

# Creating Window and setting caption for it.
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong game")

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
        self.x_vel = self.MAX_VEL
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
    start = SCORE_FONT.render("Welcome To Pong!!!", 1, WHITE)
    command = pygame.font.SysFont("comicsans", 20).render("Press Enter To start game!", 1, WHITE)
    win.blit(start, (WIDTH//2 - start.get_width()//2, 
    HEIGHT//4 - start.get_height()))
    win.blit(command, (WIDTH//2 - command.get_width()//2, 
    HEIGHT//2 - command.get_height()))
    pygame.display.update()

# Function for displaying wining window.
def winning_window(win, win_text):
    win.fill(BLACK)
    text = SCORE_FONT.render(win_text, 1, WHITE)
    win.blit(text, (WIDTH//2 - text.get_width()//2, 
                HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

# Function which is going to return the velocity in y factor.
def get_y_velocity(ball, paddle):
    paddle_middle = paddle.y + Paddle.height/2
    diff = paddle_middle - ball.y
    reduction_factor = (Paddle.height/2)/Ball.MAX_VEL
    y_vel = diff/reduction_factor
    return -y_vel


# Function for handling all type of collisions
def handle_collision(Left_paddle, Right_paddle, ball):
    if ball.y + Ball.radius >= HEIGHT or ball.y - Ball.radius <= 0:
        ball.y_vel*= -1
    
    if ball.x_vel < 0:
        if (ball.y >= Left_paddle.y and ball.y <= Left_paddle.y + Left_paddle.height
            and ball.x  - Ball.radius <= Left_paddle.x + Left_paddle.width): 
            ball.x_vel*= -1
            ball.y_vel = get_y_velocity(ball, Left_paddle)
    else:
        if (ball.y >= Right_paddle.y and ball.y <= Right_paddle.y + Right_paddle.height and ball.x + Ball.radius >= Right_paddle.x):
            ball.x_vel*= -1
            ball.y_vel = get_y_velocity(ball, Right_paddle)


# Function for handling the movement of the paddles.
def handle_movement(Left_paddle, Right_paddle, keys):
    if keys[pygame.K_w] and Left_paddle.y - Left_paddle.VELOCITY >= 2:
        Left_paddle.move(up=True)
    
    if keys[pygame.K_s] and Left_paddle.y + Left_paddle.height + Left_paddle.VELOCITY <= HEIGHT - 2:
        Left_paddle.move(up=False)
    
    if keys[pygame.K_UP] and Right_paddle.y - Right_paddle.VELOCITY >= 2:
        Right_paddle.move(up=True)
    
    if keys[pygame.K_DOWN] and Right_paddle.y + Right_paddle.height + Right_paddle.VELOCITY <= HEIGHT - 2:
        Right_paddle.move(up=False)
    

# Function for drawing different things on the screen.
def draw(win, paddles, ball, left_score, right_score):

    # filling screen with the black screen.
    win.fill(BLACK)

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
    
    # Updating the window after drawing.
    pygame.display.update()



# Main function of the program.
def main():
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

    intial = True
    while run:
        # Iterating through all the events happing on the screen.
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intial = False
        if intial:
            pre_window(WINDOW)
        else:
            # for drawing all the elements on the screen
            draw(WINDOW, [Left_paddle,Right_paddle], ball, left_score, right_score)

            # for movement of the paddles.
            handle_movement(Left_paddle, Right_paddle, pygame.key.get_pressed())
            
            ball.move() #moving the ball.

            # handling the collision by using handling collision Function.
            handle_collision(Left_paddle, Right_paddle, ball)

            # Handling the score increment.
            if ball.x - Ball.radius<= 0:
                right_score+= 1
                ball.reset()
            elif ball.x + Ball.radius >= WIDTH:
                left_score+= 1
                ball.reset()
            
            won = False
            # if any player reaches the winning score make won = true and intialize winning text.
            if right_score >= WINNING_SCORE:
                won = True
                win_text = "Right Player Won !!!"
            elif left_score >= WINNING_SCORE:
                won = True
                win_text = "Left Player Won !!!"
            
            # After winning code.
            if won:
                winning_window(WINDOW, win_text)
                ball.reset()
                Left_paddle.reset()
                Right_paddle.reset()
                left_score = 0
                right_score = 0
                intial = True
    pygame.quit()


if __name__ == '__main__':
    main()