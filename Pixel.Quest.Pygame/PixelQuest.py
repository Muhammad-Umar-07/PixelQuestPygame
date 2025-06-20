import pygame
import random
import time

pygame.init()

# Set up the display
win = pygame.display.set_mode((1300, 700))
pygame.display.set_caption("Exe_Game")

# Load and scale background images for each level
bg1 = pygame.image.load('bgexe2.jpg')
bg1 = pygame.transform.scale(bg1, (1300, 700))  # Background for level 1

bg2 = pygame.image.load('bgexe2.jpg')
bg2 = pygame.transform.scale(bg2, (1300, 700))  # Background for level 2

bg3 = pygame.image.load('bgexe1.jpg')
bg3 = pygame.transform.scale(bg3, (1300, 700))  # Background for level 3

# Set initial background
bg = bg1

# Load and scale character and bullet images
char = pygame.image.load('Standing.png')
char = pygame.transform.scale(char, (40, 60))  # Ensure the character image fits properly

bullet_img = pygame.image.load('laser.png')
bullet_img = pygame.transform.scale(bullet_img, (20, 10))  # Scale bullet image if necessary

# Load animations for character
walkRight = [pygame.transform.scale(pygame.image.load(f'R{i+1}.png'), (40, 60)) for i in range(4)]
walkLeft = [pygame.transform.scale(pygame.image.load(f'L{i+1}.png'), (40, 60)) for i in range(4)]
walkUp = [pygame.transform.scale(pygame.image.load(f'Up{i+1}.png'), (40, 60)) for i in range(4)]
walkDown = [pygame.transform.scale(pygame.image.load(f'Down{i+1}.png'), (40, 60)) for i in range(4)]

# Monster animations
monsterWalkRight = [pygame.transform.scale(pygame.image.load(f'MonsterR{i+1}.png'), (40, 60)) for i in range(4)]
monsterWalkLeft = [pygame.transform.scale(pygame.image.load(f'MonsterL{i+1}.png'), (40, 60)) for i in range(4)]
monsterWalkUp = [pygame.transform.scale(pygame.image.load(f'MonsterUp{i+1}.png'), (40, 60)) for i in range(4)]
monsterWalkDown = [pygame.transform.scale(pygame.image.load(f'MonsterDown{i+1}.png'), (40, 60)) for i in range(4)]

# Load custom font
font_path = 'Library3amsoft-6zgq.otf'
font = pygame.font.Font(font_path, 30)

# Character variables
width, height = 40, 60
x = (1300 - width) // 2
y = (700 - height) // 2
vel = 5
health = 100
max_health = 100

# Bullet variables
bullets = []
bullet_vel = 7
last_shot_time = 0

# Game variables
left = False
right = False
up = False
down = False
walkCount = 0
score = 0

# Level variable
level = 1

# Monster variables
monsters = []
monster_vel = 2
monster_max_health = 50

# Clock initialization
clock = pygame.time.Clock()

# Timer to spawn monsters
monster_spawn_interval = 5
last_monster_spawn_time = time.time()

