import pygame
import math
import sys
import os

pygame.init()
pygame.mixer.init()
bg_color = [255, 255, 255]
images_path = str(os.path.abspath('path.txt')).replace('\path.txt', '')
sc = pygame.display.set_mode((1440, 810))
sc_rect = sc.get_rect()
clock = pygame.time.Clock()
images_list = list()
particles_list = list()
pickaxes = list()
hit_s = pygame.mixer.Sound('hit_s.ogg')
kassa_s = pygame.mixer.Sound('kassa_s.ogg')
default = (1, 0, 0, 0, 1)
streak = 0
power = 1
level = 0
score = 0
money = 0
passive = 1
koeff = 1
k_1 = 0

def streak_f():
    global koeff, streak, bg_color, k_1
    koeff = 1 + int(streak) * 0.1
    if koeff != 1:
        k_1 = 255 / 8.5 * (koeff - 1)
    if k_1 < 255:
        bg_color = [255, 255 - k_1, 255 - k_1]
    else: bg_color = [255, 0, 0]
    if streak > 0.23:
        streak -= 0.225


def saved_data():
    global power, level, score, money, passive
    with open('saves.txt', 'r') as saves:
        save = tuple(saves.read().replace('(', '').replace(')', '').replace(',', '').split())
        power = int(save[0])
        level = int(save[1])
        score = int(save[2])
        money = float(save[3])
        passive = int(save[4])

def music_bg():
    music = pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.play(-1)

def images_dict_1():
    global images_list
    c = 0
    for roots, dirs, files in os.walk(images_path):
        for file in files:
            if 'dll' not in file:
                if 'lvl' and 'ore' in file:
                    print(file)
                    load_file = pygame.image.load(file)
                    images_list.append([load_file, 400])
                elif 'lvl' and 'part' in file:
                    load_file_1 = pygame.transform.scale(pygame.image.load(file), (100, 100))
                    images_list[c].append(load_file_1)
                    c += 1
                elif 'pickaxe' in file:
                    pickaxes.append(pygame.transform.scale(pygame.image.load(file), (200, 200)))

def events():
    global score, particles_list, power, money, passive, koeff, streak, level
    mouse_pos = pygame.mouse.get_pos()
    m_x = mouse_pos[0]
    m_y = mouse_pos[1]
    size_2 = images_list[cl.v_level][1]/2
    rect_top = sc_rect.centery - size_2
    rect_bottom = sc_rect.centery + size_2
    rect_left = sc_rect.centerx - size_2
    rect_right = sc_rect.centerx + size_2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('saves.txt', 'w') as saves:
                saves.write(f'{power, level, score, money, passive}')
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if m_y <= rect_bottom and m_y >= rect_top and m_x >= rect_left and m_x <= rect_right:
                                                                                                    # UDAR KIRKOY
                pygame.mixer.Sound.play(hit_s).set_volume(0.3)
                streak += 1
                particles_list.append([images_list[cl.v_level][2], m_x - 55, m_y - 55])
                score += int(power*2.5*koeff)
                money += int(power * math.pi/2 * koeff)
                if images_list[cl.v_level][1] < 480:
                    if power < 45:
                        images_list[cl.v_level][1] += power
                    else: images_list[cl.v_level][1] += 45
                                                                                                    # KUPIT KIRKU
            if cl.detection(1150, sc_rect.centery - 100, 200) and money >= power ** math.pi/1.8:
                pygame.mixer.Sound.play(kassa_s).set_volume(0.3)
                money -= power ** math.pi/1.8
                power += 1
                                                                                                    # KUPIT PASSIVE
            elif cl.detection(1150, cl.sc_rect.centery + 100, 200) and money >= passive ** 1.5:
                pygame.mixer.Sound.play(kassa_s).set_volume(0.3)
                money -= passive ** 1.5
                passive += 1
                                                                                                    # SAVE
            elif cl.detection(200, 650, 100):
                with open('saves.txt', 'w') as saves:
                    saves.write(f'{power, level, score, money, passive}')
                pygame.draw.rect(sc, (20, 20, 20), (200, 650, 100, 100))
                                                                                                    # RESTART
            elif cl.detection(100, 650, 100):
                pygame.draw.rect(sc, (20, 20, 20), (100, 650, 100, 100))
                power = 1
                level = 0
                score = 0
                money = 0
                passive = 1
                power, level, score, money, passive = default

