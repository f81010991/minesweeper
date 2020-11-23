# coding=utf-8
import random
import pygame
import time
from sys import exit
from pygame.locals import *


class Menu:
    def __init__(self, x, y, w, h, m, word=u'按钮', size=12, width=90):
        myfont = pygame.font.SysFont('simsunnsimsun', size)
        self.text = myfont.render(word, False, (0, 0, 0))
        self.rect = Rect(x, y, width, 25)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.m = m

    def mouseup(self):
        return self.w, self.h, self.m


class Grid:
    count_open = 0
    pressed = []
    change = []
    mined = []
    flaged = {}

    def __init__(self, x, y, pic):
        self.pic = pic
        self.open = False
        self.flag = False
        self.type = 'open'
        self.id = (x, y)
        self.x = x * 16 + 12
        self.y = y * 16 + 83
        self.unopen = pic['grid']
        self.pressImage = pic['0']
        self.flagImage = pic['flag']
        self.openImage = pic['0']
        self.wrong = pic['wrong']
        self.image = self.unopen

    def press_grid(self):
        self.image = self.pressImage
        Grid.pressed.append(self)
        Grid.change.append(self)

    def up_grid(self):
        self.image = self.unopen
        Grid.change.append(self)

    def open_grid(self):
        Grid.count_open += 1
        Grid.change.append(self)
        self.open = True
        self.image = self.openImage
        if self.type == 'mine':
            self.openImage = self.pic['boom']
            for g in [grid for grid in Grid.mined if grid.flag == False]:
                g.image = g.openImage
                Grid.change.append(g)
            for g in [grid for grid in Grid.flaged.values() if grid.type != 'mine']:
                g.image = g.wrong
                Grid.change.append(g)
            return 'lose', True

    def flag_grid(self):
        Grid.change.append(self)
        if not self.flag:
            Grid.flaged[self.id] = self
            self.flag = True
            self.image = self.flagImage
        else:
            del Grid.flaged[self.id]
            self.flag = False
            self.image = self.unopen


class Nonetype:
    open = True
    type = 'none'
    press = False
    flag = False


def draw_menu(mlist, mRect):
    screen.fill((242, 242, 242), mRect)
    pygame.draw.rect(screen, (204, 204, 204), (mRect[0], mRect[1], mRect[2] + 1, mRect[3] + 1), 1)  #########
    pygame.draw.line(screen, (204, 204, 204), (5, 55), (85, 55), 1)

    for m in mlist:
        screen.blit(m.text, (m.x + 5, m.y + 5))


def round_eight(this, grids):
    return [grids.get((this.id[0] - 1, this.id[1] - 1), Nonetype()),
            grids.get((this.id[0], this.id[1] - 1), Nonetype()),
            grids.get((this.id[0] + 1, this.id[1] - 1), Nonetype()),
            grids.get((this.id[0] - 1, this.id[1]), Nonetype()),
            grids.get((this.id[0] + 1, this.id[1]), Nonetype()),
            grids.get((this.id[0] - 1, this.id[1] + 1), Nonetype()),
            grids.get((this.id[0], this.id[1] + 1), Nonetype()),
            grids.get((this.id[0] + 1, this.id[1] + 1), Nonetype())]


def opening(this, grids):
    f, gameover = ('smile', False)
    for g in round_eight(this, grids):
        if not g.open and not g.flag:
            try:
                f, gameover = g.open_grid()
            except:
                pass
            if g.type == '0':
                opening(g, grids)
    return f, gameover


def game_init(g, w, h, pic):
    grids = g
    a = []
    for i in range(h + 1):
        a += [i] * w

    for i in zip(list(range(w)) * h, a):
        grids[i] = (Grid(i[0], i[1], pic))


def mine_init(g, m, minepic):
    grids = g
    for i in random.sample(list(grids), m):
        grids[i].type = 'mine'
        grids[i].openImage = minepic
        Grid.mined.append(grids[i])


