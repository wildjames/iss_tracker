import Adafruit_CharLCD as LCD
import time
from gpiozero import PWMLED

# LCD pins
lcd_rs = 27
lcd_en = 22
lcd_backlight_pin = 18

lcd_d4 = 23
lcd_d5 = 24
lcd_d6 = 10
lcd_d7 = 9

lcd_columns = 16
lcd_rows = 2

back = PWMLED(lcd_backlight_pin, initial_value=1)

lcd = LCD.Adafruit_CharLCD(
    lcd_rs, lcd_en,
    lcd_d4, lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows,
)


print("Sending hello...")
lcd.message("Hello\nWorld!!")
