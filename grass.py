from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)
        # draw_rectangle(): 좌상단(x1, y1), 우하단(x2, y2) 2개의 점을 가지고 빨간색 사각형을 그려준다.
        # 튜플은 하나의 파라미터로 간주가 되기 때문에 *를 붙여서 튜플을 풀어준다. -> 4개의 인자로 변환
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0, 0, 1600, 50

    # 잔디는 충돌 처리에 대한 아무런 동작을 하지 않으므로 빈 함수로 둔다.
    def handle_collision(self, group, other):
        pass