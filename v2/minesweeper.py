import pygame
from pygame.locals import *
import random
import win32gui
import tkinter as tk
from multiprocessing import Process, Queue
import time


def init_real_menu(x, y, q_in, q_out):
    a = RealMenu(x, y, q_in, q_out)


def game_init(width, height, mines):
    pygame.init()
    pygame.display.set_caption('mine sweeper')
    screen = pygame.display.set_mode((16 * width + 24, 16 * height + 94), 0, 32)

    src_pic = pygame.image.load('cloneskin.png').convert()
    face_pic = init_face_pic(src_pic)
    num_pic = init_time_pic(src_pic)
    grid_pic = init_grid_pic(src_pic)

    grid_rect = Rect((12, 83), (16 * width, height * 16))

    face_pos = ((16 * width + 24) / 2 - 12.5, 41)
    face = Face(face_pos, face_pic, screen)
    gridgroup = grid_init(width, height, grid_pic, grid_rect, screen, mines)

    num_pos1 = (19, 43)
    num_pos2 = (32, 43)
    num_pos3 = (45, 43)
    num_pos4 = (16 * width - 34 + 2, 43)
    num_pos5 = (16 * width - 34 + 15, 43)
    num_pos6 = (16 * width - 34 + 28, 43)

    time_count = CountBoard(num_pic, num_pos4, num_pos5, num_pos6, screen)
    mine_count = CountBoard(num_pic, num_pos1, num_pos2, num_pos3, screen)

    fake_menu = MenuBar(screen)

    game_init_draw(screen, face, width, height, src_pic, gridgroup, time_count, mine_count, mines, fake_menu)

    return screen, face, gridgroup, time_count, mine_count, fake_menu


def game_init_draw(screen, face, width, height, src_pic, ggroup, time_count, mine_count, mines, fake_menu):
    """调整游戏难度时重新绘制游戏画面"""

    screen.fill((240, 240, 240), (0, 0, 16 * width + 24, 25))

    # 绘制背景，边框等
    onepixel = src_pic.subsurface(70, 82, 1, 1)
    middletop = src_pic.subsurface(13, 82, 1, 11)
    leftmiddle1 = src_pic.subsurface(0, 94, 12, 1)
    rightmiddle1 = src_pic.subsurface(15, 94, 12, 1)
    lefttop = src_pic.subsurface(0, 82, 12, 11)
    leftmiddle = src_pic.subsurface(0, 96, 12, 11)
    leftbottom = src_pic.subsurface(0, 110, 12, 11)
    righttop = src_pic.subsurface(15, 82, 12, 11)
    rightmiddle = src_pic.subsurface(15, 96, 12, 11)
    rightbottom = src_pic.subsurface(15, 110, 12, 11)

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
    screen.blit(leftmiddle, (0, 73))
    screen.blit(leftbottom, (0, 16 * height + 83))
    screen.blit(righttop, (16 * width + 12, 25))
    screen.blit(rightmiddle, (16 * width + 12, 73))
    screen.blit(rightbottom, (16 * width + 12, 16 * height + 83))

    # 绘制两侧计数器背景板
    panel = src_pic.subsurface(28, 82, 41, 25)
    panelPos1 = (17, 41)
    panelPos2 = (16 * width - 34, 41)

    screen.blit(panel, panelPos1)
    screen.blit(panel, panelPos2)

    # 绘制笑脸
    face.screen_blit()
    # 绘制计数数字
    time_count.draw(0)
    mine_count.draw(mines)

    # 绘制格子
    for i in ggroup.grids.values():
        screen.blit(i.image, (i.x, i.y))

    # 绘制菜单
    fake_menu.draw_fake_menu()


def grid_init(w, h, pic, grid_rect, screen, mines):
    a = []
    for i in range(h + 1):
        a += [i] * w

    gridgroup = GridGroup(grid_rect, screen, mines)
    for i in zip(list(range(w)) * h, a):
        gridgroup.add_grid(i, Grid(i[0], i[1], pic, gridgroup))
    return gridgroup


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


def time_count(time_count_begin):
    pass


def handler_menu_info(info):
    if info['type'] == 'change_level':
        pass


