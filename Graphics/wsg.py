import arcade
from csv import reader
from arcade.window_commands import pause
import pandas as pd
import numpy as np
 
ROW_COUNT = 51
COLUMN_COUNT = 51
WIDTH = 15
HEIGHT = 15
 
SCREEN_WIDTH = WIDTH * COLUMN_COUNT
SCREEN_HEIGHT = HEIGHT * ROW_COUNT
SCREEN_TITLE = "Wolves-Sheep-Grass"

class MyGame(arcade.Window):
	
	def __init__(self, width, height, title):
		super().__init__(width, height, title)
		self.grid = []
		for row in range(ROW_COUNT):
			self.grid.append([])
			for column in range(COLUMN_COUNT):
				self.grid[row].append(0)
		arcade.set_background_color(arcade.color.BLACK)
		self.grid_sprite_list = arcade.SpriteList()
		for row in range(ROW_COUNT):
			for column in range(COLUMN_COUNT):
				x = column * WIDTH + WIDTH/2
				y = row * HEIGHT + WIDTH/2
				sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
				sprite.center_x = x
				sprite.center_y = y
				self.grid_sprite_list.append(sprite)
		self.df = pd.read_csv("wsg.csv", header = 0)
		self.ticks = [y.values.tolist() for x, y in self.df.groupby('Time', as_index=False)]
		self.time = 0
		self.inum = 0

	def on_draw(self):
		arcade.start_render()
		self.grid_sprite_list.draw()
		last = len(self.grid_sprite_list)

		for i in range(0, last):
			sp = self.grid_sprite_list[last - i - 1]
			self.grid_sprite_list.remove(sp)
		for row in range(ROW_COUNT):
			for column in range(COLUMN_COUNT):
				x = column * WIDTH + WIDTH/2
				y = row * HEIGHT + WIDTH/2
				sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
				sprite.center_x = x
				sprite.center_y = y
				self.grid_sprite_list.append(sprite)
		image = arcade.draw_commands.get_image(x=0, y=0, width=None, height=None)
		image.save('screenshot' + str(self.inum) + '.png', 'PNG')
		self.inum = self.inum + 1
		if self.time > 400:
			pause(300)

	def on_update(self, delta_time: float):
		agent = 0
		try:
			for row in range(ROW_COUNT):
				for column in range(COLUMN_COUNT):
					pos = row * COLUMN_COUNT + column
					if self.ticks[self.time][agent][1] == 'grass' and int(self.ticks[self.time][agent][2]) == row and int(self.ticks[self.time][agent][3]) == column:
						self.grid_sprite_list[pos].color = arcade.color.GREEN
						agent = agent + 1
					else:
						self.grid_sprite_list[pos].color = arcade.color.BROWN

			for i in range(agent, len(self.ticks[self.time])):		
				if self.ticks[self.time][i][1] == 'sheep':
					self.player_sprite = arcade.Sprite("sheep.png", .08)
					self.player_sprite.center_x = float(self.ticks[self.time][i][2]) * WIDTH
					self.player_sprite.center_y = float(self.ticks[self.time][i][3]) * HEIGHT
					self.grid_sprite_list.append(self.player_sprite)
				elif self.ticks[self.time][i][1] == 'wolf':
					self.player_sprite = arcade.Sprite("wolf.png", .2)
					self.player_sprite.center_x = float(self.ticks[self.time][i][2]) * WIDTH
					self.player_sprite.center_y = float(self.ticks[self.time][i][3]) * HEIGHT
					self.grid_sprite_list.append(self.player_sprite)
				else:
					print('Bad data!')
		except IndexError:
			pass
			
		
		self.time = self.time + 1
			
		return super().on_update(delta_time)
   
def main():
	MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	arcade.run()


if __name__ == "__main__":
	main()