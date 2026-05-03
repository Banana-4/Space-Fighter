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
        self._alive = self._alive_time < self._max_time

    def draw(self, surface):
        if self._alive:
            pygame.draw.rect(surface,self._color, self._rect)
            
    def destroyed(self):
        self._alive = False

    @property 
    def alive(self):
        return self._alive

class SpaceShip:
    def __init__(self, img, scale, pos, flip = False):
        self._spriteSize = scale
        self._pos = pygame.Vector2(pos[0], pos[1])
        self._align_pos()
        self._hitbox = pygame.Rect(self._pos[0], self._pos[1], 40, scale[1])
        self._velocity = 300
        self._speed = pygame.Vector2(0,0)
        self._moving = False
        self._bullets = []
        self._firing_cooldown = 1
        self._firing_time = 0
        path = os.path.join("assets", img)
        self._sprite = pygame.image.load(path)
        if not self._sprite:
            raise FileNotFoundError(f"Image not found: {path}")
        self._sprite = pygame.transform.scale(self._sprite, self._spriteSize)
        if flip:
            self._sprite = pygame.transform.flip(self._sprite, False, flip)
    
    def _align_pos(self):
        self._pos[0] -= self._spriteSize[0] / 2
        self._pos[1] -= self._spriteSize[1] / 2 if self._pos[1] != 0 else  self._pos[1]  + self._spriteSize[1] / 2
    

    def draw(self, surface):
        # use the center as the origin not the left top corner of the image
        surface.blit(self._sprite, (self._pos[0], self._pos[1]))
        #pygame.draw.rect(surface,"#00ff00", self._hitbox)
        for b in self._bullets:
            b.draw(surface)

    def update(self, bound, dt):
        x = self._pos[0] + self._speed[0] * dt
        if (x + self._spriteSize[0] / 2 - self._hitbox.width / 2)  >= 0 and (x + self._hitbox.width / 2 + self._spriteSize[0] / 2) <= bound: 
            self._pos[0] = x 
            self._hitbox.x = x + self._hitbox.width / 2 + self._spriteSize[0] / 2
        for b in self._bullets:
            b.update(dt)
        self._bullets = [b for b in self._bullets if b.alive]
        self._firing_time -= dt
            
    def move_left(self):
        self._speed[0] = self._velocity * -1
      

    def move_right(self):
        self._speed[0] = self._velocity
    
    def shoot(self, top):
        if self._firing_time <= 0:
            bullet = Bullet((self._pos[0] - 5, self._pos[1]), top)
            self._bullets.append(bullet)
            self._firing_time = self._firing_cooldown
           
    def move_stop(self):
        self._speed[0] = 0




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
           
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self._player1.move_left()
        elif keys[pygame.K_d]:
            self._player1.move_right()
        else:
            self._player1.move_stop()

        if keys[pygame.K_LCTRL]:
            self._player1.shoot(True)

        if keys[pygame.K_LEFT]:
            self._player2.move_left()
        elif keys[pygame.K_RIGHT]:
            self._player2.move_right()
        else:
            self._player2.move_stop()

        if keys[pygame.K_RCTRL]:
            self._player2.shoot(False)

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