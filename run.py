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
sequence = motor_sequencer.getForwardSequence()

# max 512
rotation = 3

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
		if y_axis_direction < 0:
			sequence = motor_sequencer.getForwardSequence()
			for i in range(int(rotation)):
				for step in range(len(sequence)):
					for pin in range(4):
						GPIO.output(control_pins[pin], sequence[step][pin])
					time.sleep(sleep_interval)
		elif y_axis_direction > 0:
			sequence = motor_sequencer.getBackwardSequence()
			for i in range(int(rotation)):
				for step in range(len(sequence)):
					for pin in range(4):
						GPIO.output(control_pins[pin], sequence[step][pin])
					time.sleep(sleep_interval)
