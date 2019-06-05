# # # # Requirements # # # #
# Displays a menu board on
# paginated rotation
# - pillow
# - tkinter
from PIL import ImageTk,Image
import urllib2
import Tkinter
import json
import time
import codecs
import re

def load_json(text):
	""" Load unicode JSON, removing comments """
	text = re.sub(ur'[ \t]*//[^\n]*\n', u'', text)
	return json.loads(unicode(text))

def rotate(l, n):
	""" Rotate a list """
	return l[n:] + l[:n]

def paginate(items, page_size):
	""" Split 'items' into arrays of size page_size """
	return [items[i:i + page_size] for i in xrange(0, len(items), page_size)]

def modify_colour(colour, adjustment):
	""" Brighten or darken the HTML hex colour by 'adjustment' points """
	c = tuple(int(colour.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
	return '#{:02x}{:02x}{:02x}'.format(
		0xFF if (c[0]+adjustment>0xFF) else 0 if (c[0]+adjustment<0) else c[0]+adjustment, 
		0xFF if (c[1]+adjustment>0xFF) else 0 if (c[1]+adjustment<0) else c[1]+adjustment, 
		0xFF if (c[2]+adjustment>0xFF) else 0 if (c[2]+adjustment<0) else c[2]+adjustment
	)

class MenuBoard:
	def __init__(self, config_filename):
		self.page = 0
		self.images = []

		# Load configuration
		with codecs.open(config_filename, 'r', encoding='utf8') as f:
			config = load_json(f.read())
			if 'remote_config' in config.keys():
				try:
					config = urllib2.urlopen(config['remote_config']).read()
					config = load_json(config)
				except urllib2.URLError:
					print "Error loading target URL... Stopping"
					quit()
			self.options = config['configuration']
			images = [i for i in config['images'] if i['available']]
			self.pages = paginate(images, self.options['items_per_page'])

		# Prepare the canvas
		self.root = Tkinter.Tk()
		self.root.attributes("-fullscreen", True)
		self.canvas = Tkinter.Canvas(self.root, bd=0, highlightthickness=0, background=self.options['background'])
		self.canvas.pack(fill=Tkinter.BOTH, expand=1)

	def start(self):
		""" Start the main loop """
		self.show_next_page()
		self.root.mainloop()

	def show_next_page(self):
		""" Display the next page, and schedule the next change """
		self.display_page(
			self.pages[self.page]
		)
		self.page = 0 if self.page+1>=len(self.pages) else self.page+1
		self.root.after(self.options['page_change_interval_ms'], lambda: self.show_next_page())

	def display_page(self, page):
		""" Display a page of drinks """
		self.clear_canvas()
		colours = self.options['colours']
		offset = 0
		for drink in page:
			offset = self.display_drink(drink, offset, colours[0])
			colours = rotate(colours, 1)

	def display_drink(self, drink, offset, colour_bg):
		""" Display a drink entry at the correct location """
		offset = self.add_section(offset, 
			colour_bg,
			'{0}/{1}.png'.format(self.options['image_directory'], drink['character']), 
			drink['name'], drink['ingredients'], drink['price']
		)
		return offset

	def add_section(self, offset, colour_bg, path, title, desc, price):
		""" Draw a section of the menu onto the canvas """

		# Calculate heights
		y2 = offset+self.options['screen_resolution'][1]/self.options['items_per_page']
		height = y2 - offset

		# Prepare the image, and resize it
		img = Image.open(path)
		[w, h] = img.size
		[w, h] = (
			int(w * self.options['screen_resolution'][1]/self.options['items_per_page'] / h),
			self.options['screen_resolution'][1]/self.options['items_per_page']
		)
		img = img.resize((w, h), Image.ANTIALIAS)

		# Calculate the position of the text
		text_x_offset 			= 2*self.options['image_padding_size'] + w
		text_y_offset 			= offset + self.options['image_padding_size']
		text_width				= self.options['screen_resolution'][0]-text_x_offset-self.options['image_padding_size']

		# Write the drink's name... test the height
		test_y_offset = self.text_avec_shadow(text_x_offset, text_y_offset,
			text_width, title, 
			self.options['text_font_sizes'][0], self.options['text_font'], 
			colour_bg, '#FFFFFF'
		)
		title_height = test_y_offset - text_y_offset

		# Draw the highlight strip
		self.canvas.create_rectangle(
			0, text_y_offset,
			self.options['screen_resolution'][0], text_y_offset + title_height,
			fill=colour_bg, outline=modify_colour(colour_bg, -self.options['text_shadow_darkness'])
		)

		# Display the image
		imgtk = ImageTk.PhotoImage(image=img)
		self.images.append(imgtk)
		self.canvas.create_image(self.options['image_padding_size'], offset, image=imgtk, anchor=Tkinter.NW)

		# Write the drink's name
		text_y_offset = self.text_avec_shadow(text_x_offset, text_y_offset,
			text_width, title, 
			self.options['text_font_sizes'][0], self.options['text_font'], 
			colour_bg, '#FFFFFF'
		) + self.options['image_padding_size']

		# Write the text's ingredients
		text_y_offset = self.text_avec_shadow(text_x_offset+self.options['image_padding_size'], text_y_offset,
			text_width, desc, 
			self.options['text_font_sizes'][1], self.options['text_font'], 
			self.options['background'], '#FFFFFF'
		)

		# Write the price
		self.text_avec_shadow(text_x_offset+self.options['image_padding_size'], text_y_offset,
			text_width, price, 
			self.options['text_font_sizes'][2], self.options['text_font'], 
			self.options['background'], '#FFFFFF'
		)

		# Return the location to draw the next section
		return offset+self.options['screen_resolution'][1]/self.options['items_per_page']

	def clear_canvas(self):
		""" Clear the canvas """
		self.canvas.delete("all")
		self.images = []

	def text_avec_shadow(self, x, y, width, text, size, font, background_colour, text_colour):
		""" Write text onto a canvas, with a border and drop shadow """
		text_font = [font, size, 'bold' if self.options['text_font_bold'] else '']

		# Shadow first, behind the other elements
		self.canvas.create_text(x+self.options['text_shadow_size'], y+self.options['text_shadow_size'], 
			fill=modify_colour(background_colour, -self.options['text_shadow_darkness']), 
			text=text, font=text_font, anchor=Tkinter.NW,
			width=width
		)

		# Draw the text border next... Start at the top left and go clockwise around the text
		self.canvas.create_text(x-self.options['text_border_size'], y+self.options['text_border_size'], 
			text=text, fill='black', font=text_font, anchor=Tkinter.NW, width=width)
		self.canvas.create_text(x, y+self.options['text_border_size'], 
			text=text, fill='black', font=text_font, anchor=Tkinter.NW, width=width)
		self.canvas.create_text(x+self.options['text_border_size'], y+self.options['text_border_size'], 
			text=text, fill='black', font=text_font, anchor=Tkinter.NW, width=width)
		self.canvas.create_text(x+self.options['text_border_size'], y, 
			text=text, fill='black', font=text_font, anchor=Tkinter.NW, width=width)
		self.canvas.create_text(x+self.options['text_border_size'], y-self.options['text_border_size'], 
			text=text, fill='black', font=text_font, anchor=Tkinter.NW, width=width)
		self.canvas.create_text(x, y-self.options['text_border_size'], 
			text=text, fill='black', font=text_font, anchor=Tkinter.NW, width=width)
		self.canvas.create_text(x-self.options['text_border_size'], y-self.options['text_border_size'], 
			text=text, fill='black', font=text_font, anchor=Tkinter.NW, width=width)
		self.canvas.create_text(x-self.options['text_border_size'], y, 
			text=text, fill='black', font=text_font, anchor=Tkinter.NW, width=width)

		# And the fill
		text_fill = self.canvas.create_text(x, y, text=text, fill=text_colour, font=text_font, anchor=Tkinter.NW,
			width=width)

		# Calculate positioning
		bounds = self.canvas.bbox(text_fill)
		height = bounds[3] - bounds[1]
		return y + height + 2*self.options['text_border_size']

board = MenuBoard('config.json')
board.start()