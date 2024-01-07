import pygame
import sys
import random
import time


# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyPong")

# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255,0)
blue = (0, 0, 255)
black = (0, 0, 0)
clr = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

# Set up player
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size
player_speed = 5

# Set up balls
balls = []

# Set up score
score = 0
font = pygame.font.Font(None, 36)

# Load background image
background_image = pygame.image.load("background-0.jpg")  # Replace "background.jpg" with your image file
if background_image.get_width()/800 > background_image.get_height()/600:
    background_image = pygame.transform.scale(background_image, (width, width*background_image.get_height()/background_image.get_width()))
else :
    background_image = pygame.transform.scale(background_image, (height*background_image.get_width()/background_image.get_height(), height))


class Ball:
    def __init__(self):
        self.size = random.randint(5,50)
        self.x = random.randint(0, width - self.size)
        self.y = random.randint(-height, -self.size)  # Start above the screen
        self.speed = random.uniform(1, 3)

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, clr, (int(self.x + self.size // 2), int(self.y + self.size // 2)), self.size // 2)

def is_collision(player_x, player_y, player_size, ball_x, ball_y, ball_size):
    return player_x - ball_size < ball_x < player_x + player_size + ball_size and player_y - ball_size < ball_y < player_y + player_size + ball_size

clock = pygame.time.Clock()
game_over = False
start = False

while not start:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        start = True
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (width // 2 - 50, player_y + player_size + 10))

    # Update display
    pygame.draw.rect(screen, red, (player_x, player_y, player_size, player_size))

    pygame.display.flip()

    # Set frames per second
    pygame.time.Clock().tick(60)
    

# Main game loop
while True:
    screen.fill(white)
    screen.blit(background_image, ((width-background_image.get_width())/2, (height - background_image.get_height())/2))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed
    if keys[pygame.K_BACKSPACE] :
        pygame.quit()
        sys.exit()
    
    if game_over :
        if keys[pygame.K_r]:
            game_over = False
            balls = []
            score = 0
        else :
            continue

    # Move and draw balls
    for ball in balls:
        ball.move()
        ball.draw()
        if is_collision(player_x, player_y, player_size, ball.x, ball.y, ball.size):
            game_over = True
            # Game over message
            game_over_text = font.render("Game Over! Your Score: " + str(score), True, black)
            screen.blit(game_over_text, (width // 2 - 150, height // 2 - 18))

            replay_text = font.render(f"Press R to replay | Press BackSpace to exit", True, black)
            screen .blit(replay_text,(width//2 - 250, height // 2 + 10))
            pygame.display.flip()

    # Generate a new ball with a probability
    if random.random() < 0.02:
        balls.append(Ball())

    # Remove balls that have gone below the screen
    balls = [ball for ball in balls if ball.y < height]

    # Update score
    score += 1

    # Draw score
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (width // 2 - 50, player_y + player_size + 10))


    # Update display
    pygame.draw.rect(screen, red, (player_x, player_y, player_size, player_size))

    pygame.display.flip()

    # Set frames per second
    pygame.time.Clock().tick(60)


# Wait for a few seconds before quitting
pygame.time.wait(3000)
pygame.quit()
sys.exit()