def num_init(g, pic):
    grids = g
    for i in grids:
        if grids[i].type == 'open':
            grids[i].type = str([g.type for g in round_eight(grids[i], grids)].count('mine'))
            grids[i].openImage = pic[grids[i].type]


def init_grid_pic(src_pic):
    """初始化格子图片"""
    k = ['0', '1', '2', '3', '4', '5', '6', '7', '8', 'grid', '0', 'mine', 'flag', 'wrong', 'boom']
    v = []
    for i in range(15):
        v.append(src_pic.subsurface(i % 9 * 16, i // 9 * 16, 16, 16))
    Gpic = dict(zip(k, v))
    return Gpic


def init_face_pic(src_pic):
    """初始化笑脸图片"""
    k = ['smile', 'click', 'lose', 'win', 'press']
    v = []
    for i in range(5):
        v.append(src_pic.subsurface(27 * i, 55, 25, 25))
    Fpic = dict(zip(k, v))
    return Fpic


def init_time_pic(src_pic):
    """生成计时和计雷数用的时间数字图片"""
    t = []
    for i in range(11):
        t.append(src_pic.subsurface(i * 12, 33, 11, 21))
    return t


def init_element_pos(width, height):
    """直接修改一些元素的位置Rect"""
    global gridRect, facePos, faceRect, num_pos4, num_pos5, num_pos6, mlist
    gridRect = Rect((12, 83), (16 * width, height * 16))
    facePos = ((16 * width + 24) / 2 - 12.5, 41)
    faceRect = Rect(facePos, (25, 25))
    num_pos4 = (16 * width - 34 + 2, 43)
    num_pos5 = (16 * width - 34 + 15, 43)
    num_pos6 = (16 * width - 34 + 28, 43)
    mlist = [Menu(0, 0, -99, -99, -99, u'选项', width=40),
             Menu(0, 25, width, height, mines, u'开始       F2'),
             Menu(0, 60, 8, 8, 10, u'初级'),
             Menu(0, 85, 16, 16, 40, u'中级'),
             Menu(0, 110, 30, 16, 99, u'高级')]


def re_size(width, height):
    screen = pygame.display.set_mode((16 * width + 24, 16 * height + 94), 0, 32)
    src_pic = pygame.image.load('cloneskin.png').convert()
    init_element_pos(width, height)

    screen.fill((255, 255, 255), (0, 0, 16 * width + 24, 25))
    screen.blit(mlist[0].text, (mlist[0].x + 5, mlist[0].y + 5))

    panel = src_pic.subsurface(28, 82, 41, 25)
    panelPos1 = (17, 41)
    panelPos2 = (16 * width - 34, 41)

    lefttop = src_pic.subsurface(0, 82, 12, 11)
    leftmiddle = src_pic.subsurface(0, 96, 12, 11)
    leftmiddle1 = src_pic.subsurface(0, 94, 12, 1)
    leftbottom = src_pic.subsurface(0, 110, 12, 11)
    righttop = src_pic.subsurface(15, 82, 12, 11)
    rightmiddle = src_pic.subsurface(15, 96, 12, 11)
    rightmiddle1 = src_pic.subsurface(15, 94, 12, 1)
    rightbottom = src_pic.subsurface(15, 110, 12, 11)
    middletop = src_pic.subsurface(13, 82, 1, 11)
    onepixel = src_pic.subsurface(70, 82, 1, 1)

    for i in range(12, 16 * width + 12):
        for j in range(36, 72):
            screen.blit(onepixel, (i, j))

    for i in range(12, 16 * width + 12):
        screen.blit(middletop, (i, 25))
        screen.blit(middletop, (i, 72))
        screen.blit(middletop, (i, 16 * height + 83))

    for i in range(36, 16 * height + 83):
        screen.blit(leftmiddle1, (0, i))
        screen.blit(rightmiddle1, (16 * width + 12, i))

    screen.blit(lefttop, (0, 25))
    screen.blit(righttop, (16 * width + 12, 25))
    screen.blit(leftmiddle, (0, 73))
    screen.blit(rightmiddle, (16 * width + 12, 73))
    screen.blit(leftbottom, (0, 16 * height + 83))
    screen.blit(rightbottom, (16 * width + 12, 16 * height + 83))

    screen.blit(panel, panelPos1)
    screen.blit(panel, panelPos2)

    return screen, src_pic


def time_count():
    pass


pygame.init()
c = 1
resize = True

width = 8
height = 8
mines = 10

gridRect = Rect((12, 83), (16 * width, height * 16))
facePos = ((16 * width + 24) / 2 - 12.5, 41)
faceRect = Rect(facePos, (25, 25))
num_pos1 = (19, 43)
num_pos2 = (32, 43)
num_pos3 = (45, 43)
num_pos4 = (16 * width - 34 + 2, 43)
num_pos5 = (16 * width - 34 + 15, 43)
num_pos6 = (16 * width - 34 + 28, 43)
mRect = Rect(0, 25, 90, 135)
mlist = [Menu(0, 0, -99, -99, -99, u'选项', width=40),
         Menu(0, 25, width, height, mines, u'开始       F2'),
         Menu(0, 60, 8, 8, 10, u'初级'),
         Menu(0, 85, 16, 16, 40, u'中级'),
         Menu(0, 110, 30, 16, 99, u'高级')]

while True:
    time.sleep(0.002)

    pygame.display.set_caption('mine sweeper')

    if resize:
        resize = False

        screen, src_pic = re_size(width, height)
        Fpic = init_face_pic(src_pic)
        t = init_time_pic(src_pic)
        Gpic = init_grid_pic(src_pic)

        menu = False
        initial = True

    if initial:
        initial = False

        gameover = False
        facepress = False
        leftdown = False
        double = False

        Grid.count_open = 0
        Grid.mined = []
        Grid.flaged = {}

        face = Fpic['smile']

        time_count = 0

        screen.blit(t[mines // 100], num_pos1)
        screen.blit(t[mines % 100 // 10], num_pos2)
        screen.blit(t[mines % 100 % 10], num_pos3)

        screen.blit(t[0], num_pos4)
        screen.blit(t[0], num_pos5)
        screen.blit(t[0], num_pos6)

        screen.blit(face, facePos)

        grids = {}
        game_init(grids, width, height, Gpic)
        for i in grids:
            screen.blit(grids[i].image, (grids[i].x, grids[i].y))

    if not gameover:

        if time_count > 1:
            time_now = time.time() - time_begin
            if time_now < 999:
                screen.blit(t[(int(time_now) + 1) // 100], num_pos4)
                screen.blit(t[(int(time_now) + 1) % 100 // 10], num_pos5)
                screen.blit(t[(int(time_now) + 1) % 100 % 10], num_pos6)
        elif time_count == 1:
            time_begin = time.time()
            time_count += 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN and event.key == 283 and menu == False:
                initial = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu:
                    if not (mRect.collidepoint(event.pos) or mlist[0].rect.collidepoint(event.pos)):
                        menu = False
                        screen.blit(save, (0, 25))
                        screen.fill((255, 255, 255), mlist[0].rect)
                        screen.blit(mlist[0].text, (mlist[0].x + 5, mlist[0].y + 5))
                else:
                    if gridRect.collidepoint(event.pos):
                        x1, y1 = int((event.pos[0] - 12) / 16), int((event.pos[1] - 83) / 16)
                        mousePress = pygame.mouse.get_pressed()

                        if mousePress[0] == 1 and mousePress[2] == 0:
                            leftdown = True
                            face = Fpic['click']
                            if grids[(x1, y1)].flag == False and grids[(x1, y1)].open == False:
                                grids[(x1, y1)].press_grid()

                        elif mousePress[0] == 0 and mousePress[2] == 1 and grids[(x1, y1)].open == False:
                            grids[(x1, y1)].flag_grid()
                            if mines - len(Grid.flaged) >= 0:
                                screen.blit(t[(mines - len(Grid.flaged)) // 100], num_pos1)
                                screen.blit(t[(mines - len(Grid.flaged)) % 100 // 10], num_pos2)
                                screen.blit(t[(mines - len(Grid.flaged)) % 100 % 10], num_pos3)
                            else:
                                screen.blit(t[10], num_pos1)
                                screen.blit(t[abs(mines - len(Grid.flaged)) % 100 // 10], num_pos2)
                                screen.blit(t[abs(mines - len(Grid.flaged)) % 100 % 10], num_pos3)

                        elif mousePress[0] == 1 and mousePress[2] == 1:
                            leftdown = False
                            double = True
                            face = Fpic['click']
                            for g in round_eight(grids[(x1, y1)], grids) + [grids[(x1, y1)]]:
                                if g.open == False and g.flag == False:
                                    g.press_grid()
                        screen.blit(face, facePos)
                    elif faceRect.collidepoint(event.pos) and event.button == 1:
                        face = Fpic['press']
                        facepress = True
                        screen.blit(face, facePos)
                    elif mlist[0].rect.collidepoint(event.pos) and event.button == 1:
                        menu = True
                        save = screen.subsurface(mRect[0], mRect[1], mRect[2] + 1, mRect[3] + 1).copy()
                        draw_menu(mlist, mRect)
            elif event.type == pygame.MOUSEMOTION:
                if menu:
                    if mRect.collidepoint(event.pos):
                        for m1 in mlist[1:]:
                            if m1.rect.collidepoint(event.pos):
                                screen.fill((144, 200, 246), m1.rect)
                                screen.blit(m1.text, (m1.x + 5, m1.y + 5))
                            else:
                                screen.fill((242, 242, 242), m1.rect)
                                screen.blit(m1.text, (m1.x + 5, m1.y + 5))
                    else:
                        for m1 in mlist[1:]:
                            screen.fill((242, 242, 242), m1.rect)
                            screen.blit(m1.text, (m1.x + 5, m1.y + 5))
                elif sum(event.buttons) == 0:
                    if mlist[0].rect.collidepoint(event.pos):
                        c = 0
                        screen.fill((229, 243, 255), mlist[0].rect)
                        screen.blit(mlist[0].text, (mlist[0].x + 5, mlist[0].y + 5))
                    elif c == 0:
                        c = 1
                        screen.fill((255, 255, 255), mlist[0].rect)
                        screen.blit(mlist[0].text, (mlist[0].x + 5, mlist[0].y + 5))
                elif sum(event.buttons) != 0:
                    for i in range(len(Grid.pressed)):
                        Grid.pressed.pop().up_grid()
                    if gridRect.collidepoint(event.pos):
                        x1, y1 = int((event.pos[0] - 12) / 16), int((event.pos[1] - 83) / 16)
                        if leftdown == True and grids[(x1, y1)].flag == False and grids[(x1, y1)].open == False:
                            grids[(x1, y1)].press_grid()
                        elif double:
                            for g in round_eight(grids[(x1, y1)], grids) + [grids[(x1, y1)]]:
                                if g.open == False and g.flag == False:
                                    g.press_grid()
                    elif facepress and not faceRect.collidepoint(event.pos):
                        facepress = False
                        face = Fpic['smile']
                        screen.blit(face, facePos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if menu:
                    for m1 in mlist[1:]:
                        if m1.rect.collidepoint(event.pos):
                            width, height, mines = m1.mouseup()
                            resize = True
                else:
                    for i in range(len(Grid.pressed)):
                        Grid.pressed.pop().up_grid()
                    if leftdown:
                        face = Fpic['smile']
                        leftdown = False
                        if gridRect.collidepoint(event.pos):
                            x1, y1 = int((event.pos[0] - 12) / 16), int((event.pos[1] - 83) / 16)
                            if grids[(x1, y1)].flag == False and grids[(x1, y1)].open == False:
                                if time_count == 0:
                                    gg = grids[(x1, y1)]
                                    del grids[(x1, y1)]
                                    mine_init(grids, mines, Gpic['mine'])
                                    grids[(x1, y1)] = gg
                                    num_init(grids, Gpic)

                                try:
                                    f, gameover = grids[(x1, y1)].open_grid()
                                except:
                                    f = 'smile'
                                face = Fpic[f]
                                time_count += 1

                                if grids[(x1, y1)].type == '0':
                                    opening(grids[(x1, y1)], grids)

                    elif double == True:
                        face = Fpic['smile']
                        double = False
                        if gridRect.collidepoint(event.pos):
                            x1, y1 = int((event.pos[0] - 12) / 16), int((event.pos[1] - 83) / 16)
                            if grids[(x1, y1)].open == True and grids[(x1, y1)].type != '0':
                                count_flag = [f.flag for f in round_eight(grids[(x1, y1)], grids)].count(True)
                                if int(grids[(x1, y1)].type) == count_flag:
                                    f, gameover = opening(grids[(x1, y1)], grids)
                                    face = Fpic[f]

                    elif facepress == True:
                        initial = True

                    screen.blit(face, facePos)

        if Grid.count_open == width * height - mines and gameover == False:
            face = Fpic['win']
            gameover = True
            screen.blit(face, facePos)

        for i in range(len(Grid.change)):
            g = Grid.change.pop()
            screen.blit(g.image, (g.x, g.y))

        pygame.display.update()
    else:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN and event.key == 283:
            initial = True

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if menu == True:
                if not (mRect.collidepoint(event.pos) or mlist[0].rect.collidepoint(event.pos)):
                    menu = False
                    screen.blit(save, (0, 25))
                    screen.fill((255, 255, 255), mlist[0].rect)
                    screen.blit(mlist[0].text, (mlist[0].x + 5, mlist[0].y + 5))
            elif event.button == 1:
                if faceRect.collidepoint(event.pos):
                    res_face = face
                    face = Fpic['press']
                    facepress = True
                    screen.blit(face, facePos)
                elif mlist[0].rect.collidepoint(event.pos):
                    menu = True
                    save = screen.subsurface((mRect[0], mRect[1], mRect[2] + 1, mRect[3] + 1)).copy()
                    draw_menu(mlist, mRect)
        elif event.type == pygame.MOUSEMOTION:
            if menu == True:
                if mRect.collidepoint(event.pos):
                    for m1 in mlist[1:]:
                        if m1.rect.collidepoint(event.pos):
                            screen.fill((144, 200, 246), m1.rect)
                            screen.blit(m1.text, (m1.x + 5, m1.y + 5))
                        else:
                            screen.fill((242, 242, 242), m1.rect)
                            screen.blit(m1.text, (m1.x + 5, m1.y + 5))
                else:
                    for m1 in mlist[1:]:
                        screen.fill((242, 242, 242), m1.rect)
                        screen.blit(m1.text, (m1.x + 5, m1.y + 5))
            elif facepress == True and not faceRect.collidepoint(event.pos):
                facepress = False
                face = res_face
                screen.blit(face, facePos)
            elif sum(event.buttons) == 0:

                if mlist[0].rect.collidepoint(event.pos):
                    c = 0
                    screen.fill((229, 243, 255), mlist[0].rect)
                    screen.blit(mlist[0].text, (mlist[0].x + 5, mlist[0].y + 5))
                elif c == 0:
                    c = 1
                    screen.fill((255, 255, 255), mlist[0].rect)
                    screen.blit(mlist[0].text, (mlist[0].x + 5, mlist[0].y + 5))

        elif event.type == pygame.MOUSEBUTTONUP:
            if menu == True:
                for m1 in mlist[1:]:
                    if m1.rect.collidepoint(event.pos):
                        width, height, mines = m1.mouseup()
                        resize = True
            elif facepress == True:
                initial = True

        pygame.display.update()
