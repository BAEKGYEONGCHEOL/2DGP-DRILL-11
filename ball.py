from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel
GRAVITY = 9.8  # 중력 가속도 (m/s²)

class Ball:
    image = None

    def __init__(self, x = 400, y = 300, throwin_speed = 15, throwin_angle = 45):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y
        self.xv = throwin_speed * math.cos(math.radians(throwin_angle))  # m/s
        self.yv = abs(throwin_speed * math.sin(math.radians(throwin_angle)))   # m/s
        self.stopped = True if throwin_speed == 0.0 else False
        self.stop_state = False

    def draw(self):
        self.image.draw(self.x, self.y)
        # draw_rectangle(): 좌상단(x1, y1), 우하단(x2, y2) 2개의 점을 가지고 빨간색 사각형을 그려준다.
        # 튜플은 하나의 파라미터로 간주가 되기 때문에 *를 붙여서 튜플을 풀어준다. -> 4개의 인자로 변환
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.stopped:
            return
        # 위치 업데이트
        self.x += self.xv * game_framework.frame_time * PIXEL_PER_METER
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        # y 축 속도에 중력 가속도 적용
        self.yv -= GRAVITY * game_framework.frame_time  # m/s

    def get_bb(self):
        # ball의 바운더리 박스를 튜플 형태로 반환하여 사각형의 범위를 알려준다.
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        # group이 소년과 볼 사이의 충돌이라면
        if group == 'boy:ball':
            # 아래처럼 작성하면 지울 수 없는 에러가 발생!
            # game_worl d에서는 ball 이 사라졌지만 collision_pairs 에는 여전히 남아 있기 때문이다.
            # collision_pairs 에서는 계속해서 비교를 시도하게 되고, 이미 지워진 ball 객체에 접근하려고 하면서 에러가 발생한다.
            # 해결 방법은 collision_pairs 에서도 해당 객체를 제거해 주어야 한다.
            # 이 작업은 game_world.py 의 game_world.remove_object() 함수에서 처리해 준다.
            game_world.remove_object(self)
        # group이 잔디와 볼 사이의 충돌이라면
        elif group == 'grass:ball' and self.stop_state == False:
            # 볼이 잔디 위에서 멈춘다.
            self.stopped = True
            self.stop_state = True
        elif group == 'zombie:ball' and self.stop_state == False:
            # 볼이 좀비와 충돌하면 제거한다.
            game_world.remove_object(self)