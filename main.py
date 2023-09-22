from pygame import *

level1 = [
    "r                                                                    .",
    "r                                                                    .",
    "r                                                                    .",
    "r                                                                    .",
    "rr    °  °      l                             r    °  °  °     l     .",
    "r  ------------                                ---------------       .",
    "rr / l                                       r / l         r / l     .",
    "rr   l                                       r   l         r   l     .",
    "rr     °  l                       r     °  °     l   r         l     .",
    "r  ------                           ------------       -------       .",
    "r     r / l                                          r / l           .",
    "r     r   l                                          r   l           .",
    "r     r       °  °   l                       r   °  °    l           .",
    "r       ------------                           ---------             .",
    "r                r / l                       r / l                   .",
    "r                r   l                       r   l                   .",
    "r                                                                    .",
    "----------------------------------------------------------------------"]
level1_width = len(level1[0]) * 40
level1_height = len(level1) * 40


W, H = 1280, 720


window = display.set_mode((W, H))
display.set_icon(image.load("images/mana.png"))
display.set_caption("BLOCKADA")

bg = transform.scale(image.load('new_images/bgr.jpg'), (W, H))







"""ЗВУКИ"""
mixer.init()
fire = mixer.Sound('sounds/fire.ogg')
kick = mixer.Sound('sounds/kick.ogg')
k_coll = mixer.Sound('sounds/k_coll.wav')
c_coll = mixer.Sound('sounds/c_coll.wav')
lock = mixer.Sound('sounds/lock.wav')
tp = mixer.Sound('sounds/teleport.ogg')
click = mixer.Sound('sounds/click.wav')
chest_snd = mixer.Sound('sounds/chest.wav')

"""ШРИФТИ І ТЕКСТ"""
font.init()
font1 = font.SysFont(('font/ariblk.ttf'), 200)
gname = font1.render("Blockada", True, (106, 90, 205), (250, 235, 215))

font2 = font.SysFont(('font/ariblk.ttf'), 60)
e_tap = font2.render('press (e)', True, (255, 0, 255))
k_need = font2.render('You need a key to open!', True, (255, 0, 255))
space = font2.render('press (space) to kill the enemy', True, (255, 0, 255))

font3 = font.SysFont(('font/calibrib.ttf'), 45)
wasd_b = font3.render('WASD - move buttons. You can only go up and down the stairs', True,
                      (255, 0, 0))
space_b = font3.render('Space - shoot button. You are a wizard who only knows one spell', True,
                       (255, 0, 0))
e_b = font3.render('E - interaction button. Open doors, collect keys, activate portals', True,
                   (255, 0, 0))

font4 = font.SysFont(('font/ariblk.ttf'), 150)
done = font4.render('LEVEL DONE!', True, (0, 255, 0), (255, 100, 0))
lose = font4.render('YOU LOSE!', True, (255, 0, 0), (245, 222, 179))
pausa = font4.render('PAUSE', True, (255, 0, 0), (245, 222, 179))

"""КАРТИНКИ СПРАЙТІВ"""
hero_l = "images/sprite1.png"
hero_r = "images/sprite1_r.png"



enemy_r = "new_images/grib_r.png"
enemy_l = "new_images/grib_l.png"

coin_img = "new_images/coin.png"
door_img = "images/door.png"
key_img = "images/key.png"
chest_open = "images/cst_open.png"
chest_close = "images/cst_close.png"
stairs = "images/stair.png"
portal_img = "images/portal.png"
platform = "new_images/platform.png"
power = "images/mana.png"
nothing = "images/nothing.png"
boss = "images/nothing.png"
boss_l = "images/boss_l.png"
boss_r = "images/boss_r.png"

