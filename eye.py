import time
import random
import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

LEFT_X = 0
LEFT_Y = 1
LEFT_BLINK = 2
RIGHT_X = 3
RIGHT_Y = 4
RIGHT_BLINK = 5

X_LIMITS = (85, 95)
Y_LIMITS = (85, 95)
BLINK_LIMITS = (0, 25)

DIR_LEFT_X = 1
DIR_LEFT_Y = 1
DIR_LEFT_BLINK = 1

DIR_RIGHT_X = 1
DIR_RIGHT_Y = -1
DIR_RIGHT_BLINK = -1

BLINK_OPEN_LEFT = -12
BLINK_OPEN_RIGHT = 0
BLINK_SIDE_DELAY = 0.03

MOVE_STEP = 1
MOVE_DELAY = 0.02
BLINK_INTERVAL = (4, 12)
BLINK_SPEED = 0.003
BLINK_HOLD = 0.10

MIN_PULSE_MS = 0.5
MAX_PULSE_MS = 2.5
PERIOD_MS = 20.0

current_servo_angles = {
    LEFT_X: 90,
    LEFT_Y: 90,
    LEFT_BLINK: BLINK_OPEN_LEFT,
    RIGHT_X: 90,
    RIGHT_Y: 90,
    RIGHT_BLINK: BLINK_OPEN_RIGHT,
}

def set_servo_angle(channel, direction, angle):
    if direction == -1:
        angle = 180 - angle
    pulse_range = MAX_PULSE_MS - MIN_PULSE_MS
    pulse_width = MIN_PULSE_MS + (pulse_range * angle / 180.0)
    duty_cycle = int((pulse_width / PERIOD_MS) * 65535)
    pca.channels[channel].duty_cycle = duty_cycle

def move_servos_together(angles_dict, current_angles):
    max_steps = 0
    for ch, (_, target) in angles_dict.items():
        max_steps = max(max_steps, abs(target - current_angles[ch]))
    if max_steps == 0:
        return
    for step in range(0, max_steps + 1, MOVE_STEP):
        for ch, (direction, target) in angles_dict.items():
            start = current_angles[ch]
            if start == target:
                continue
            t = min(1.0, step / max_steps)
            new_angle = int(start + (target - start) * t)
            set_servo_angle(ch, direction, new_angle)
        time.sleep(MOVE_DELAY)
    for ch, (_, target) in angles_dict.items():
        current_angles[ch] = target

def blink_eyes(probability=1.0):
    if random.random() > probability:
        return
    left_open = BLINK_OPEN_LEFT
    right_open = BLINK_OPEN_RIGHT
    closed = BLINK_LIMITS[1]
    left_range = closed - left_open
    right_range = closed - right_open
    steps_total = max(left_range, right_range)
    if steps_total <= 0:
        return
    side_steps = int(round(BLINK_SIDE_DELAY / BLINK_SPEED))
    for step in range(0, steps_total + 1):
        left_progress = min(step, left_range) / left_range if left_range > 0 else 1.0
        left_angle = int(left_open + left_progress * left_range)
        right_step_index = max(0, step - side_steps)
        right_progress = min(right_step_index, right_range) / right_range if right_range > 0 else 1.0
        right_angle = int(right_open + right_progress * right_range)
        set_servo_angle(LEFT_BLINK, DIR_LEFT_BLINK, left_angle)
        set_servo_angle(RIGHT_BLINK, DIR_RIGHT_BLINK, right_angle)
        time.sleep(BLINK_SPEED)
    time.sleep(BLINK_HOLD)
    for step in range(steps_total, -1, -1):
        left_progress = min(step, left_range) / left_range if left_range > 0 else 1.0
        left_angle = int(left_open + left_progress * left_range)
        right_step_index = max(0, step - side_steps)
        right_progress = min(right_step_index, right_range) / right_range if right_range > 0 else 1.0
        right_angle = int(right_open + right_progress * right_range)
        set_servo_angle(LEFT_BLINK, DIR_LEFT_BLINK, left_angle)
        set_servo_angle(RIGHT_BLINK, DIR_RIGHT_BLINK, right_angle)
        time.sleep(BLINK_SPEED)

def eyes_idle_loop(get_status_func):
    last_blink_timestamp = time.time()
    next_blink = time.time() + random.uniform(*BLINK_INTERVAL)

    while True:
        is_running, is_speaking, is_thinking = get_status_func()
        if not is_running:
            break

        now = time.time()

        if is_thinking:
            new_x, new_y = random.randint(85, 95), random.randint(85, 95)
            targets = {
                LEFT_X: (DIR_LEFT_X, new_x),
                LEFT_Y: (DIR_LEFT_Y, new_y),
                RIGHT_X: (DIR_RIGHT_X, new_x),
                RIGHT_Y: (DIR_RIGHT_Y, new_y)
            }
            move_servos_together(targets, current_servo_angles)
            if random.random() < 0.3 and now - last_blink_timestamp > 0.2:
                blink_eyes(probability=1.0)
                last_blink_timestamp = time.time()
            time.sleep(random.uniform(1.0, 2.0))

        elif is_speaking:
            new_x, new_y = random.randint(85, 95), random.randint(85, 95)
            targets = {
                LEFT_X: (DIR_LEFT_X, new_x),
                LEFT_Y: (DIR_LEFT_Y, new_y),
                RIGHT_X: (DIR_RIGHT_X, new_x),
                RIGHT_Y: (DIR_RIGHT_Y, new_y)
            }
            move_servos_together(targets, current_servo_angles)
            if random.random() < 0.2 and now - last_blink_timestamp > 0.2:
                blink_eyes(probability=1.0)
                last_blink_timestamp = time.time()
            time.sleep(random.uniform(1.5, 3.0))

        else:
            new_x, new_y = random.randint(85, 95), random.randint(85, 95)
            targets = {
                LEFT_X: (DIR_LEFT_X, new_x),
                LEFT_Y: (DIR_LEFT_Y, new_y),
                RIGHT_X: (DIR_RIGHT_X, new_x),
                RIGHT_Y: (DIR_RIGHT_Y, new_y)
            }
            move_servos_together(targets, current_servo_angles)
            if now >= next_blink:
                blink_eyes(probability=1.0)
                last_blink_timestamp = time.time()
                next_blink = time.time() + random.uniform(*BLINK_INTERVAL)
            time.sleep(random.uniform(3.0, 6.0))