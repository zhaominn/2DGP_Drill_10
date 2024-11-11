# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font
from state_machine import *
import game_world
import game_framework

# Bird Run Speed
PIXEL_PER_METER =(10.0/0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH=20.0 # km/Hour
RUN_SPEED_MSM=(RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS=(RUN_SPEED_MSM/60.0)
RUN_SPEED_PPS=(RUN_SPEED_MPS*PIXEL_PER_METER)
# Bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Run:
    @staticmethod
    def enter(bird, e):
        bird.frame=random.randint(0,4)
        bird.dir=bird.face_dir

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if bird.x>=1650 or bird.x<=-50:
            bird.dir*=-1
            bird.face_dir*=-1
        #PPS : 픽셀 퍼 세컨드
    @staticmethod
    def draw(bird):
        if bird.dir==1:
            bird.image.clip_draw(int(bird.frame) * int(917/5), bird.action * int(505/3), int(917/5), int(505/3), bird.x, bird.y)
        elif bird.dir==-1:
            bird.image.clip_composite_draw(int(bird.frame) * int(917/5), bird.action * int(505/3),int(917/5),int(505/3), 0, 'h', bird.x, bird.y)





class Bird:

    def __init__(self):
        self.x, self.y = -50, random.randint(400,550)
        self.face_dir = random.randint(0,1)
        if self.face_dir ==0:
            self.face_dir=-1
            self.x, self.y = 1650, random.randint(400, 550)
        self.action=0
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Run)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()