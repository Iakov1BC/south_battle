import pygame
import random
import pygame
from sys import exit
from os import path
from math import sin, cos, radians, atan, degrees

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('')
    screen = pygame.display.set_mode((0, 0), flags=pygame.FULLSCREEN)
    window = 1


    def load_image(name, colorkey=None):
        fullname = path.join('data', name)
        if not path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image


    def st_window():
        def click():
            screen.blit(bg, (0, 0))
            rects = []
            for i in range(4):
                but = button1.copy()
                if i % 2 == 1:
                    but = pygame.transform.flip(button1, True, False)
                rect = but.get_rect()
                rect.center = (screen.get_width() // 4 * i + 170, screen.get_height() // 3)
                screen.blit(but, rect)
                rects.append(rect)
            rect = button.get_rect()
            rect.center = (screen.get_width() // 2, screen.get_height() // 3 * 2)
            screen.blit(button, rect)
            rects.append(rect)
            for i in range(2):
                rect = characters_[n_of_char[i]].get_rect()
                rect.center = (screen.get_width() // 8 * [1, 5][i] + 170, screen.get_height() // 3)
                screen.blit(characters_[n_of_char[i]], rect)
            return rects

        bg = load_image('st_window_background.jpg')
        button = load_image('button.png', colorkey=-1)
        rect = button.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(bg, (0, 0))
        screen.blit(button, rect)
        running, play_clicked = True, False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if not play_clicked:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and rect.collidepoint(event.pos[0], event.pos[1]):
                            play_clicked = True
                            screen.blit(bg, (0, 0))
                            button1 = load_image('button1.png', colorkey=-1)
                            characters_ = [load_image('Stan.png'), load_image('keni.png'), load_image('Cartman.png')]
                            for i in range(3):
                                characters_[i] = pygame.transform.rotozoom(characters_[i], 0, [0.4, 0.25, 0.65][i])
                            n_of_char = [0, 1]
                            rects = click()
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if rects[0].collidepoint(event.pos[0], event.pos[1]):
                                n_of_char[0] = (n_of_char[0] + 1) % 3
                                n_of_char[0] = (n_of_char[0] + 1) % 3 if n_of_char[0] == n_of_char[1] else n_of_char[0]
                                rects = click()
                            elif rects[1].collidepoint(event.pos[0], event.pos[1]):
                                n_of_char[0] = (n_of_char[0] - 1) % 3
                                n_of_char[0] = (n_of_char[0] - 1) % 3 if n_of_char[0] == n_of_char[1] else n_of_char[0]
                                rects = click()
                            elif rects[2].collidepoint(event.pos[0], event.pos[1]):
                                n_of_char[1] = (n_of_char[1] + 1) % 3
                                n_of_char[1] = (n_of_char[1] + 1) % 3 if n_of_char[0] == n_of_char[1] else n_of_char[1]
                                rects = click()
                            elif rects[3].collidepoint(event.pos[0], event.pos[1]):
                                n_of_char[1] = (n_of_char[1] - 1) % 3
                                n_of_char[1] = (n_of_char[1] - 1) % 3 if n_of_char[0] == n_of_char[1] else n_of_char[1]
                                rects = click()
                            elif rects[4].collidepoint(event.pos[0], event.pos[1]):
                                with open('players', 'w', encoding='UTF-8', ) as file:
                                    file.write(str(n_of_char)[1:-1].replace(', ', ' '))
                                return 2
            pygame.display.flip()


    def main_window():
        number_of_map = random.choice([0, 1])
        characters = []
        all_sprites = pygame.sprite.Group()
        with open('players', 'r', encoding='UTF-8', ) as file:
            characters_ = list(map(int, file.readline().split(' ')))

        def destr_circle(r):
            destr_circ = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(destr_circ, (1, 1, 1), (r, r), r)
            destr_mask = pygame.mask.from_surface(destr_circ)
            return destr_mask

        bg = [pygame.transform.scale(load_image('background1.png'), screen.get_size()),
              pygame.transform.scale(load_image('background2.png'), screen.get_size())][number_of_map]

        class Map(pygame.sprite.Sprite):
            image = [pygame.transform.scale(load_image('map1.png'), screen.get_size()),
                     pygame.transform.scale(load_image('map2.png', colorkey=-1), screen.get_size())][number_of_map]

            def __init__(self):
                super().__init__(all_sprites)
                self.image = Map.image.copy()
                self.rect = self.image.get_rect()
                self.rect.bottom = screen.get_height()
                self.mask = pygame.mask.from_surface(self.image)

            def destroying(self, x, y, al, r):
                if al <= 90:
                    x, y = x - self.rect.x - r, y - self.rect.y - r
                else:
                    x, y = x - self.rect.x - r, y - self.rect.y - r
                self.mask.erase(destr_circle(r), (x, y))
                self.image = self.mask.to_surface(self.image, setsurface=self.image)
                self.image.set_colorkey((0, 0, 0))
                self.mask = pygame.mask.from_surface(self.image)

        class Character(pygame.sprite.Sprite):
            def __init__(self, pos):
                super().__init__(all_sprites)
                characters.append(self)
                self.im = [(load_image('Stan.png'), 0.13), (load_image('keni.png'), 0.08),
                           (load_image('Cartman.png'), 0.26)]
                self.image = pygame.transform.rotozoom(self.im[characters_[player]][0], 0,
                                                       self.im[characters_[player]][1])
                self.rect = self.image.get_rect()
                self.rect.center = pos
                self.fall_ = True
                self.jump_ = False
                self.spase_pressed = False
                self.side = 1 - player * 2
                self.v = 0
                self.x, self.y = self.rect.topleft
                self.jump_start_time = 0
                self.mask = pygame.mask.from_surface(self.image)
                self.hp = 500
                self.alp = 70
                self.jump_v = 50
                self.jump_after_exp = False

            def fall(self):
                self.y += 400 / fps
                self.rect.y = int(self.y)
                while pygame.sprite.collide_mask(self, map_):
                    self.fall_ = False
                    self.rect.y -= 1
                    self.y -= 1

            def walk(self):
                self.x += self.v / fps
                self.rect.x = int(self.x)
                if 0 <= self.rect.left and self.rect.right <= screen.get_width():
                    if pygame.sprite.collide_mask(self, map_):
                        if (self.v > 0 and map_.mask.get_at((self.rect.right - 7, self.rect.bottom))) or (
                                self.v < 0 and map_.mask.get_at((self.rect.left + 7, self.rect.bottom))):
                            for i in range(0, -6, -1):
                                self.y += i
                                self.rect.y = int(self.y)
                                if not pygame.sprite.collide_mask(self, map_):
                                    return
                                self.y -= i
                                self.rect.y = int(self.y)
                        self.x -= self.v / fps
                        self.rect.x = int(self.x)
                else:
                    self.x -= self.v / fps
                    self.rect.x = int(self.x)

            def jump(self):
                t = (pygame.time.get_ticks() - self.jump_start_time) / 65
                h = (abs(self.jump_v) * sin(radians(self.alp)) * t - 9.81 * t ** 2 / 2) * 100
                l_ = self.jump_v * cos(radians(self.alp)) * t * 100
                x, y = self.rect.topleft
                self.rect.x, self.rect.y = int(self.x + l_ / fps), int(self.y - h / fps)
                if 0 >= self.rect.left or self.rect.right >= screen.get_width() or pygame.sprite.collide_mask(
                        self, map_):
                    if pygame.sprite.collide_mask(self, map_):
                        self.jump_after_exp = False
                    self.jump_ = False
                    self.rect.topleft = (x, y)
                    self.x, self.y = x, y
                    self.alp = 70
                    self.jump_v = 50
                    if 0 > self.rect.left or self.rect.right > screen.get_width():
                        self.fall_ = True

            def damage(self, exp_x, exp_y, v_, max_damage, char_exp=False):
                a = [self.rect.topleft, self.rect.topright, (self.rect.right, self.rect.centery), self.rect.bottomright,
                     self.rect.bottomleft, (self.rect.left, self.rect.centery)]
                r = min([[((i[0] - exp_x) ** 2 + (i[1] - exp_y) ** 2) ** 0.5, i] for i in a], key=lambda x: x[0])
                if char_exp or r[0] <= 1:
                    self.hp -= int((v_ - 60) / 140 * 20 + max_damage)
                    r[0] = 1
                else:
                    self.hp -= max(int((v_ - 60) / 140 * 20 + max_damage - r[0] // 2), 0)
                if r[0] <= 60 and r[1] != self.rect.midtop:
                    if r[1] in [self.rect.topleft, self.rect.topright]:
                        self.alp = 20
                    elif r[1] in [self.rect.midright, self.rect.midleft]:
                        self.alp = 40
                    elif r[1] in [self.rect.bottomright, self.rect.bottomleft]:
                        self.alp = 70
                    elif r[1] in [self.rect.midbottom]:
                        self.alp = 85
                    self.jump_v = 70 * (v_ / 200) / r[0]
                    if self.rect.centerx - exp_x < 0:
                        self.jump_v *= -1
                    self.spase_pressed, self.jump_ = True, True
                    self.jump_after_exp = True
                    self.update()

            def update(self):
                self.rect.y += 1
                if not pygame.sprite.collide_mask(self, map_) and not self.jump_:
                    self.fall_ = True
                self.rect.y -= 1
                if self.fall_:
                    self.fall()
                elif self.v != 0:
                    self.walk()
                elif self.jump_:
                    if self.spase_pressed:
                        self.x, self.y = self.rect.topleft
                        self.jump_start_time = pygame.time.get_ticks()
                        if not self.jump_after_exp:
                            self.jump_v *= self.side
                        self.spase_pressed = False
                    self.jump()

        class Gun(pygame.sprite.Sprite):
            image = load_image('bazooka1.png', colorkey=-1)

            def __init__(self, pos):
                super().__init__(all_sprites)
                self.rev = True if characters[player].side == -1 else False
                self.image = pygame.transform.rotate(Gun.image, alpha[player])
                if self.rev:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.image.get_rect()
                self.rect.center = self.pos = pos
                self.al = alpha[player]

            def update(self):
                self.rect.center = self.pos = characters[player].rect.center
                if self.al != alpha[player] or characters[player].side == -1 and not self.rev or characters[
                        player].side == 1 and self.rev:
                    self.rev = True if characters[player].side == -1 else False
                    self.image = pygame.transform.rotate(Gun.image, alpha[player])
                    if self.rev:
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.rect = self.image.get_rect()
                    self.rect.center, self.al = self.pos, alpha[player]

        class Rocket(pygame.sprite.Sprite):
            image = load_image('rocket.png', colorkey=-1)

            def __init__(self, r, pos, v):
                super().__init__(all_sprites)
                self.image = pygame.transform.rotate(pygame.transform.scale(Rocket.image, (30, 30)),
                                                     -70 + alpha[player])
                self.rect = self.image.get_rect()
                self.im = load_image('explode.png', colorkey=-1)
                self.x0, self.y0 = pos
                self.x, self.y = 0, 0
                self.rect.x, self.rect.y = pos
                self.t = 2 * v * sin(radians(alpha[player])) / 98.1
                self.mid = False
                self.rev = True if characters[player].side == -1 else False
                self.alpha = alpha[player]
                self.exp, self.exp_t = False, 0
                self.exp_x, self.exp_y = pos
                self.start_time = pygame.time.get_ticks()
                self.r = int(r)
                self.v = v
                self.not_in_char = False

            def update(self):
                if -35 < self.rect.x < screen.get_width() + 35 and screen.get_height() + 35 > self.rect.y \
                        and not self.exp:
                    t = (pygame.time.get_ticks() - self.start_time) / 100
                    h = (self.v * sin(radians(self.alpha)) * t - 9.81 * t ** 2 / 2)
                    l_ = self.v * cos(radians(self.alpha)) * t
                    a, b = l_ / fps * 50 - self.x, abs(h / fps * 50 - self.y)
                    deg = abs(degrees(atan(b / a))) if a != 0 else abs(degrees(atan(b / 1)))
                    if self.mid:
                        deg = -deg
                    if t / 10 >= self.t / 2 and not self.mid:
                        self.mid = True
                    if self.rev:
                        deg = - deg + 180
                    if deg == 0.0:
                        deg = self.alpha
                    self.image = pygame.transform.rotate(pygame.transform.scale(Rocket.image, (30, 30)), -70 + deg)
                    self.rect = self.image.get_rect()
                    if not self.rev:
                        self.rect.x, self.rect.y = int(self.x0 + l_ / fps * 50), int(self.y0 - h / fps * 50)
                    else:
                        self.rect.x, self.rect.y = int(self.x0 - l_ / fps * 50), int(self.y0 - h / fps * 50)
                    self.x, self.y = l_ / fps * 50, h / fps * 50
                    if not self.not_in_char and not pygame.sprite.collide_rect(self, characters[player]):
                        self.not_in_char = True
                    if pygame.sprite.collide_mask(self, map_) or \
                            (pygame.sprite.collide_mask(self, characters[
                                player]) and self.not_in_char) or pygame.sprite.collide_mask(self,
                                                                                             characters[
                                                                                                 (player + 1) % 2]):
                        if characters[player].side == 1 and alpha[player] != 90:
                            if deg > 0:
                                self.exp_x, self.exp_y = self.rect.topright[0] - 10, self.rect.topright[1] + 10
                            else:
                                self.exp_x, self.exp_y = self.rect.bottomright[0] - 10, self.rect.bottomright[1] - 10
                        elif alpha[player] == 90:
                            if deg > 0:
                                self.exp_x, self.exp_y = self.rect.x + 20, self.rect.top
                            else:
                                self.exp_x, self.exp_y = self.rect.x + 18, self.rect.bottom
                        else:
                            if deg > 0:
                                self.exp_x, self.exp_y = self.rect.topleft[0] + 10, self.rect.topleft[1] + 10
                            else:
                                self.exp_x, self.exp_y = self.rect.bottomleft[0] + 10, self.rect.bottomleft[1] - 10
                        self.exp_t = pygame.time.get_ticks()
                        self.exp = True
                        map_.destroying(self.exp_x, self.exp_y, alpha[player], self.r)
                        if pygame.sprite.collide_mask(self, characters[0]):
                            characters[0].damage(self.exp_x, self.exp_y, self.v, 100, char_exp=True)
                            characters[1].damage(self.exp_x, self.exp_y, self.v, 100)
                        elif pygame.sprite.collide_mask(self, characters[1]):
                            characters[1].damage(self.exp_x, self.exp_y, self.v, 100, char_exp=True)
                            characters[0].damage(self.exp_x, self.exp_y, self.v, 100)

                        else:
                            [i.damage(self.exp_x, self.exp_y, self.v, 100) for i in characters]
                        pygame.time.set_timer(MYEVENTTYPE2, 10)

                elif self.exp:
                    self.explode()
                else:
                    pygame.time.set_timer(MYEVENTTYPE2, 10)
                    all_sprites.remove(self)

            def explode(self):
                t = (pygame.time.get_ticks() - self.exp_t)
                if t < 300:
                    self.image = pygame.transform.scale(self.im, (int(t), int(t)))
                    self.rect = self.image.get_rect()
                    self.rect.center = (self.exp_x, self.exp_y)
                else:
                    all_sprites.remove(self)

        def screen_update():
            screen.blit(bg, (0, 0))
            if sp_down:
                font = pygame.font.Font(None, 50)
                text = font.render(f"V={int((v - 60) // 1.4)}%", True, (100, 255, 100))
                screen.blit(text, (screen.get_width() - 180, 20))
            text = pygame.font.Font(None, 75).render(f"Player {player + 1}", True,
                                                     (200 * player, 0, abs(player - 1) * 200))
            screen.blit(text, (int(screen.get_width() / 2) - 100, 20))
            if len(characters) == 2:
                for i in range(2):
                    text = pygame.font.Font(None, 40).render(str(characters[i].hp), True,
                                                             (200 * i, 0, abs(i - 1) * 200))
                    rect = text.get_rect()
                    rect.center = (characters[i].rect.centerx, characters[i].rect.top - 30)
                    screen.blit(text, rect)
            all_sprites.draw(screen)
            all_sprites.update()
            cl.tick(fps)
            pygame.display.flip()
            if len(characters) == 2:
                for i in range(2):
                    if characters[i].hp <= 0:
                        with open('players', 'w', encoding='UTF-8') as file:
                            file.write(f'{characters_[(i + 1) % 2]} {(i + 1) % 2}')
                        return True

        running = True
        player = 0
        map_ = Map()
        gun_loaded, k_up, k_down, sp_down, shooted = False, False, False, False, False
        MYEVENTTYPE, MYEVENTTYPE1, MYEVENTTYPE2 = pygame.USEREVENT + 1, pygame.USEREVENT + 2, pygame.USEREVENT + 3
        v, fps, alpha = 50, 144, [0, 0]
        cl = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and len(characters) < 2:
                    if event.button == 1:
                        Character(event.pos)
                        player = (player + 1) % 2
                if len(characters) == 2:
                    if not gun_loaded:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE and not characters[player].jump_ and not characters[
                                    player].fall_ and not characters[player].jump_:
                                characters[player].spase_pressed = True
                                characters[player].jump_ = True
                        if pygame.key.get_pressed()[pygame.K_RIGHT] and not characters[player].fall_ and not characters[
                                player].jump_:
                            characters[player].v = 65
                            characters[player].side = 1
                        if not pygame.key.get_pressed()[pygame.K_RIGHT] and not pygame.key.get_pressed()[pygame.K_LEFT]:
                            characters[player].v = 0
                        if pygame.key.get_pressed()[pygame.K_LEFT] and not characters[player].fall_ and not characters[
                                player].jump_:
                            characters[player].v = -65
                            characters[player].side = -1
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 3:
                                gun = Gun(characters[player].rect.center)
                                gun_loaded = True
                                characters[player].v = 0
                    elif gun_loaded and not shooted:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 3:
                                gun_loaded = False
                                all_sprites.remove(gun)
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                sp_down = True
                                pygame.time.set_timer(MYEVENTTYPE1, 150)
                            if event.key == pygame.K_UP:
                                k_up = True
                                pygame.time.set_timer(MYEVENTTYPE, 100)
                                alpha[player] = alpha[player] if alpha[player] > 86 else alpha[player] + 5
                            if event.key == pygame.K_DOWN:
                                k_down = True
                                pygame.time.set_timer(MYEVENTTYPE, 100)
                                alpha[player] = alpha[player] if alpha[player] < -86 else alpha[player] - 5
                            if event.key == pygame.K_RIGHT:
                                characters[player].side = 1
                            if event.key == pygame.K_LEFT:
                                characters[player].side = -1
                                Gun.rev = True
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_SPACE and sp_down:
                                sp_down = False
                                al = alpha[player] if characters[player].side != -1 else 180 - alpha[player]
                                pygame.time.set_timer(MYEVENTTYPE1, 0)
                                Rocket(35 + 20 * v / 200, (characters[player].rect.center[0] - 20 + 35 * cos(radians(
                                    al)), characters[player].rect.center[1] - 20 - 35 * sin(radians(al))), v)
                                v = 60
                                all_sprites.remove(gun)
                                shooted = True
                            if event.key == pygame.K_UP:
                                k_up = False
                                pygame.time.set_timer(MYEVENTTYPE, 0)
                            if event.key == pygame.K_DOWN:
                                k_down = False
                                pygame.time.set_timer(MYEVENTTYPE, 0)
                    if event.type == MYEVENTTYPE:
                        if k_up:
                            alpha[player] = alpha[player] if alpha[player] > 86 else alpha[player] + 5
                        if k_down:
                            alpha[player] = alpha[player] if alpha[player] < -86 else alpha[player] - 5
                    if event.type == MYEVENTTYPE1:
                        v = v + 20 if v <= 180 else 200
                    if event.type == MYEVENTTYPE2:
                        if not characters[player].jump_ and not characters[(player + 1) % 2].jump_:
                            player = (player + 1) % 2
                            gun_loaded = False
                            shooted = False
                            pygame.time.set_timer(MYEVENTTYPE2, 0)
            if screen_update():
                return 3


    def th_window():
        characters = {'0': 'Stan', '1': 'Kenny', '2': 'Cartman'}
        with open('players', 'r', encoding='UTF-8') as file:
            char = file.readline().split()
        bg = pygame.transform.scale(load_image('th_window_background.jpg'), (screen.get_size()))
        screen.blit(bg, (0, 0))
        text = pygame.font.Font(None, 100).render(f'{characters[char[0]]} wins!', True,
                                                  (220 * int(char[1]), 0, 220 * ((int(char[1]) + 1) % 2)))
        rect = text.get_rect()
        rect.center = (screen.get_width() // 2, screen.get_height() // 20)
        screen.blit(text, rect)
        button = load_image('button3.png', colorkey=-1)
        button.set_alpha(240)
        rect = button.get_rect()
        rect.center = (screen.get_width() // 2, screen.get_height() // 20 * 9)
        screen.blit(button, rect)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and rect.collidepoint(event.pos[0], event.pos[1]):
                        return 1
            pygame.display.flip()


    while window:
        if window == 1:
            window = st_window()
        elif window == 2:
            window = main_window()
        elif window == 3:
            window = th_window()
    pygame.quit()
