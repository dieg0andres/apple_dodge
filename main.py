import pygame, random, os

pygame.init()

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = WINDOW_WIDTH // 1.5
PLAYER_VELOCITY = 5
STARTING_SCORE = 10
FPS = 60
NUM_APPLES = 8
MIN_APPLE_V = 5
MAX_APPLE_V = 12

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('apple game')

class Apple(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'apple64.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(WINDOW_WIDTH, WINDOW_WIDTH*2), random.randint(0, WINDOW_HEIGHT - self.rect.height))
        self.velocity = random.randint(5,20)

    def update(self):
        if self.rect.right < 0:
            self.rect.x = random.randint(WINDOW_WIDTH, WINDOW_WIDTH*2)
            self.rect.y = random.randint(0, WINDOW_HEIGHT - self.rect.height)
            self.velocity = random.randint(MIN_APPLE_V, MAX_APPLE_V)
        self.velocity += random.randint(-2, 4) / 10
        self.rect.left -= self.velocity

class Mutant(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'mutant_tree.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH - self.rect.width, WINDOW_HEIGHT // 2)
        self.velocity = 5

    def update(self):
        pass

class Seed(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'seed.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.velocity = 10

    def update(self):
        self.rect.x += self.velocity


class Player(pygame.sprite.Sprite):

    def __init__(self, velocity, score, apple_group, seed_group):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'poop.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width, WINDOW_HEIGHT / 2)
        self.velocity = velocity
        self.score = score
        self.group = apple_group
        self.seed_group = seed_group
        self.hit_by_apple_sound = pygame.mixer.Sound(os.path.join('assets','Apple-hits-poop.mp3'))

    def update(self):
        self.move()
        self.shoot_seed()
        self.check_collisions()

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.velocity

        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.velocity

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity

    def shoot_seed(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.seed_group.add(Seed(self.rect.center[0]+40, self.rect.center[1]+5))


    def check_collisions(self):
        if pygame.sprite.spritecollide(self, self.group, True):
            self.score -= 1
            self.group.add(Apple())
            self.hit_by_apple_sound.play()
            print(self.score)

        if self.score < 0:
            pygame.quit()


apple_group = pygame.sprite.Group()
for i in range(NUM_APPLES):
    apple = Apple()
    apple_group.add(apple)

seed_group = pygame.sprite.Group()

player = Player(PLAYER_VELOCITY, STARTING_SCORE, apple_group, seed_group)
player_group = pygame.sprite.Group()
player_group.add(player)

tree = Mutant()
tree_group = pygame.sprite.Group()
tree_group.add(tree)

background = pygame.image.load(os.path.join('assets', 'background.png'))
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

skibidi_song = pygame.mixer.music.load(os.path.join('assets','SkibidiToilet.mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    screen.blit(background, (0,0))

    apple_group.update()
    player_group.update()
    tree_group.update()
    seed_group.update()

    apple_group.draw(screen)
    player_group.draw(screen)
    tree_group.draw(screen)
    seed_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
