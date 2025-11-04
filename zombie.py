import random
import math
import game_framework
import game_world

from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.size = 200
        self.hit_state = False


    def get_bb(self):
        return self.x - self.size / 2, (self.y - (100 - self.size / 2)) - self.size / 2, self.x + self.size / 2, (self.y - (100 - self.size / 2)) + self.size / 2

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)
        pass


    def draw(self):
        if self.dir < 0:
            Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y - (100 - self.size / 2), self.size, self.size)
        else:
            Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y - (100 - self.size / 2), self.size, self.size)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        # group이 소년과 좀비 사이의 충돌이라면
        if group == 'boy:zombie':
            # 게임 종료
            game_framework.quit()
        # group이 좀비와 공 사이의 충돌이라면
        elif group == 'zombie:ball' and self.hit_state == False:
            # 공이 멈춰있으면 함수 종료!
            if other.stop_state == True:
                return
            # 1차적으로 좀비 크기 감소
            self.size *= 1/2
            self.hit_state = True
        elif group == 'zombie:ball' and self.hit_state == True:
            # 공이 멈춰있으면 함수 종료!
            if other.stop_state == True:
                return
            # 2차적으로 좀비 제거
            game_world.remove_object(self)