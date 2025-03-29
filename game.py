import raylibpy as rl
import random
import time
import threading
import cv2
from utils import Finger_counter

s = 7
finger_count = 0  # Shared variable

def finger_tracking():
    global finger_count
    cap = cv2.VideoCapture(0)
    counter = Finger_counter()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        _, count = counter.count_fingers(frame)
        finger_count = count

        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

class Position:
    POSITION_1, POSITION_2, POSITION_3 = range(3)

class Position1:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Position2(Position1):
    pass

class Position3(Position1):
    pass

class Pole1:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

class Pole2_1(Pole1):
    pass

class Pole2_2(Pole1):
    pass

class Pole3(Pole1):
    pass

def main():
    global finger_count
    score = 0
    last_score_update_time = time.time()
    threading.Thread(target=finger_tracking, daemon=True).start()
    time.sleep(1)  # Allow camera to warm up

    random.seed(time.time())
    position = Position.POSITION_1
    width = 16 * 100
    height = 9 * 100

    rl.init_window(width, height, "fingers-number-game")
    rl.init_audio_device()  # Initialize audio device
    bgm = rl.load_music_stream(r"C:\programs\python\OPENcv\fingers-number-game\bgm.mp3")
    rl.play_music_stream(bgm)

    rl.set_target_fps(60)

    image_bg = rl.load_image(r"C:\programs\python\OPENcv\fingers-number-game\bg.png")
    background = rl.load_texture_from_image(image_bg)

    image_eagle = rl.load_image(r"C:\programs\python\OPENcv\fingers-number-game\e.png")
    eagle = rl.load_texture_from_image(image_eagle)
    image_butterfly = rl.load_image(r"C:\programs\python\OPENcv\fingers-number-game\b.png")
    butterfly = rl.load_texture_from_image(image_butterfly)
    image_snake = rl.load_image(r"C:\programs\python\OPENcv\fingers-number-game\s.png")
    snake = rl.load_texture_from_image(image_snake)

    position2 = Position2(210 + 250, height // 2 - (height // 10) // 2 - 30, 160, height // 10)
    position3 = Position3(210 + 250, height - 70 - height // 10, 314, height // 10)

    pole1 = Pole1(width, 230, 150, height - 230, s)
    pole2_1 = Pole2_1(width, 0, 150, height // 2 - 100, s)
    pole2_2 = Pole2_2(width, height // 2 + 100, 150, height - (height // 2 - 100), s)
    pole3 = Pole3(width, 0, 150, height - 230, s)

    current_pole = random.randint(1, 3)
    game_over = False
    game_started = False

    while not rl.window_should_close():
        rl.update_music_stream(bgm)  # Update the music stream

        

        if not game_started:
            
            rl.begin_drawing()
            rl.clear_background(rl.RAYWHITE)
            rl.draw_texture(background, 0, 0, rl.WHITE)
            rl.draw_text("Raise 5 fingers to Start", width // 2 - 200, height // 2, 40, rl.DARKGRAY)
            score = 0
            rl.end_drawing()

            

            if finger_count == 5:
                game_started = True
                game_over = False
                pole1.x = pole2_1.x = pole2_2.x = pole3.x = width
                current_pole = random.randint(1, 3)
            continue

        if game_over:
            rl.begin_drawing()
            rl.clear_background(rl.RAYWHITE)
            rl.draw_texture(background, 0, 0, rl.WHITE)
            rl.draw_text("Game Over!", width // 2 - 100, height // 2 - 40, 40, rl.RED)
            rl.draw_text("Raise 4 fingers to Restart", width // 2 - 220, height // 2 + 40, 40, rl.DARKGRAY)
            rl.end_drawing()

            if finger_count == 4:
                game_started = False
            continue

        # Finger-controlled position switching
        if finger_count == 1:
            position = Position.POSITION_1
        elif finger_count == 2:
            position = Position.POSITION_2
        elif finger_count == 3:
            position = Position.POSITION_3

        if current_pole == 1:
            pole1.x -= pole1.speed
            if pole1.x + pole1.width < 0:
                pole1.x = width
                current_pole = random.randint(1, 3)
        elif current_pole == 2:
            pole2_1.x -= pole2_1.speed
            pole2_2.x -= pole2_2.speed
            if pole2_1.x + pole2_1.width < 0 and pole2_2.x + pole2_2.width < 0:
                pole2_1.x = pole2_2.x = width
                current_pole = random.randint(1, 3)
        elif current_pole == 3:
            pole3.x -= pole3.speed
            if pole3.x + pole3.width < 0:
                pole3.x = width
                current_pole = random.randint(1, 3)

        if game_started:
            current_time = time.time()
            if current_time - last_score_update_time >= 1:  # Check if 1 second has passed
                score += 1
                last_score_update_time = current_time


        if position == Position.POSITION_1:
            player_rect = rl.Rectangle(210+250, 70, 229, height // 10)
        elif position == Position.POSITION_2:
            player_rect = rl.Rectangle(position2.x, position2.y, position2.width, position2.height)
        elif position == Position.POSITION_3:
            player_rect = rl.Rectangle(position3.x, position3.y, position3.width, position3.height)

        if current_pole == 1:
            if rl.check_collision_recs(player_rect, rl.Rectangle(pole1.x, pole1.y, pole1.width, pole1.height)):
                game_over = True
        elif current_pole == 2:
            if (rl.check_collision_recs(player_rect, rl.Rectangle(pole2_1.x, pole2_1.y, pole2_1.width, pole2_1.height)) or
                rl.check_collision_recs(player_rect, rl.Rectangle(pole2_2.x, pole2_2.y, pole2_2.width, pole2_2.height))):
                game_over = True
        elif current_pole == 3:
            if rl.check_collision_recs(player_rect, rl.Rectangle(pole3.x, pole3.y, pole3.width, pole3.height)):
                game_over = True

        
        

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        rl.draw_texture(background, 0, 0, rl.WHITE)

        if position == Position.POSITION_1:
            rl.draw_texture(eagle, 210 + 250, 70, rl.WHITE)  # Shift x by +60
        elif position == Position.POSITION_2:
            rl.draw_texture(butterfly, 210 + 250, height // 2 - (height // 10) // 2 - 30, rl.WHITE)  # Shift x by +60
        elif position == Position.POSITION_3:
            rl.draw_texture(snake, 210 + 250, height - 70 - height // 10, rl.WHITE)  # Shift x by +60

        if current_pole == 1:
            rl.draw_rectangle(pole1.x, pole1.y, pole1.width, pole1.height, rl.DARKBLUE)
        elif current_pole == 2:
            rl.draw_rectangle(pole2_1.x, pole2_1.y, pole2_1.width, pole2_1.height, rl.DARKBLUE)
            rl.draw_rectangle(pole2_2.x, pole2_2.y, pole2_2.width, pole2_2.height, rl.DARKBLUE)
        elif current_pole == 3:
            rl.draw_rectangle(pole3.x, pole3.y, pole3.width, pole3.height, rl.DARKBLUE)

        rl.draw_text(f"Score : {score}", width -300, 50, 40, rl.RED)

        rl.end_drawing()

    rl.stop_music_stream(bgm)
    rl.unload_music_stream(bgm)
    rl.close_audio_device()  # Close audio device
    rl.unload_texture(background)
    rl.unload_image(image_bg)
    rl.unload_texture(eagle)
    rl.unload_image(image_eagle)
    rl.unload_texture(butterfly)
    rl.unload_image(image_butterfly)
    rl.unload_texture(snake)
    rl.unload_image(image_snake)

    rl.close_window()

if __name__ == "__main__":
    main()
