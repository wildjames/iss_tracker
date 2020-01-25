import Adafruit_CharLCD as LCD
import time

rs = 14
rw = 15
en = 18

d4 = 6
d5 = 13
d6 = 19
d7 = 26


lcd_columns = 14
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(
    rs, en,
    d4, d5, d6, d7,
    lcd_columns, lcd_rows,
)


print("Sending hello...")
lcd.message("Hello\nWorld!!")
time.sleep(10)

