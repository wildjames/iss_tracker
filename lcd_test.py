import Adafruit_CharLCD as LCD
import time

con = 14
rs  = 15
rw  = 18
en  = 23
d0  = 24
d1  = 25
d2  = 8
d3  = 7
d4  = 1
d5  = 12
d6  = 16
d7  = 20
A   = 21

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

