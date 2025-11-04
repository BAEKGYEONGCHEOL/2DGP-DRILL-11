import random
from pico2d import *

import game_framework
import game_world

from boy import Boy
from grass import Grass
from ball import Ball
from zombie import Zombie

boy = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy

    grass = Grass()
    game_world.add_object(grass, 0)
    # 잔디를 만들 때 잔디와 볼의 충돌 검사가 필요하다는 정보를 추가
    game_world.add_collision_pair('grass:ball', grass, None)

    boy = Boy()
    game_world.add_object(boy, 1)

    global balls
    balls = [Ball(random.randint(100, 1600-100), 60, 0) for _ in range(30)]
    game_world.add_objects(balls, 1)

    # 소년과 볼 사이에 대한 충돌 검사가 필요하다는 정보를 추가
    # game_world 에 정보를 추가 -> boy와 ball 사이의 충돌 검사가 필요하다는 정보
    # 첫 번째 함수는 boy 객체를 전달, 두 번째는 None
    # 두 번째 함수는 ball 객체를 전달, 첫 번째는 None
    game_world.add_collision_pair('boy:ball', boy, None)
    for ball in balls:
        game_world.add_collision_pair('boy:ball', None, ball)


    # 좀비를 추가!
    zombies = [Zombie() for _ in range(4)]
    game_world.add_objects(zombies, 1)

    # 좀비와 소년 사이에 대한 충돌 검사가 필요하다는 정보를 추가
    game_world.add_collision_pair('boy:zombie', boy, None)
    for zombie in zombies:
        game_world.add_collision_pair('boy:zombie', None, zombie)

    # 좀비와 소년이 발사한 볼 사이의 충돌 검사가 필요하다는 정보 추가
    for zombie in zombies:
        game_world.add_collision_pair('zombie:ball', zombie, None)


def update():
    game_world.update()
    # for ball in balls.copy():
    # # 각각의 ball이 소년과 만나는지 확인이 필요
    #     if game_world.collide(boy, ball):
    #         print('COLLISION boy:ball')
    #         # 아래처럼 작성하면 에러가 발생!
    #         # 여기서 삭제를 해도 balls 리스트에는 여전히 남아있기 때문이다.
    #         # 계속 충돌이 발생하게 되므로 무한 출력이 된다.
    #         # boy.ball_count += 1
    #         # game_world.remove_object(ball)
    #         # 아래처럼 balls.remove(ball) 을 하여 리스트에서도 제거해야 한다.
    #         # 위처럼 balls.copy() 로 복사본을 만들어서 처리하는 것이 더 안전하다.
    #         boy.ball_count += 1
    #         game_world.remove_object(ball)
    #         balls.remove(ball)
    #         # 하지만 위처럼 작성하면 충돌 처리 내용이 길어질수록 더 복잡해지기 때문에 사용하지 않는다.
    #         # 좀 더 객체 지향적인 방법으로 처리하는 것이 좋다.

    # 충돌 처리 담당 함수 호출
    game_world.handle_collision()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