class Grid:
    """单个的格子"""

    def __init__(self, x, y, pic, ggroup):
        """
        x,y : 格子的横纵坐标
        pic : 每个格子可能用到的图片，包括空白，1-8的数字，地雷，旗子，非雷格子错误标记后显示的叉叉，以及格子被按下时的图片
        ggroup : 所在的组，所有格子都会添加到这个 对象 里面统一管理
        """
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
        self.pressed = False
        self.ggroup = ggroup

    def press_grid(self):
        """格子被按下"""
        if not self.flag and not self.open:
            self.pressed = True
            self.image = self.pressImage
            self.ggroup.pressed.append(self)
            self.ggroup.changed.append(self)

    def up_grid(self):
        """格子按下后，没有被打开的情况下，弹起恢复原样"""
        if self.pressed:
            self.pressed = False
            self.image = self.unopen
            self.ggroup.changed.append(self)

    def open_grid(self):
        """格子被打开"""
        if not self.flag and not self.open:
            self.open = True
            self.ggroup.changed.append(self)
            self.image = self.openImage
            if self.type == 'mine':
                self.ggroup.on_mine = True
                self.openImage = self.pic['boom']
            else:
                self.ggroup.count_open += 1

    def flag_grid(self):
        """右键插旗"""
        if not self.open:
            self.ggroup.changed.append(self)
            if not self.flag:
                self.ggroup.flaged[self.id] = self
                self.flag = True
                self.image = self.flagImage
            else:
                del self.ggroup.flaged[self.id]
                self.flag = False
                self.image = self.unopen


