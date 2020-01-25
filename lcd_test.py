import Adafruit_CharLCD as LCD
import time

rs = 9
en = 11

d4 = 17
d5 = 27
d6 = 22
d7 = 10

A  = 14

lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(
    rs, en,
    d4, d5, d6, d7,
    lcd_columns, lcd_rows,
    A
)


print("Sending hello...")
lcd.set_backlight(1)
lcd.message("Hello\nWorld!!")
time.sleep(10)

