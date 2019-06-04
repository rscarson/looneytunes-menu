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

class MenuBoard:
	def __init__(self, config_filename):
		self.page = 0
		self.images = []

		# Load configuration
		with codecs.open(config_filename, 'r', encoding='utf8') as f:
			config = self.load_json(f.read())
			if 'remote_config' in config.keys():
				try:
					config = urllib2.urlopen(config['remote_config']).read()
					config = self.load_json(config)
				except urllib2.URLError:
					print "Error loading target URL... Stopping"
					quit()
			self.options = config['configuration']
			images = [i for i in config['images'] if i['available']]
			self.pages = self.paginate(images, self.options['items_per_page'])

		# Prepare the canvas
		self.root = Tkinter.Tk()
		self.root.attributes("-fullscreen", True)
		self.canvas = Tkinter.Canvas(self.root, bd=0, highlightthickness=0)
		self.canvas.pack(fill=Tkinter.BOTH, expand=1)

	def generate_html(self):
		""" Generate an HTML out for debug purposes """
		with codecs.open('menu_board.html', 'w', encoding='utf8') as f:
			for page in self.pages:
				f.write("<hr /><hr /><hr /><hr />")
				for drink in page:
					f.write(u"""
					<p style="font-size: 20; background: {0}"><strong>
						character: "{1}"<br/>
						name: "{2}"<br/> 
						ingredients: "{3}"<br/>
						price: "{4}"
					</strong></p>
					""".format(drink['colour'], drink['character'], drink['name'], drink['ingredients'], drink['price']))

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
		offset = 0
		for drink in page:
			offset = self.display_drink(drink, offset)

	def display_drink(self, drink, offset):
		""" Display a drink entry at the correct location """
		offset = self.add_section(offset, 
			drink['colour'], '{0}/{1}.png'.format(self.options['image_directory'], drink['character']), 
			drink['name'], drink['ingredients'], drink['price']
		)
		return offset

	def add_section(self, offset, colour, path, title, desc, price):
		""" Draw a section of the menu onto the canvas """

		# Draw the background
		self.canvas.create_rectangle(
			0, offset,
			self.options['screen_resolution'][0], offset+self.options['screen_resolution'][1]/self.options['items_per_page'],
			fill=colour, outline=colour)

		# Prepare the image, and resize it
		img = Image.open(path)
		[w, h] = img.size
		[w, h] = (
			int(w * self.options['screen_resolution'][1]/self.options['items_per_page'] / h),
			self.options['screen_resolution'][1]/self.options['items_per_page']
		)
		img = img.resize((w, h), Image.ANTIALIAS)

		# Display the image
		imgtk = ImageTk.PhotoImage(image=img)
		self.images.append(imgtk)
		self.canvas.create_image(self.options['image_padding_size'], offset, image=imgtk, anchor=Tkinter.NW)

		# Calculate the position of the text
		text_x_offset 			= 2*self.options['image_padding_size'] + w
		text_y_offset 			= offset + self.options['image_padding_size']
		text_width				= self.options['screen_resolution'][0]-text_x_offset-self.options['image_padding_size']

		# Write the drink's name
		text_y_offset = self.text_avec_shadow(text_x_offset, text_y_offset,
			text_width, title, 
			self.options['text_font_sizes'][0], self.options['text_font'], 
			colour
		) + self.options['image_padding_size']

		# Write the text's ingredients
		text_y_offset = self.text_avec_shadow(text_x_offset+self.options['image_padding_size'], text_y_offset,
			text_width, desc, 
			self.options['text_font_sizes'][1], self.options['text_font'], 
			colour
		)

		# Write the price
		self.text_avec_shadow(text_x_offset+self.options['image_padding_size'], text_y_offset,
			text_width, price, 
			self.options['text_font_sizes'][2], self.options['text_font'], 
			colour
		)

		# Return the location to draw the next section
		return offset+self.options['screen_resolution'][1]/self.options['items_per_page']

	def clear_canvas(self):
		""" Clear the canvas """
		self.canvas.delete("all")
		self.images = []

	def load_json(self, text):
		""" Load unicode JSON, removing comments """
		text = re.sub(ur'[ \t]*//[^\n]*\n', u'', text)
		return json.loads(unicode(text))

	def paginate(self, items, page_size):
		""" Split 'items' into arrays of size page_size """
		return [items[i:i + page_size] for i in xrange(0, len(items), page_size)]

	def modify_colour(self, colour, adjustment):
		""" Brighten or darken the HTML hex colour by 'adjustment' points """
		c = tuple(int(colour.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
		return '#{:02x}{:02x}{:02x}'.format(
			0xFF if (c[0]+adjustment>0xFF) else 0 if (c[0]+adjustment<0) else c[0]+adjustment, 
			0xFF if (c[1]+adjustment>0xFF) else 0 if (c[1]+adjustment<0) else c[1]+adjustment, 
			0xFF if (c[2]+adjustment>0xFF) else 0 if (c[2]+adjustment<0) else c[2]+adjustment
		)

	def text_avec_shadow(self, x, y, width, text, size, font, background_colour):
		""" Write text onto a canvas, with a border and drop shadow """
		text_font = [font, size, 'bold' if self.options['text_font_bold'] else '']

		# Shadow first, behind the other elements
		self.canvas.create_text(x+self.options['text_shadow_size'], y+self.options['text_shadow_size'], 
			fill=self.modify_colour(background_colour, -self.options['text_shadow_darkness']), 
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

		# And the white fill
		text_fill = self.canvas.create_text(x, y, text=text, fill='white', font=text_font, anchor=Tkinter.NW,
			width=width)

		# Calculate positioning
		bounds = self.canvas.bbox(text_fill)
		height = bounds[3] - bounds[1]
		return y + height + 2*self.options['text_border_size']

board = MenuBoard('config.json')
board.generate_html()
board.start()