class Clicker():
    def __init__(self, sc, images_list, level, power, score, particles_list, pickaxes):
        self.sc = sc
        self.sc_rect = sc.get_rect()
        self.images_list = images_list
        self.level = level
        self.power = power
        self.score_font_size = 100
        self.score = score
        self.particles_list = particles_list
        self.v_level = level
        self.pickaxes = pickaxes

    def lvlvlvlv(self):
        if level <= 22:
            self.v_level = level
        else:
            self.v_level = level % (len(images_list) - 1)

    def level_rapids(self):
        return int(1000 * ((level + 1) ** math.pi * 2.7))

    def draw(self):
        size = self.images_list[self.v_level][1]
        f_image = pygame.transform.scale(images_list[self.v_level][0], (size, size))
        self.sc.blit(f_image, (self.sc_rect.centerx - size/2, self.sc_rect.centery - size/2))
        if size > 300:
            if power < 100:
                images_list[self.v_level][1] -= power/10
            else: images_list[self.v_level][1] -= 13

    def shop(self):
        mouse_pos = pygame.mouse.get_pos()
        m_x = mouse_pos[0]
        m_y = mouse_pos[1]
        if power <= 1920:
            image = pickaxes[power//320]
        else: image = pickaxes[5]
        image_rect = image.get_rect()
        if self.detection(1150, self.sc_rect.centery - image_rect.centery, 200):
            pygame.draw.rect(self.sc, (220, 220, 220), (1150, self.sc_rect.centery - image_rect.centery, 200, 200))
        self.sc.blit(image, (1150, self.sc_rect.centery - image_rect.centery))
        if self.detection(1150, self.sc_rect.centery - image_rect.centery, 200):
            self.text_banner('УЛУЧШИТЬ КИРКУ', m_x, m_y - 15, 15, (200, 75, 90))
        elif self.detection(1150, self.sc_rect.centery + 100, 200):
            pygame.draw.rect(self.sc, (220, 220, 220), (1150, self.sc_rect.centery - image_rect.centery + 200, 200, 200))


    def text_banner(self, text, x, y, score_font_size, color):
        score_font = pygame.font.SysFont('bahnschrift', score_font_size)
        text = score_font.render(text, True, color, None)
        text_rect = text.get_rect()
        self.sc.blit(text, (x - text_rect.centerx, y))

    def particles(self):
        c = 0
        for image, x, y in particles_list:
            particles_list[c][2] += 12
            sc.blit(image, (x, y))
            if y > 850:
                del particles_list[c]
            c += 1

    def levels(self):
        global level
        if score >= self.level_rapids():
            level += 1


    def detection(self, x, y, size):
        mouse_pos = pygame.mouse.get_pos()
        m_x = mouse_pos[0]
        m_y = mouse_pos[1]
        rect_top = y
        rect_bottom = y + size
        rect_left = x
        rect_right = x + size
        if m_y <= rect_bottom and m_y >= rect_top and m_x >= rect_left and m_x <= rect_right:
            return True
        else: return False


def banners():
    cl.text_banner(f'УРОВЕНЬ КИРКИ: {power}', 200, 150, 20, (0, 0, 0))
    cl.text_banner(f'СИЛА КИРКИ: {int(power*2.5*koeff)}', 200, 200, 20, (0, 0, 0))
    cl.text_banner(str(score), sc_rect.centerx, 50, 75, (0, 0, 0))
    cl.text_banner(f'ДО СЛЕДУЮЩЕГО УРОВНЯ: {cl.level_rapids() - score}', 200, 50, 20, (0, 0, 0))
    cl.text_banner(f'УРОВЕНЬ: {level + 1}', 200, 100, 20, (0, 0, 0))
    cl.text_banner(f'ДЕНЬГИ: {int(money)}$', 200, 250, 20, (0, 0, 0))
    cl.text_banner(f'СТОИМОСТЬ: {int(power ** math.pi/1.8)}$', 1250, sc_rect.centery - 150, 20, (0, 0, 0))
    cl.text_banner(f'ПАССИВНЫЙ ДОХОД: {round(passive/100 * 60 * koeff, 1)}$/cек', 200, 300, 20, (0, 0, 0))
    cl.text_banner(f'ДОХОД С УДАРА: {int(power * 2 * koeff)}', 200, 350, 20, (0, 0, 0))
    cl.text_banner(f'УВЕЛИЧИТЬ ПАССИВНЫЙ ДОХОД', 1250, 600, 20, (0, 0, 0))
    cl.text_banner(f'СТОИМОСТЬ: {int(passive ** 1.5)}$', 1250, 620, 20, (0, 0, 0))
    cl.text_banner(f'СЕРИЯ: {int(streak)}', 200, 400, 20, (0, 0, 0))
    cl.text_banner(f'МНОЖИТЕЛЬ СЕРИИ: {round(koeff, 2)}', 200, 450, 20, (0, 0, 0))
    cl.text_banner('СБРОС    СОХРАНЕНИЕ', 210, 700, 20, (0, 0, 0))


def main():
    global money, power, passive
    while True:
        cl.lvlvlvlv()
        events()
        cl.levels()
        sc.fill(bg_color)
        cl.draw()
        cl.particles()
        cl.shop()
        banners()
        pygame.display.set_caption(f'топ игра века от миши туманова')
        clock.tick(59)
        streak_f()
        money += passive/100 * koeff
        pygame.display.flip()


if __name__ == '__main__':
    images_dict_1()
    music_bg()
    saved_data()
    cl = Clicker(sc, images_list, level, power, score, particles_list, pickaxes)
    main()

