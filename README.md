# LooneyTunes Menu Board
Displays a themed menu

## Installation
### Install requirements
- pillow: `pip install Pillow`
- tkinter: `sudo apt-get install python-tk`
### Clone repository
    git clone https://github.com/rscarson/looneytunes-menu.git
### Configure and start
    cp config.json.default config.json
    chmod +x start.sh
    ./start.sh
    
## Configuration
The menu entries are located in the 'images' section of the config, and consists of comma separated sections like this one:

    {
    	"character" : "bugs",
    	"name": "Carrot Juice", 
    	"ingredients": "Ginger Beer, Vodka, Carrot Juice, Lime, Angostura Bitters",
    	"price": "$2.75",
    	"available": true
    }
    
The options available are:
- **character**: the character icon to display next to the item; a full list can be found below
- **name**: The name of the menu item
- **ingredients**: The ingredients list to display
- **price**: The displayed price.
- **available**: true to display the item, false to ignore it. Use this to remove a menu item without having to delete it.

### Available character icons
<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/bugs.png" width="100" height="100"/>
  <em>bugs</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/coyote.png" width="100" height="100"/>
  <em>coyote</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/daffy.png" width="100" height="100"/>
  <em>daffy</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/elmer.png" width="100" height="100"/>
  <em>elmer</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/foghorn.png" width="100" height="100"/>
  <em>foghorn</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/frog.png" width="100" height="100"/>
  <em>frog</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/lola.png" width="100" height="100"/>
  <em>lola</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/marvin.png" width="100" height="100"/>
  <em>marvin</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/pepe.png" width="100" height="100"/>
  <em>pepe</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/porky.png" width="100" height="100"/>
  <em>porky</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/roadrunner.png" width="100" height="100"/>
  <em>roadrunner</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/speedy.png" width="100" height="100"/>
  <em>speedy</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/sylvester.png" width="100" height="100"/>
  <em>sylvester</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/taz.png" width="100" height="100"/>
  <em>taz</em>
</p>

<p>
  <img src="https://github.com/rscarson/looneytunes-menu/raw/master/logos_1080p/tweety.png" width="100" height="100"/>
  <em>tweety</em>
</p>