# Game over flag
game_over = False

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, monster_type):
        super().__init__()
        self.x = x
        self.y = y
        self.health = monster_max_health
        self.type = monster_type
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.images = self.get_images_for_type()
        self.walkCount = 0  # Initialize walkCount for the monster

    def get_images_for_type(self):
        if self.type == 1:
            return monsterWalkRight if self.direction == 'right' else monsterWalkLeft
        elif self.type == 2:
            return monsterWalkUp if self.direction == 'up' else monsterWalkDown
        elif self.type == 3:
            return monsterWalkRight if self.direction == 'right' else monsterWalkLeft
        elif self.type == 4:
            return monsterWalkUp if self.direction == 'up' else monsterWalkDown

    def move_towards(self, target_x, target_y):
        if self.x < target_x:
            self.x += monster_vel
        elif self.x > target_x:
            self.x -= monster_vel

        if self.y < target_y:
            self.y += monster_vel
        elif self.y > target_y:
            self.y -= monster_vel

    def draw(self, win):
        images = self.images
        if self.walkCount + 1 >= len(images) * 3:
            self.walkCount = 0
        win.blit(images[self.walkCount // 3], (self.x, self.y))
        self.walkCount += 1

def redrawGameWindow():
    global walkCount, bg
    win.blit(bg, (0, 0))

    # Draw the player
    if walkCount + 1 >= 12:
        walkCount = 0

    if left:
        win.blit(walkLeft[walkCount // 3], (x, y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount // 3], (x, y))
        walkCount += 1
    elif up:
        win.blit(walkUp[walkCount // 3], (x, y))
        walkCount += 1
    elif down:
        win.blit(walkDown[walkCount // 3], (x, y))
        walkCount += 1
    else:
        win.blit(char, (x, y))
        walkCount = 0

    # Draw bullets
    for bullet in bullets:
        win.blit(bullet_img, (bullet[0], bullet[1]))

    # Draw monsters
    for monster in monsters:
        monster.draw(win)

    # Draw health bar
    pygame.draw.rect(win, (255, 0, 0), (10, 10, max_health, 20))  # Red background for health bar
    pygame.draw.rect(win, (0, 255, 0), (10, 10, health, 20))  # Green foreground for health bar

    # Draw score
    score_text = font.render(f"Score: {score}", True, (0, 0, 255))
    win.blit(score_text, (10, 40))

    # Draw level
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    text_width = level_text.get_width()
    win.blit(level_text, ((1300 - text_width) // 2, 10))

    # Draw game over screen if needed
    if game_over:
        game_over_text = font.render("Game Over! Press 'R' to Restart or 'Q' to Quit", True, (255, 0, 0))
        text_width = game_over_text.get_width()
        win.blit(game_over_text, ((1300 - text_width) // 2, 350))
    
    pygame.display.update()

def handle_bullets():
    global bullets
    new_bullets = []
    for bullet in bullets:
        if bullet[2] == 'right':
            bullet[0] += bullet_vel
        elif bullet[2] == 'left':
            bullet[0] -= bullet_vel
        elif bullet[2] == 'up':
            bullet[1] -= bullet_vel
        elif bullet[2] == 'down':
            bullet[1] += bullet_vel

        if 0 < bullet[0] < 1300 and 0 < bullet[1] < 700:
            new_bullets.append(bullet)
    
    bullets = new_bullets

def handle_monsters():
    global monsters, score, health, game_over
    for monster in monsters:
        if not game_over:
            monster.move_towards(x, y)
            for bullet in bullets:
                if (monster.x < bullet[0] < monster.x + 40 and
                    monster.y < bullet[1] < monster.y + 60):
                    monsters.remove(monster)
                    bullets.remove(bullet)
                    score += 50
                    break

            if (x < monster.x + 40 and x + 40 > monster.x and
                y < monster.y + 60 and y + 60 > monster.y):
                health -= 1
                if health <= 0:
                    health = 0
                    game_over = True

def next_level():
    global level, x, y, bg, monsters, last_monster_spawn_time, monster_vel, monster_spawn_interval
    level += 1
    x = (1300 - width) // 2
    y = (700 - height) // 2
    monsters = []
    last_monster_spawn_time = time.time()

    if level == 2:
        bg = bg2
        monster_vel += 1
        monster_spawn_interval = 3
    elif level == 3:
        bg = bg3
        monster_vel += 2
        monster_spawn_interval = 2

def restart_game_with_reduced_difficulty():
    global health, score, game_over, level, bg, monster_vel, monster_spawn_interval, monsters
    health = max_health
    score = 0
    game_over = False
    level = 1
    bg = bg1
    monster_vel = 2  # Reset difficulty to initial state
    monster_spawn_interval = 5  # Reset spawn interval to initial state
    monsters = []  # Clear current monsters

def spawn_monsters():
    global monsters, last_monster_spawn_time
    current_time = time.time()

    if current_time - last_monster_spawn_time >= monster_spawn_interval:
        monster_type = random.randint(1, 4)
        if monster_type == 1:  # Spawn on left
            new_monster = Monster(0, random.randint(0, 700), 1)
        elif monster_type == 2:  # Spawn on right
            new_monster = Monster(1300, random.randint(0, 700), 2)
        elif monster_type == 3:  # Spawn at top
            new_monster = Monster(random.randint(0, 1300), 0, 3)
        elif monster_type == 4:  # Spawn at bottom
            new_monster = Monster(random.randint(0, 1300), 700, 4)

        monsters.append(new_monster)
        last_monster_spawn_time = current_time

# Main loop
run = True
while run:
    clock.tick(27)

    if game_over:
        redrawGameWindow()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            restart_game_with_reduced_difficulty()
        if keys[pygame.K_q]:
            run = False
        continue

    handle_bullets()
    handle_monsters()
    spawn_monsters()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT]:
            x -= vel
            left, right, up, down = True, False, False, False
        elif keys[pygame.K_RIGHT]:
            x += vel
            left, right, up, down = False, True, False, False
        elif keys[pygame.K_UP]:
            y -= vel
            left, right, up, down = False, False, True, False
        elif keys[pygame.K_DOWN]:
            y += vel
            left, right, up, down = False, False, False, True
        else:
            left, right, up, down = False, False, False, False

        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - last_shot_time > 500:
                if right:
                    bullets.append([x + 40, y + 30, 'right'])
                elif left:
                    bullets.append([x, y + 30, 'left'])
                elif up:
                    bullets.append([x + 20, y, 'up'])
                elif down:
                    bullets.append([x + 20, y + 60, 'down'])
                last_shot_time = now

        if (level == 1 and score >= 300) or (level == 2 and score >= 400) or (level == 3 and score >= 500):
            next_level()

    redrawGameWindow()

pygame.quit()
