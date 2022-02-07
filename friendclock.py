#!/usr/bin/python3

import datetime
from pytz import timezone
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

inky_display = auto(ask_user=True, verbose=True)

WIDTH = 250
HEIGHT = 122

img = Image.new('L', (WIDTH, HEIGHT), 1)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('/home/pi/friendclock/VCR_OSD_MONO_1.001.ttf', 20)

CW, CH = draw.textsize('X', font)

# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
LIST = [
	('UTC',		'UTC'),
	('buffrr',	'America/Denver'),
	('Falci',	'Europe/Madrid'),
	('nodech',	'Asia/Tbilisi'),
	('rithvik',	'Asia/Calcutta'),
	('chikeichan',	'Asia/Hong_Kong'),
]

row = 0
for pair in LIST:
	name = pair[0]
	place = pair[1]
	tz = timezone(place)
	time = datetime.datetime.now(tz)
	m = ''
	hour = time.hour
	if name is not 'UTC':
		hour = (time.hour % 12)
		hour = 12 if hour == 0 else hour
		m = ' am' if time.hour < 12 else ' pm'
	text =  '%-11.11s%2.2s:%-2.2d%-4.4s' % (name, hour, time.minute, m)
	bg = inky_display.BLACK
	fg = inky_display.WHITE
	if m is ' am':
		bg = inky_display.WHITE
		fg = inky_display.BLACK

	draw.rectangle((2, (row * CH) + 2, WIDTH - 2, (row * CH) + 2 + CH), bg, bg)
	draw.text((2, (row * CH) + 2), text, fg, font)
	print(text)
	row += 1

inky_display.set_image(img.rotate(180))
inky_display.show()