class GridGroup:
    """统一管理所有grid对象"""

    def __init__(self, rect, screen, mines):
        """
        :param rect: 整个所有格子所在区域的rect对象
        :param screen: 所在的screen，要在上面绘制
        :param mines: 初始化设定的地雷的数量
        """
        self.grids = {}
        self.count_open = 0
        self.pressed = []
        self.changed = []
        self.mined = []
        self.flaged = {}
        self.on_mine = False
        self.rect = rect
        self.double_pressed = False
        self.left_down = False
        self.screen = screen
        self.mine_count = mines

    def add_grid(self, grid_id, grid):
        self.grids[grid_id] = grid

    def round_eight(self, center):
        """返回某个格子周边8个格子对象"""
        grid_list = [self.grids.get((center.id[0] - 1, center.id[1] - 1)),
                     self.grids.get((center.id[0], center.id[1] - 1)),
                     self.grids.get((center.id[0] + 1, center.id[1] - 1)),
                     self.grids.get((center.id[0] - 1, center.id[1])),
                     self.grids.get((center.id[0] + 1, center.id[1])),
                     self.grids.get((center.id[0] - 1, center.id[1] + 1)),
                     self.grids.get((center.id[0], center.id[1] + 1)),
                     self.grids.get((center.id[0] + 1, center.id[1] + 1))]
        return [x for x in grid_list if x is not None]

    def open_grids(self, center, grids):
        """打开成片的格子，用于点开空白格子的情况"""
        for g in self.round_eight(center):
            if not g.open and not g.flag:
                g.open_grid()
                if g.type == '0':
                    self.open_grids(g, grids)

    def mine_init(self, tmp_grids, mines, minepic):
        """点开第一个格子后，初始化随机布置地雷"""
        for i in random.sample(list(tmp_grids), mines):
            tmp_grids[i].type = 'mine'
            tmp_grids[i].openImage = minepic
            self.mined.append(tmp_grids[i])

    def num_init(self, pic):
        """布置地雷完成后，按地雷分布设置其他格子的数字"""
        for g in self.grids.values():
            if g.type == 'open':
                g.type = str([g.type for g in self.round_eight(g)].count('mine'))
                g.openImage = pic[g.type]

    def screen_blit(self, img, pos):
        self.screen.blit(img, pos)

    def failed_draw(self):
        """踩地雷时游戏结束，翻开相应的格子"""
        for g in [grid for grid in self.mined if not grid.flag]:
            g.image = g.openImage
            self.changed.append(g)
        for g in [grid for grid in self.flaged.values() if grid.type != 'mine']:
            g.image = g.wrong
            self.changed.append(g)

    def reset(self, event):
        """当事件在区域外发生时，当前对象失去焦点时，需要做出的一些动作"""
        for _ in range(len(self.pressed)):
            self.pressed.pop().up_grid()
        if event.type == pygame.MOUSEBUTTONUP and event.button != 2:
            self.double_pressed = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.left_down = False
        for i in range(len(self.changed)):
            g = self.changed.pop()
            self.screen.blit(g.image, (g.x, g.y))

    def on_event(self, event, face, mine_countboard):
        """响应在本区域内发生的鼠标事件，即游戏过程的响应"""
        x, y = int((event.pos[0] - 12) / 16), int((event.pos[1] - 83) / 16)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.on_mouse_down(face, (x, y), mine_countboard)
        elif event.type == pygame.MOUSEMOTION:
            self.on_mouse_motion(event, (x, y))
        elif event.type == pygame.MOUSEBUTTONUP:
            self.on_mouse_up(event, face, (x, y))
        for i in range(len(self.changed)):
            g = self.changed.pop()
            self.screen.blit(g.image, (g.x, g.y))

    def on_mouse_down(self, face, grid_id, mine_countboard):
        mousepressd = pygame.mouse.get_pressed(3)
        if mousepressd[0] == 1 and mousepressd[2] == 0:
            self.grids[grid_id].press_grid()
            self.left_down = True
            face.on_click()
        elif mousepressd[0] == 0 and mousepressd[2] == 1:
            self.grids[grid_id].flag_grid()
            mine_countboard.draw(self.mine_count - len(self.flaged))
        elif mousepressd[0] == 1 and mousepressd[2] == 1:
            self.grids[grid_id].press_grid()
            self.double_pressed = True
            self.left_down = False
            face.on_click()
            for g in self.round_eight(self.grids[grid_id]):
                g.press_grid()

    def on_mouse_motion(self, event, grid_id):
        for _ in range(len(self.pressed)):
            self.pressed.pop().up_grid()
        if event.buttons[0] == 1 and event.buttons[2] == 0 and self.left_down:
            self.grids[grid_id].press_grid()
        elif event.buttons[0] == 1 and event.buttons[2] == 1 and self.double_pressed:
            self.grids[grid_id].press_grid()
            for g in self.round_eight(self.grids[grid_id]):
                g.press_grid()

    def on_mouse_up(self, event, face, grid_id):
        if event.button != 2:
            for _ in range(len(self.pressed)):
                self.pressed.pop().up_grid()
            if self.double_pressed:
                self.double_pressed = False
                if self.grids[grid_id].open and self.grids[grid_id].type != '0':
                    count_flag = [g.flag for g in self.round_eight(self.grids[grid_id])].count(True)
                    if int(self.grids[grid_id].type) == count_flag:  # int('mine')
                        self.open_grids(self.grids[grid_id], self.grids)
            elif self.left_down:
                if not self.grids[grid_id].open and event.button == 1:
                    if self.count_open > 0:
                        self.grids[grid_id].open_grid()
                        if self.grids[grid_id].type == '0':
                            self.open_grids(self.grids[grid_id], self.grids)
                    elif self.count_open == 0:
                        tmp_grids = {k: v for k, v in self.grids.items() if k != grid_id}
                        self.mine_init(tmp_grids, self.mine_count, self.grids[grid_id].pic['mine'])
                        self.num_init(self.grids[grid_id].pic)
                        self.grids[grid_id].open_grid()
                        if self.grids[grid_id].type == '0':
                            self.open_grids(self.grids[grid_id], self.grids)

            if self.on_mine:
                self.failed_draw()
                face.if_lose()
            elif len(self.grids) - len(self.mined) == self.count_open:
                face.if_win()
            else:
                face.unpress_face()


