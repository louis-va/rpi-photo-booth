#!/usr/bin/env python3
from picamera2 import Picamera2
from luma.core.interface.serial import spi
from luma.oled.device import ssd1309
from PIL import Image, ImageDraw, ImageFont
from escpos.printer import Serial
from gpiozero import Button
from signal import pause
import time

OLED_WIDTH = 128
OLED_HEIGHT = 64
IMG_SIZE = 64
COUNTDOWN_START = 5
COUNTDOWN_FRAMES = 50
FLASH_DURATION = 0.1
BLINK_DURATION = 0.1
PRINT_TEXT = "PRINTING..."
FONT_PATH = "JetBrainsMono-Bold.ttf"
FONT_SIZE_LARGE = 20
FONT_SIZE_SMALL = 16
PRINTER_DEV = "/dev/serial0"
PRINTER_BAUD = 9600
BUTTON_GPIO = 17

# Hardware Initialization
def init_oled():
    serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=8_000_000)
    return ssd1309(serial, width=OLED_WIDTH, height=OLED_HEIGHT)

def init_printer():
    return Serial(devfile=PRINTER_DEV, baudrate=PRINTER_BAUD, timeout=2, xonxoff=True)

def init_camera():
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"size": (IMG_SIZE, IMG_SIZE)}))
    picam2.start()
    return picam2

def init_button():
    button = Button(BUTTON_GPIO)
    return button

def load_fonts():
    font_large = ImageFont.truetype(FONT_PATH, FONT_SIZE_LARGE)
    font_small = ImageFont.truetype(FONT_PATH, FONT_SIZE_SMALL)
    return font_large, font_small

# Display Functions
def display_countdown(oled, img, countdown, counter, font_large, font_small):
    canvas = Image.new("1", (OLED_WIDTH, OLED_HEIGHT), 0)
    x = (OLED_WIDTH - IMG_SIZE) // 2
    y = (OLED_HEIGHT - IMG_SIZE) // 2
    canvas.paste(img, (x, y))
    draw = ImageDraw.Draw(canvas)
    draw.text((106, 18), str(countdown), font=font_large, fill=1)
    circleFill = 1 if (countdown > 2 and counter % 6 == 0 or countdown <= 2 and counter % 3 == 0 ) else 0
    draw.text((12, 18), "●", font=font_small, fill=circleFill)
    oled.display(canvas)

def display_flash(oled):
    canvas = Image.new("1", (OLED_WIDTH, OLED_HEIGHT), 1)
    oled.display(canvas)
    time.sleep(FLASH_DURATION)

def display_blink(oled):
    for fill in [0, 1, 0]:
        canvas = Image.new("1", (OLED_WIDTH, OLED_HEIGHT), fill)
        oled.display(canvas)
        time.sleep(BLINK_DURATION)
    time.sleep(1)

def display_printing(oled, font_small):
    canvas = Image.new("1", (OLED_WIDTH, OLED_HEIGHT), 0)
    draw = ImageDraw.Draw(canvas)
    draw.text((12, 18), PRINT_TEXT, font=font_small, fill=1)
    oled.display(canvas)

# Main Logic
def start_photo_process():
    # init
    oled = init_oled()
    printer = init_printer()
    picam2 = init_camera()
    font_large, font_small = load_fonts()

    try:
        # start counter
        counter = 0
        countdown = COUNTDOWN_START

        # Countdown loop
        while counter < COUNTDOWN_FRAMES:
            frame = picam2.capture_array()
            img = Image.fromarray(frame).convert("1")
            display_countdown(oled, img, countdown, counter, font_large, font_small)
            time.sleep(0.1)
            counter += 1
            if counter % 10 == 0:
                countdown -= 1

        # Flash effect
        display_flash(oled)

        # Take picture and resize for printer
        frame = picam2.capture_array()
        img = Image.fromarray(frame).resize((384,384)).convert("1")

        # Blinking effect
        display_blink(oled)

        # Printing message
        display_printing(oled, font_small)

        # Print image
        printer.image(img, impl="bitImageRaster")
        printer.text("\n\n\n")
        printer.close()

    except KeyboardInterrupt:
        print("Stopped photo process.")
    except Exception as e:
        print(e)
    finally:
        oled.clear()
        picam2.stop()
        picam2.close()

def main():
    try:
        button = init_button()
        while True:
            button.wait_for_press()
            start_photo_process()
    except KeyboardInterrupt:
        print("Stopped main process.")

if __name__ == "__main__":
    main()