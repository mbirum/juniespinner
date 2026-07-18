import pygame
import os
import RPi.GPIO as GPIO
import time
import motor_sequencer
import sys
import subprocess
import select

GPIO.setmode(GPIO.BOARD)

left_pins = [7,11,13,15]
right_pins = [11,13,15,37]
sleep_interval = 0.001

control_pins = right_pins
sequence = motor_sequencer.forward()

# max 512
rotation = 150

# initialize pins
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
if joystick_count < 1:
	print("No joystick found")
else:
	y_axis_direction = 0
	y_axis_speed_factor = 1
	x_axis_direction = 0
	x_axis_speed_factor = 1
	joystick = pygame.joystick.Joystick(0)
	joystick.init()
	print("Initialized joystick")
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.JOYBUTTONDOWN:
				print(f"Button {event.button} pressed")
				
				sequence = motor_sequencer.backward()
				for i in range(int(rotation)):
					GPIO.output(control_pins[0], sequence[0][0])
					GPIO.output(control_pins[1], sequence[0][1])
					GPIO.output(control_pins[2], sequence[0][2])
					GPIO.output(control_pins[3], sequence[0][3])

					GPIO.output(control_pins[0], sequence[1][0])
					GPIO.output(control_pins[1], sequence[1][1])
					GPIO.output(control_pins[2], sequence[1][2])
					GPIO.output(control_pins[3], sequence[1][3])

					GPIO.output(control_pins[0], sequence[2][0])
					GPIO.output(control_pins[1], sequence[2][1])
					GPIO.output(control_pins[2], sequence[2][2])
					GPIO.output(control_pins[3], sequence[2][3])

					GPIO.output(control_pins[0], sequence[3][0])
					GPIO.output(control_pins[1], sequence[3][1])
					GPIO.output(control_pins[2], sequence[3][2])
					GPIO.output(control_pins[3], sequence[3][3])

					GPIO.output(control_pins[0], sequence[4][0])
					GPIO.output(control_pins[1], sequence[4][1])
					GPIO.output(control_pins[2], sequence[4][2])
					GPIO.output(control_pins[3], sequence[4][3])

					GPIO.output(control_pins[0], sequence[5][0])
					GPIO.output(control_pins[1], sequence[5][1])
					GPIO.output(control_pins[2], sequence[5][2])
					GPIO.output(control_pins[3], sequence[5][3])

					GPIO.output(control_pins[0], sequence[6][0])
					GPIO.output(control_pins[1], sequence[6][1])
					GPIO.output(control_pins[2], sequence[6][2])
					GPIO.output(control_pins[3], sequence[6][3])

					GPIO.output(control_pins[0], sequence[7][0])
					GPIO.output(control_pins[1], sequence[7][1])
					GPIO.output(control_pins[2], sequence[7][2])
					GPIO.output(control_pins[3], sequence[7][3])
			
						
			elif event.type == pygame.JOYBUTTONUP:
				print(f"Button {event.button} released")
			elif event.type == pygame.JOYAXISMOTION and event.axis == 0:
				if event.value < 0:
					print(f"left {event.value}")
				elif event.value > 0:
					print(f"right {event.value}")
			elif event.type == pygame.JOYAXISMOTION and event.axis == 1:
				if event.value <= 0.05:
					print(f"up {event.value}")
					y_axis_direction = -1
					speed = 10 - (round(abs(event.value),1) * 10)
					if speed < 1:
						speed = 1
					elif speed > 10:
						speed = 10
					speed = speed / 1000
					sleep_interval = speed
				elif event.value >= 0.07:
					print(f"down {event.value}")
					y_axis_direction = 1
					speed = 10 - (round(abs(event.value),1) * 10)
					if speed < 1:
						speed = 1
					elif speed > 10:
						speed = 10
					speed = speed / 1000
					sleep_interval = speed
				else:
					y_axis_direction = 0
		# if y_axis_direction < 0:
		# 	sequence = motor_sequencer.forward()
		# 	for i in range(int(rotation)):
		# 		for step in range(len(sequence)):
		# 			for pin in range(4):
		# 				GPIO.output(control_pins[pin], sequence[step][pin])
		# 			time.sleep(sleep_interval)
		# elif y_axis_direction > 0:
		# 	sequence = motor_sequencer.backward()
		# 	for i in range(int(rotation)):
		# 		for step in range(len(sequence)):
		# 			for pin in range(4):
		# 				GPIO.output(control_pins[pin], sequence[step][pin])
		# 			time.sleep(sleep_interval)
