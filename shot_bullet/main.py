import asyncio
import pyxel
import micropip


# メイン関数を非同期で実行するための関数
def run_asyncio():
    # 現在のイベントループを取得
    loop = asyncio.get_event_loop()

    # イベントループが実行中か確認
    if loop.is_running():
        # 実行中の場合は、非同期タスクとしてmain()を登録
        asyncio.ensure_future(main())
    else:
        # 実行中でない場合は、新しいイベントループでmain()を実行
        asyncio.run(main())


# 非同期のメイン関数
async def main():
    try:
        # micropipを使ってwhlファイルからpymunkをインストール
        print("Installing Pymunk...")
        await micropip.install(
            "https://yutams.github.io/game01/pymunk-6.11.0-cp312-cp312-pyodide_2024_0_wasm32.whl"
        )
        print("Pymunk installed successfully")

        # pymunkをインポート
        import pymunk

        # Appクラスを初期化して実行
        App(pymunk)
    except Exception as e:
        print(f"Error: {e}")


class App:
    def __init__(self, pymunk, fps=60):
        self.pymunk = pymunk
        self.fps = fps

        pyxel.init(256, 256, fps=fps, title="Vertical Stack with Pyxel")
        pyxel.load("shot_bullet.pyxres")
        self.create_world()
        pyxel.run(self.update, self.draw)

    def create_world(self):
        self.space = self.pymunk.Space()
        self.space.gravity = 0, 900
        self.space.sleep_time_threshold = 0.3

        # Static lines
        static_lines = [
            self.pymunk.Segment(self.space.static_body, (10, 200), (240, 200), 1),
            self.pymunk.Segment(self.space.static_body, (230, 200), (230, 50), 1),
        ]
        for line in static_lines:
            line.friction = 0.3
        self.space.add(*static_lines)

        # Stacked boxes
        self.shapes = []
        for x in range(5):
            for y in range(10):
                size = 10
                mass = 10.0
                moment = self.pymunk.moment_for_box(mass, (size, size))
                block_body = self.pymunk.Body(mass, moment)
                block_body.position = 100 + x * 20, 100 + y * (size + 0.1)
                block_shape = self.pymunk.Poly.create_box(block_body, (size, size))
                block_shape.friction = 0.3
                self.space.add(block_body, block_shape)
                self.shapes.append(block_shape)
        # Bullets
        self.bullets = []

    def update(self):
        step = 5  # Run multiple steps for more stable simulation
        step_dt = 1 / self.fps / step
        for _ in range(step):
            self.space.step(step_dt)

        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            mass = 100
            r = 5
            moment = self.pymunk.moment_for_circle(mass, 0, r, (0, 0))
            bullet_body = self.pymunk.Body(mass, moment)
            bullet_body.position = (10, 165)
            bullet_shape = self.pymunk.Circle(bullet_body, r, (0, 0))
            bullet_shape.friction = 0.3
            self.space.add(bullet_body, bullet_shape)
            self.bullets.append(bullet_shape)

            impulse = 150_000
            bullet_body.apply_impulse_at_local_point((impulse, 0), (0, 0))

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_A):
            self.create_world()

    def draw(self):
        pyxel.cls(0)

        # Draw bullets
        for bullet_shape in self.bullets:
            x, y, *_ = bullet_shape.bb
            angle = -bullet_shape.body.angle * 180 / 3.14  # radian => degree
            pyxel.blt(x, y, 1, 0, 0, 10, 10, rotate=angle)

        # Draw boxes
        for block_shape in self.shapes:
            x, y, *_ = block_shape.bb
            angle = -block_shape.body.angle * 180 / 3.14  # radian => degree
            pyxel.blt(x, y, 0, 0, 0, 10, 10, rotate=angle)

        # Draw static lines
        pyxel.line(10, 200, 240, 200, 7)
        pyxel.line(230, 200, 230, 50, 7)

        # Draw Key explanation
        pyxel.text(4, 4, "SPACE: Shot Bullet", 7)
        pyxel.text(4, 12, "A    : Reset", 7)


# メイン関数を実行
run_asyncio()
