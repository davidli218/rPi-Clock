"""
Raspberry Pi Clock
A multi functional LED display clock built by Raspberry Pi.

Date:2020/08/11 David Li <david_ri@163.com>
"""

import RPi.GPIO as GPIO
import time

SYS_NAME = "Raspberry Pi Clock"
SYS_VERSION = "0.15"

SYS_TOTAL_TASK = 2
SYS_INTERRUPT = False
SYS_TASK_MODE = 0


def sys_interrupt(_):
    """Interrupt the task on main thread"""
    global SYS_INTERRUPT
    SYS_INTERRUPT = True


def task_switcher():
    """Switch the task on main thread"""
    global SYS_TASK_MODE, SYS_INTERRUPT

    SYS_TASK_MODE = (SYS_TASK_MODE + 1) % SYS_TOTAL_TASK
    SYS_INTERRUPT = False

    if SYS_TASK_MODE == 0:
        Clock(digits, segments, nums, buttons[1])
    elif SYS_TASK_MODE == 1:
        Timer(digits, segments, nums, buttons[1])


def display_7seg(txt: str, digs, segs, ns):
    """Display content on the screen"""
    dec_pt = segs[-1]

    dis_nums = txt.replace('.', '')

    dis_pts = []
    tmp = 0
    for i in txt:
        if i == '.':
            tmp = 0
            dis_pts.append(True)
        elif tmp == 1:
            dis_pts.append(False)
        else:
            tmp += 1
    if len(dis_pts) == 3:
        dis_pts.append(False)

    for dig_i in range(4):
        for seg_i in range(7):
            GPIO.output(segs[seg_i], ns[dis_nums[dig_i]][seg_i])
        GPIO.output(dec_pt, 0 if dis_pts[dig_i] else 1)

        GPIO.output(digs[dig_i], 1)
        time.sleep(0.001)
        GPIO.output(digs[dig_i], 0)


class Clock:
    """Clock mode"""
    current_status = 0
    total_status = 2

    def __init__(self, digs, segs, ns, ctrl_but):
        GPIO.add_event_detect(ctrl_but, GPIO.RISING, callback=self.next_mode, bouncetime=200)

        self.digs = digs
        self.segs = segs
        self.ns = ns

        while not SYS_INTERRUPT:
            self.time_mode()
            self.date_mode()

        GPIO.remove_event_detect(ctrl_but)

    def time_mode(self):
        while not SYS_INTERRUPT and self.current_status == 0:
            now = time.ctime()[11:19]  # Current time
            now = now[:2] + ('' if int(now[-2:]) % 2 else '.') + now[3:5]  # Display form
            display_7seg(now, self.digs, self.segs, self.ns)

    def date_mode(self):
        while not SYS_INTERRUPT and self.current_status == 1:
            date = time.strftime("%m.%d", time.localtime())  # Current date
            display_7seg(date, self.digs, self.segs, self.ns)

    def next_mode(self, _):
        self.current_status = (self.current_status + 1) % self.total_status


class Timer:
    """Timer mode"""
    current_status = 0
    total_status = 3

    def __init__(self, digs, segs, ns, ctrl_but):
        GPIO.add_event_detect(ctrl_but, GPIO.RISING, callback=self.next_status, bouncetime=200)

        while not SYS_INTERRUPT:
            '''Waiting for start'''
            for seg_i in range(7):
                GPIO.output(segs[seg_i], ns['0'][seg_i])

            while not SYS_INTERRUPT and self.current_status == 0:
                if time.time() % 1 * 100 > 50:
                    display_7seg('00.00', digs, segs, ns)
                else:
                    time.sleep(0.1)

            '''Start'''
            time_start = time.time()

            while not SYS_INTERRUPT and self.current_status == 1:
                display_7seg(self.time_display_form(time.time() - time_start), digs, segs, ns)

            '''Result'''
            time_total = time.time() - time_start

            while not SYS_INTERRUPT and self.current_status == 2:
                if time.time() % 2 > 0.8:
                    display_7seg(self.time_display_form(time_total), digs, segs, ns)
                else:
                    time.sleep(0.1)

        GPIO.remove_event_detect(ctrl_but)

    @staticmethod
    def time_display_form(s):
        if s < 100:
            return f'{s:05.2f}'
        elif s < 6000:
            return f'{s // 60:02.0f}.{s % 60:02.0f}.'
        else:
            return 'Err.0'  # Time out

    def next_status(self, _):
        self.current_status = (self.current_status + 1) % self.total_status


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    '''
    GPIO.BCM ports for the 7seg pins

    ┌──0──┐
    3     4
    ├──1──┤
    5     6
    └──2──┘  7
    '''
    segments = (5, 6, 13, 19, 26, 16, 12, 20)

    '''
    GPIO.BCM ports for the digit 0-3 pins
    
    ┌───┐ ┌───┐ ┌───┐ ┌───┐
    ├ 0 ┤ ├ 1 ┤ ├ 2 ┤ ├ 3 ┤
    └───┘ └───┘ └───┘ └───┘
    '''
    digits = (18, 27, 22, 23)

    buttons = [24, 25]

    buzzer = 21

    nums = {' ': (1, 1, 1, 1, 1, 1, 1),
            '0': (0, 1, 0, 0, 0, 0, 0),
            '1': (1, 1, 1, 1, 0, 1, 0),
            '2': (0, 0, 0, 1, 0, 0, 1),
            '3': (0, 0, 0, 1, 0, 1, 0),
            '4': (1, 0, 1, 0, 0, 1, 0),
            '5': (0, 0, 0, 0, 1, 1, 0),
            '6': (0, 0, 0, 0, 1, 0, 0),
            '7': (0, 1, 1, 1, 0, 1, 0),
            '8': (0, 0, 0, 0, 0, 0, 0),
            '9': (0, 0, 0, 0, 0, 1, 0),
            'E': (0, 0, 0, 0, 1, 0, 1),
            'r': (1, 0, 1, 1, 1, 0, 1)}

    GPIO.setup(digits, GPIO.OUT, initial=0)  # 0 Dark, 1 Light
    GPIO.setup(segments, GPIO.OUT, initial=1)  # 1 Dark, 0 Light
    GPIO.setup(buttons, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Pull down
    GPIO.setup(buzzer, GPIO.OUT)

    GPIO.add_event_detect(buttons[0], GPIO.RISING, callback=sys_interrupt, bouncetime=200)

    try:
        while True:
            Clock(digits, segments, nums, buttons[1])
            if GPIO.event_detected(buttons[0]):
                task_switcher()

    finally:
        GPIO.cleanup()
