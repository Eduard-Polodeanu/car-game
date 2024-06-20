

class Button():
	def __init__(self, image, position, text, font, color, hover_color):
		self.image = image
		self.x, self.y = position[0], position[1]
		self.font = font
		self.color, self.hover_color = color, hover_color
		self.text = text

		self.text_render = self.font.render(self.text, True, self.color)
		if self.image is None:
			self.image = self.text_render
		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.text_rect = self.text_render.get_rect(center=(self.x, self.y))


	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text_render, self.text_rect)

	def check_for_click(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def change_color_hover(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text_render = self.font.render(self.text, True, self.hover_color)
		else:
			self.text_render = self.font.render(self.text, True, self.color)