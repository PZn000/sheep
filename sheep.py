# 获取教程、习题、案例，共同学习、讨论、打卡
# 请关注：Crossin的编程教室
# QQ群：725903636，微信：sunset24678
# 代码使用 pygame-zero 框架，看起来与一般代码稍有不同，会有很多未定义的方法和变量，
# 在一些编辑器里会报错，但其实是可以运行的，无需手动增加 import。
# pgzero有两种方式运行（https://pygame-zero.readthedocs.io/zh_CN/latest/ide-mode.html）
# 本代码用的是第二种直接运行的方式（需新版pgzero）。
# 有部分读者反馈此代码在spyder上无法运行，类似情况可以尝试第一种传统方法：
# 把最后的pgzrun.go()去掉，然后直接在命令行该目录下运行： pgzrun sheep.py
import pgzero
import pgzrun
import pygame
import random
import math
import os
import time
# 定义游戏相关属性
TITLE = '动了个物'
WIDTH = 600
HEIGHT = 720
# 自定义游戏常量
T_WIDTH = 60
T_HEIGHT = 66
GAME_STATE = 0
TIME = 300
SVAE_TIME = 300
SCORE = 0
TEXT = 'timeleft:' + str(int(TIME))
# 下方牌堆的位置
DOCK = Rect((90, 564), (T_WIDTH*7, T_HEIGHT))
# 上方的所有牌
tiles = []
# 牌堆里的牌
docks = []
#界面对象
begin = Actor(('begin'),(300,250))
diffculty = Actor('diffculty',(300,450))
easy = Actor('easy',(300,100))
medium = Actor('medium',(300,300))
diffcult = Actor('diffcult',(300,500))
CURRENT_SCREEN = 0
# 初始化牌组，12*12张牌随机打乱
ts = list(range(1, 13))*12
random.shuffle(ts)
n = 0
for k in range(7):    # 7层
    for i in range(7-k):    #每层减1行
        for j in range(7-k):
            t = ts[n]        #获取排种类
            n += 1
            tile = Actor(f'a{t}')       #使用tileX图片创建Actor对象
            tile.pos = 120 + (k * 0.5 + j) * tile.width, 100 + (k * 0.5 + i) * tile.height * 0.9    #设定位置
            tile.tag = t            #记录种类
            tile.layer = k          #记录层级
            tile.status = 1 if k == 6 else 0        #除了最顶层，状态都设置为0（不可点）这里是个简化实现
            tiles.append(tile)
for i in range(4):        #剩余的4张牌放下面（为了凑整能通关）
    t = ts[n]
    n += 1
    tile = Actor(f'a{t}')
    tile.pos = 210 + i * tile.width, 516
    tile.tag = t
    tile.layer = 0
    tile.status = 1
    tiles.append(tile)

def init():
    global docks
    global tiles
    global SCORE
    SCORE = 0
    docks = []
    tiles = []
    ts = list(range(1, 13)) * 12
    random.shuffle(ts)
    n = 0
    for k in range(7):  # 7层
        for i in range(7 - k):  # 每层减1行
            for j in range(7 - k):
                t = ts[n]  # 获取排种类
                n += 1
                tile = Actor(f'a{t}')  # 使用tileX图片创建Actor对象
                tile.pos = 120 + (k * 0.5 + j) * tile.width, 100 + (k * 0.5 + i) * tile.height * 0.9  # 设定位置
                tile.tag = t  # 记录种类
                tile.layer = k  # 记录层级
                tile.status = 1 if k == 6 else 0  # 除了最顶层，状态都设置为0（不可点）这里是个简化实现
                tiles.append(tile)
    for i in range(4):  # 剩余的4张牌放下面（为了凑整能通关）
        t = ts[n]
        n += 1
        tile = Actor(f'a{t}')
        tile.pos = 210 + i * tile.width, 516
        tile.tag = t
        tile.layer = 0
        tile.status = 1
        tiles.append(tile)
def draw_time():
    global TIME
    global TEXT
    screen.draw.text(TEXT,(330,30),fontsize = 50,color = 'red')
def drow_score():
    screen.draw.text('score:'+str(SCORE),(100,30),fontsize = 50, color = 'blue')
def draw_menu():
    screen.clear()
    screen.fill((0,255,255))
    screen.draw.text("animals",(160,100),fontsize = 100)
    begin.draw()
    diffculty.draw()
def draw_diffculty():
    screen.clear()
    screen.fill((0,255,255))
    easy.draw()
    medium.draw()
    diffcult.draw()