class CountBoard:
    """两侧计数器"""

    def __init__(self, pic, pos1, pos2, pos3, screen):
        """
        :param pic: 计数器需要用到的数字图片字典
        :param pos1: 第一个数字的位置
        :param pos2: 第二个数字的位置
        :param pos3: 第三个数字的位置
        :param screen: 所要绘制的screen
        """
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos3 = pos3
        self.pic = pic
        self.screen = screen

    def draw(self, num):
        """按照传入的数字取出相应图片并绘制"""
        if num > 999:
            num = 999
        if num >= 0:
            single_ind = num % 100 % 10
            tens_ind = num % 100 // 10
            hundreds_ind = num // 100
        else:
            single_ind = abs(num % 100 % 10)
            tens_ind = abs(num % 100 // 10)
            hundreds_ind = 10

        self.screen.blit(self.pic[hundreds_ind], self.pos1)
        self.screen.blit(self.pic[tens_ind], self.pos2)
        self.screen.blit(self.pic[single_ind], self.pos3)


class Face:
    """笑脸按钮对象"""

    def __init__(self, pos, pic, screen):
        self.pic = pic
        self.pos = pos
        self.rect = Rect(self.pos, (25, 25))
        self.img = self.pic['smile']
        self.last_face = self.pic['smile']
        self.pressed = False
        self.screen = screen

    def press_face(self):
        self.img = self.pic['press']
        self.pressed = True
        self.screen_blit()

    def unpress_face(self):
        self.img = self.last_face
        self.pressed = False
        self.screen_blit()

    def on_click(self):
        self.img = self.pic['click']
        self.screen_blit()

    def if_win(self):
        self.img = self.pic['win']
        self.last_face = self.img
        self.screen_blit()

    def if_lose(self):
        self.img = self.pic['lose']
        self.last_face = self.img
        self.screen_blit()

    def screen_blit(self):
        self.screen.blit(self.img, self.pos)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.last_face = self.img
            self.press_face()
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed:
                self.screen_blit()
                return 'RESTART'
        self.screen_blit()
        return 'CONTINUE'

    def reset(self):
        self.unpress_face()
        self.screen_blit()


class MenuBar:
    """在菜单没有真正使用的情况下生成的假菜单栏。。为了避免真菜单栏在窗口拖动时需要同步移动的麻烦"""
    def __init__(self, screen):
        self.buttons = []
        self.rect = Rect(0, 5, 120, 24)
        self.screen = screen
        self.add_fake_button()
        self.real_menu = False
        self.real_menu_process = None
        self.q_in = Queue()
        self.q_out = Queue()

    def on_event(self, event):
        if event.type == pygame.MOUSEMOTION and not self.real_menu:
            print('%s menu_on_foucs' % time.time())
            info = pygame.display.get_wm_info()
            rect = win32gui.GetWindowRect(info['window'])
            self.real_menu_process = Process(target=init_real_menu, args=(rect[0] + 8, rect[1] + 34, self.q_in, self.q_out), name='real_menu')
            self.real_menu_process.start()
            self.real_menu = True

    def reset(self, event):
        """失去焦点，恢复假菜单栏，菜单栏和窗口标题之间要留空"""
        if event.type == pygame.MOUSEMOTION and self.real_menu:
            self.draw_fake_menu()
            self.q_in.put('exit')
            self.real_menu = False

    def draw_fake_menu(self):
        for b in self.buttons:
            self.screen.blit(b.text, (b.x + 5, b.y + 5))

    def add_fake_button(self):
        btnlist = [FakeMenuButton(0, 0, u'游戏'),
                   # FakeMenuButton(40, 0, u'选项'),
                   # FakeMenuButton(80, 0, u'说明')
                   ]
        for b in btnlist:
            self.buttons.append(b)


class FakeMenuButton:
    def __init__(self, x, y, word=u'按钮', size=12):
        myfont = pygame.font.SysFont('simsunnsimsun', size)
        self.text = myfont.render(word, False, (0, 0, 0))
        self.rect = Rect(x, y, 40, 24)
        self.x = x
        self.y = y


class RealMenu:

    def __init__(self, x, y, q_in, q_out):
        self.x = x
        self.y = y
        self.q_in = q_in
        self.q_out = q_out
        self.root = tk.Tk()
        self.init_menu(x, y)

    def init_menu(self, x, y):
        self.root.overrideredirect(True)
        self.root.geometry('120x0+%s+%s' % (x, y))

        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='游戏', menu=filemenu)

        # filemenu.add_command(label='新游戏')
        # filemenu.add_separator()
        filemenu.add_command(label='初级', command=lambda: self.change_level(8, 8, 10))
        filemenu.add_command(label='中级', command=lambda: self.change_level(16, 16, 40))
        filemenu.add_command(label='高级', command=lambda: self.change_level(30, 16, 99))
        # filemenu.add_command(label='自定义')
        # filemenu.add_separator()
        # filemenu.add_command(label='退出', command=self.root.quit)

        self.root.configure(menu=menubar)

        self.root.after(50, self.get_msg, self.q_in)
        self.root.mainloop()

    def change_level(self, width, height, mines):
        print(width, height)
        menu_info = {'type': 'change_level',
                     'width': width,
                     'height': height,
                     'mines': mines}
        self.q_out.put(menu_info)
        self.root.quit()

    def get_msg(self, q_in):
        # print('data in q: ', q_in.qsize())
        if not q_in.empty():
            info = q_in.get()
            if info == 'exit':
                self.root.quit()
        self.root.after(50, self.get_msg, q_in)














