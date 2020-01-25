import Adafruit_CharLCD as LCD
import time

lcd_rs = 14
lcd_rw = 15
lcd_en = 18

lcd_d4 = 6
lcd_d5 = 13
lcd_d6 = 19
lcd_d7 = 26


lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(
    lcd_rs, lcd_en,
    lcd_d4, lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows,
)


print("Sending hello...")
lcd.message("Hello\nWorld!!")

lcd.message("This is a really long string I want to write to the character display")
