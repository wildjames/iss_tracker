import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
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

lcd_rs = digitalio.DigitalInOut(rs)
lcd_en = digitalio.DigitalInOut(en)
lcd_d7 = digitalio.DigitalInOut(d7)
lcd_d6 = digitalio.DigitalInOut(d6)
lcd_d5 = digitalio.DigitalInOut(d5)
lcd_d4 = digitalio.DigitalInOut(d4)
lcd_backlight = digitalio.DigitalInOut(A)

lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_Mono(
    lcd_rs, lcd_en,
    lcd_d4, lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows,
    lcd_backlight)


lcd.display = True
lcd.message("Hello\nWorld!!")
time.sleep(10)