def draw_fail():
    screen.clear()
    screen.blit('fail',(0,0))
    screen.draw.text('your score:' + str(SCORE),(200,550),fontsize = 50, color = 'blue')
def draw_win():
    screen.clear()
    screen.blit('win',(0,0))
def update():
    global TIME
    global TEXT
    global GAME_STATE
    # 超过7张，失败
    if len(docks) >= 7:
        GAME_STATE = 3
    # 没有剩牌，胜利
    if len(tiles) == 0:
        GAME_STATE = 4
    if TIME > 0 and GAME_STATE == 1:
        TIME -= 1/60
        TEXT = 'timeleft:' + str((int(TIME)))
    if GAME_STATE == 1 and TIME < 0:
        GAME_STATE = 3
# 绘制函数
def draw():
    global CURRENT_SCREEN
    global TIME
    global GAME_STATE
    global docks
    if GAME_STATE == 3:
        draw_fail()
        CURRENT_SCREEN = 3
    if GAME_STATE == 0:
        draw_menu()
        CURRENT_SCREEN = 0
    if GAME_STATE == 2:
        draw_diffculty()
        CURRENT_SCREEN = 2
    if GAME_STATE == 4:
        draw_win()
        CURRENT_SCREEN =4
    if GAME_STATE == 1:
        CURRENT_SCREEN = 1
        #背景图
        screen.blit('back', (0, 0))
        drow_score()
        draw_time()
        for tile in tiles:
            #绘制上方牌组
            tile.draw()
            if tile.status == 0:
                screen.blit('mask', tile.topleft)     #不可点的添加遮罩
        for i, tile in enumerate(docks):
            #绘制排队，先调整一下位置（因为可能有牌被消掉）
            tile.left = (DOCK.x + i * T_WIDTH)
            tile.top = DOCK.y
            tile.draw()

def on_mouse_down(pos,button):
    global GAME_STATE
    global TIME
    global CURRENT_SCREEN
    global SVAE_TIME
    global SCORE
    if GAME_STATE == 0 and CURRENT_SCREEN == 0:
        if begin.collidepoint(pos) :
            init()
            GAME_STATE = 1
        if diffculty.collidepoint(pos):
            GAME_STATE = 2
    if GAME_STATE == 2 and CURRENT_SCREEN == 2:
        if easy.collidepoint(pos) :
            TIME = 300
            SVAE_TIME =300
            GAME_STATE = 0
        if medium.collidepoint(pos):
            TIME = 240
            SVAE_TIME = 240
            GAME_STATE = 0
        if diffcult.collidepoint(pos):
            TIME = 180
            SVAE_TIME = 180
            GAME_STATE = 0
    if GAME_STATE == 3 and CURRENT_SCREEN == 3:
        x,y = pos
        if 180<x<430 and 350<y<420:
            init()
            GAME_STATE = 1
            TIME = SVAE_TIME
        if 180<x<430 and 440<y<540:
            init()
            GAME_STATE = 0
            TIME = SVAE_TIME
    if GAME_STATE == 4 and CURRENT_SCREEN == 4:
        x, y = pos
        if 180 < x < 430 and 350 < y < 420:
            init()
            GAME_STATE = 1
            TIME = SVAE_TIME
        if 180 < x < 430 and 440 < y < 540:
            init()
            GAME_STATE = 0
            TIME = SVAE_TIME
    if GAME_STATE == 1 and CURRENT_SCREEN == 1:
        global docks
        for tile in reversed(tiles):    #逆序循环是为了先判断上方的牌，如果点击了就直接跳出，避免重复判定
            if tile.status == 1 and tile.collidepoint(pos):
                # 状态1可点，并且鼠标在范围内
                tile.status = 2
                tiles.remove(tile)
                diff = [t for t in docks if t.tag != tile.tag]    #获取牌堆内不相同的牌
                if len(docks) - len(diff) < 2:    #如果相同的牌数量<2，就加进牌堆
                    docks.append(tile)
                else:             #否则用不相同的牌替换牌堆（即消除相同的牌）
                    docks = diff
                    SCORE += 100
                for down in tiles:      #遍历所有的牌
                    if down.layer == tile.layer - 1 and down.colliderect(tile):   #如果在此牌的下一层，并且有重叠
                        for up in tiles:      #那就再反过来判断这种被覆盖的牌，是否还有其他牌覆盖它
                            if up.layer == down.layer + 1 and up.colliderect(down):     #如果有就跳出
                                break
                        else:      #如果全都没有，说明它变成了可点状态
                            down.status = 1
                return
music.play('bgm')

pgzrun.go()
