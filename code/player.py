import pygame
from importer import import_tiles


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, obstacles):
        super().__init__(group)
        self.type = 'player'
        self.hasWater = False
        # hitbox setup
        self.image = pygame.image.load("../tiles/character/down/1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -50)

        # animations setup
        self.animations = {
            'up': [],
            'up_idle': [],
            'right': [],
            'right_idle': [],
            'down': [],
            'down_idle': [],
            'left': [],
            'left_idle': []
        }
        self.import_player_images()
        self.status = 'down'
        self.frame = 1
        self.frame_speed = 0.2

        # movement setup
        self.dir = pygame.math.Vector2()
        self.vel = 5

        # collision setup
        self.obstacles = obstacles

    def import_player_images(self):
        path = '../tiles/character/'

        for animation_key in self.animations.keys():
            full_path = path + animation_key
            self.animations[animation_key] = import_tiles(full_path)

    def keyboard_input(self):
        keys = pygame.key.get_pressed()

        # y coordinate movement
        if keys[pygame.K_UP]:
            self.dir.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.dir.y = 1
            self.status = 'down'
        else:
            self.dir.y = 0

        # x coordinate movement
        if keys[pygame.K_LEFT]:
            self.dir.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.dir.x = 1
            self.status = 'right'
        else:
            self.dir.x = 0

    def idle_status(self):
        if self.dir.x == 0 and self.dir.y == 0 and 'idle' not in self.status:
            self.status += '_idle'

    def move(self):
        # normalizing direction
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()

        self.hitbox.x += self.dir.x * self.vel
        self.collision('x-coordinate')
        self.hitbox.y += self.dir.y * self.vel
        self.collision('y-coordinate')
        self.rect.center = self.hitbox.center

    def collision(self, collision_type):
        # x coordinate collision
        if collision_type == 'x-coordinate':
            for obstacle in self.obstacles:
                if obstacle.hitbox.colliderect(self.hitbox):
                    if self.dir.x > 0:
                        self.hitbox.right = obstacle.hitbox.left
                    if self.dir.x < 0:
                        self.hitbox.left = obstacle.hitbox.right

        # y coordinate collision
        if collision_type == 'y-coordinate':
            for obstacle in self.obstacles:
                if obstacle.hitbox.colliderect(self.hitbox):
                    if self.dir.y > 0:
                        self.hitbox.bottom = obstacle.hitbox.top
                    if self.dir.y < 0:
                        self.hitbox.top = obstacle.hitbox.bottom

    def animate_player(self):
        animation = self.animations[self.status]

        # frame index change
        self.frame += self.frame_speed
        if self.frame >= len(animation):
            self.frame = 1

        # changing an image
        self.image = animation[str(int(self.frame)) + '.png']
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.keyboard_input()
        self.idle_status()
        self.animate_player()
        self.move()