# клас для кнопок в меню
class Button:
    def __init__(self, color, x, y, w, h, text, text_size, text_color):
        self.width = w
        self.height = h
        self.color = color

        self.image = Surface([self.width, self.height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.text_image = font.Font('font/impact.ttf', text_size).render(text, True, text_color)

    def draw(self, shift_x, shift_y):
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.text_image, (self.rect.x + shift_x, self.rect.y + shift_y))

# створення кнопок меню
btn_start = Button((178, 34, 34), 470, 300, 280, 70, 'START GAME', 50, (255, 255, 255))
btn_control = Button((178, 34, 34), 470, 450, 280, 70, 'HOW TO PLAY', 50, (255, 255, 255))
btn_exit = Button((178, 34, 34), 470, 600, 280, 70, 'EXIT GAME', 50, (255, 255, 255))
btn_menu = Button((178, 34, 34), 470, 600, 280, 70, 'BACK to MENU', 50, (255, 255, 255))
btn_restart = Button((178, 34, 34), 470, 450, 280, 70, 'RESTART', 50, (255, 255, 255))
btn_continue = Button((178, 34, 34), 470, 350, 280, 70, 'CONTINUE', 50, (255, 255, 255))
btn_pause = Button((178, 34, 34), 1200, 15, 50, 50, 'I I', 40, (255, 255, 255))
btn_level2 = Button((178, 34, 34), 470, 525, 280, 70, 'LEVEL2', 50, (255, 255, 255))


# клас для камери
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

# налаштування камери
def camera_config(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + W / 2, -t + H / 2

    l = min(0, l)  # Не виходимо за ліву межу
    l = max(-(camera.width - W), l)  # Не виходимо за праву межу
    t = max(-(camera.height - H), t)  # Не виходимо за нижню межу
    t = min(0, t)  # Не виходимо за верхню межу

    return Rect(l, t, w, h)
 

camera = Camera(camera_config, level1_width, level1_height)


class Settings(sprite.Sprite):
    def __init__(self, x, y, w, h, speed, img):
        super().__init__()

        self.speed = speed
        self.width = w
        self.height = h 
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Settings):
    def update_rl(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed

    def update_ud(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed


def start_pos():
    global hero, items, platforms, stairs_lst, coins_lst, blocks_r, blocks_l
    hero = Player(300, 650, 50, 50, 5, hero_r)
    global items
    items = sprite.Group()
    platforms = []
    stairs_lst = []
    coins_lst = []
    blocks_r = []
    blocks_l = []

    x, y = 0, 0
    for r in level1:
        for c in r:
            if c == "-":
                r1 = Settings(x, y, 40, 40, 0, platform)
                platforms.append(r1)
                items.add(r1)
            if c == "/":
                r2 = Settings(x, y-40, 40, 180, 0, stairs)
                stairs_lst.append(r2)
                items.add(r2)
            if c == "°":
                r3 = Settings(x, y, 40, 40, 0, coin_img)
                coins_lst.append(r3)
                items.add(r3)
            if c == "r":
                r4 = Settings(x, y, 40, 40, 0, nothing)
                blocks_r.append(r4)
                items.add(r4)
            if c == "l":
                r5 = Settings(x, y, 40, 40, 0, nothing)
                blocks_l.append(r5)
                items.add(r5)
            x += 40
        x = 0
        y += 40
    items.add(hero)
        
def collides():
    for stair in stairs_lst:
        if sprite.collide_rect(hero, stair):
            hero.update_ud()
            if hero.rect.y <= (stair.rect.y - 40):
                hero.rect.y = stair.rect.y - 40 
            if hero.rect.y >= (stair.rect.y + 120):
                hero.rect.y = stair.rect.y + 120
    for r in blocks_r:
        if sprite.collide_rect(hero, r):
            hero.rect.x = r.rect.x + hero.width*1.5
    for l in blocks_l:
        if sprite.collide_rect(hero, l):
            hero.rect.x = l.rect.x - hero.width*1.5
    






points = 0

start_pos()
game = True
while game:
    time.delay(10)
    window.blit(bg, (0, 0))
    hero.update_rl()
    camera.update(hero)
    for i in items:
        window.blit(i.image, camera.apply(i))


    for e in event.get():
        if e.type == QUIT: 
            game = False
    window.blit(transform.scale(image.load(coin_img), (30, 30)), (10, 10))
    coin_txt = font2.render(":" + str(points), 1, (255, 255, 255))
    window.blit(coin_txt, (40, 5))
    collides()
    display.update()
