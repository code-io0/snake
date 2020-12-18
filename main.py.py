import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox
from pygame.locals import *
from pygame.math import Vector2

class Food:
	def __init__(self):
		self.randomize()

	def draw_food(self, win):
		food_rect = pygame.Rect(self.pos.x * BOX_SIZE, self.pos.y * BOX_SIZE, BOX_SIZE, BOX_SIZE)
		pygame.draw.rect(win, self.color, food_rect)

	def randomize(self):
		self.x = random.randint(0, BOX_NUM-1)
		self.y = random.randint(0, BOX_NUM-1)
		self.pos = Vector2(self.x,self.y)
		self.color = random.choice(COLORS)


class Snake:
	def __init__(self):
		self.body = [Vector2(5,6),Vector2(4,6),Vector2(3,6)]
		self.direction = Vector2(1,0)
		self.snack = False

	def draw_snake(self, win):
		for index,block in enumerate(self.body):
			if index == 0:
				color = WHITE
			else:
				color = RED
			block_rect = pygame.Rect(block.x * BOX_SIZE, block.y * BOX_SIZE, BOX_SIZE, BOX_SIZE)
			pygame.draw.rect(win, color, block_rect)

	def move_snake(self):
		if not self.snack:
			body_copy = self.body[:-1]
			body_copy.insert(0, body_copy[0] + self.direction)
			self.body = body_copy
		else:
			body_copy = self.body[:]
			body_copy.insert(0, body_copy[0] + self.direction)
			self.body = body_copy
			self.snack = False

	def snack_eaten(self):
		self.snack = True


class Game:
	def __init__(self):
		self.snake = Snake()
		self.food = Food()

	def draw_elements(self, win):
		self.draw_grid()
		self.snake.draw_snake(win)
		self.food.draw_food(win)

	def update(self):
		self.snake.move_snake()
		self.eat_snack()
		self.check_collision()

	def eat_snack(self):
		if self.food.pos == self.snake.body[0]:
			crunch_sound.play()
			self.snake.snack_eaten()
			self.food.randomize()

	def check_collision(self):
		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()

		if not -1 <= self.snake.body[0].x <= BOX_NUM or not -1 <= self.snake.body[0].y <= BOX_NUM:
			self.game_over()

	def game_over(self):
		self.message_box("You lost", f"You got {len(self.snake.body)-3} Play again!!")
		self.snake.body = [Vector2(5,6),Vector2(4,6),Vector2(3,6)]
		self.snake.direction = Vector2(1,0)
		self.food.randomize()

	@staticmethod
	def draw_grid():
		for x in range(BOX_NUM):
			for y in range(BOX_NUM):
				grid_rect = pygame.Rect(x * BOX_SIZE, y * BOX_SIZE, BOX_SIZE, BOX_SIZE)
				pygame.draw.rect(screen, GRAY, grid_rect, 1)

	@staticmethod
	def message_box(subject ,message):
		root = tk.Tk()
		root.attributes("-topmost",True)
		root.withdraw()
		messagebox.showinfo(subject, message)
		root.destroy()

pygame.init()
BOX_SIZE, BOX_NUM = 30, 20
WIDTH = BOX_SIZE * BOX_NUM
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()


RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (128,128,128)
YELLOW = (255,255,0)
BLACK = (0,0,0)

COLORS = [RED,WHITE,RED,GREEN,YELLOW]

game = Game()

crunch_sound = pygame.mixer.Sound("sound/crunch.wav")

while True:
	clock.tick(10)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_UP:
				if game.snake.direction.y  != 1:
					game.snake.direction = Vector2(0,-1)
			if event.key == K_DOWN:
				if game.snake.direction.y  != -1:
					game.snake.direction = Vector2(0,1)
			if event.key == K_LEFT:
				if game.snake.direction.x  != 1:
					game.snake.direction = Vector2(-1,0)
			if event.key == K_RIGHT:
				if game.snake.direction.x  != -1:
					game.snake.direction = Vector2(1,0)

	screen.fill(BLACK)
	game.draw_elements(screen)
	game.update()
	pygame.display.update()