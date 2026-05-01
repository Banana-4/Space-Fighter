import pygame
import os

class Bullet:
    def __init__(self, pos, top):
        self._rect = pygame.Rect(pos[0], pos[1], 5, 10)
        self._color = "#ff0000"
        self._alive = True
        self._alive_time = 0
        self._max_time = 60
        if top:
            self._speed = -400
        else:
            self._speed = 400

    def update(self, dt):
        self._rect.y += self._speed * dt
        self._alive_time += dt
        self._alive_time = True if self._alive_time < self._max_time else False

    def draw(self, surface):
        if self._alive:
            pygame.draw.rect(surface,self._color, self._rect)


class SpaceShip:
    def __init__(self, img, scale, pos, flip = False):
        self._spriteSize = scale
        self._pos = pygame.Vector2(pos[0], pos[1])
        self._velocity = 300
        self._speed = pygame.Vector2(0,0)
        self._moving = False
        self._bullets = []
        self._firing_cooldown = 0.5
        self._firing_time = 0
        path = os.path.join("assets", img)
        self._sprite = pygame.image.load(path)
        if not self._sprite:
            raise FileNotFoundError(f"Image not found: {path}")
        self._sprite = pygame.transform.scale(self._sprite, self._spriteSize)
        if flip:
            self._sprite = pygame.transform.flip(self._sprite, False, flip)

    def draw(self, surface):
        # use the center as the origin not the left top corner of the image
        x = self._pos[0] - self._spriteSize[0] / 2
        y = self._pos[1]  - self._spriteSize[1] / 2 if self._pos[1] != 0 else  self._pos[1]  + self._spriteSize[1] / 2
        surface.blit(self._sprite, (x, y))
        for b in self._bullets:
            b.draw(surface)
    def update(self, bound, dt):
        x = self._pos[0] + self._speed[0] * dt
        if x >= self._spriteSize[0] / 4 and x  <= bound - self._spriteSize[0] / 4: 
            self._pos[0] = x 
        for b in self._bullets:
            b.update(dt)
        self._bullets = [b for b in self._bullets if b._alive]
            
    def move_left(self, active):
        if active:
            self._speed[0] = self._velocity * -1
            self._speed[1] = 0
        else:
            self._speed[0] = 0

    def move_right(self, active):
        if active:
            self._speed[0] = self._velocity
            self._speed[1] = 0
        else:
            self._speed[0] = 0
    
    def shoot(self, top, dt):
        if self._firing_time <= 0:
            bullet = Bullet((self._pos[0] - 5, self._pos[1]), top)
            self._bullets.append(bullet)
            self._firing_time = self._firing_cooldown
        else:
            self._firing_time -= dt




class Game:
    def __init__(self) -> None:
        pygame.init()
        self._width, self._height = 640, 480
        self._fps = 60
        self._run = False
        self._spriteSize = (96,64)

        self.WINDOW = pygame.display.set_mode((self._width, self._height))
        self._bound_box = self.WINDOW.get_size()
        self._player1 = SpaceShip("ship1.png", self._spriteSize, (self._width / 2, self._height - self._spriteSize[1] / 2))
        self._player2 = SpaceShip("ship1.png", self._spriteSize, (self._width / 2, self._spriteSize[1] / 2), True)

        pygame.display.set_caption("Space Fight")

    def main(self):
        clock = pygame.Clock()
        self._run = True
        while self._run:
            clock.tick(self._fps)
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._run = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self._player1.move_left(False)
                    if event.key == pygame.K_d:
                        self._player1.move_right(False)
                    if event.key == pygame.K_LEFT:
                        self._player2.move_left(False)
                    if event.key == pygame.K_RIGHT:
                        self._player2.move_right(False)
                            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self._player1.move_left(True)
        if keys[pygame.K_d]:
            self._player1.move_right(True)
        if keys[pygame.K_LCTRL]:
            self._player1.shoot(True, 1/60)
        if keys[pygame.K_LEFT]:
            self._player2.move_left(True)
        if keys[pygame.K_RIGHT]:
            self._player2.move_right(True)

    def update(self):
        self._player1.update(self._bound_box[0], 1/60)
        self._player2.update(self._bound_box[0], 1/60)
        
    def draw(self):
        self.WINDOW.fill("#050400")
        self._player1.draw(self.WINDOW)
        self._player2.draw(self.WINDOW)
        pygame.display.flip()
      
if __name__ == "__main__":
    game = Game()
    game.main()