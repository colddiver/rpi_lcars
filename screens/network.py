from subprocess import call
from datetime import datetime
import pygame
from pygame.mixer import Sound

from ui.utils.loadinfo import *
from ui.colours import randomcolor

from ui import colours
from ui.widgets.background import LcarsBackgroundImage
from ui.widgets.lcars_widgets import LcarsText, LcarsButton
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.screen import LcarsScreen

class ScreenNetwork(LcarsScreen):
    def setup(self, all_sprites):
        # Load BG image
        all_sprites.add(LcarsBackgroundImage("assets/lcars_bg.png"), layer=0)

        # Time/Date display
        self.stardate = LcarsText(colours.BLUE, (12, 380), "", 1.5)
        self.lastClockUpdate = 0
        all_sprites.add(self.stardate, layer=1)

        # Static text
        all_sprites.add(LcarsText(colours.BLACK, (8, 40), "LCARS 1123"), layer=1)
        all_sprites.add(LcarsText(colours.ORANGE, (0, 135), "NETWORK STATUS", 2), layer=1)

        # Interfaces
        all_sprites.add(LcarsButton(colours.RED_BROWN, "btn", (6, 660), "MAIN", self.logoutHandler), layer=2)
        all_sprites.add(LcarsButton(randomcolor(), "nav", (145, 15), "LAN", self.display_lan), layer=2)
        all_sprites.add(LcarsButton(randomcolor(), "nav", (200, 15), "INTERNET", self.display_internet), layer=2)
        all_sprites.add(LcarsButton(randomcolor(), "nav", (255, 15), "SERVER", self.nullfunction), layer=2)
        all_sprites.add(LcarsButton(randomcolor(), "nav", (310, 15), "", self.nullfunction), layer=2)
        all_sprites.add(LcarsButton(randomcolor(), "nav", (365, 15), "", self.nullfunction), layer=2)

        all_sprites.add(LcarsButton(randomcolor(), "btn", (140, 660), "ROUTERS", self.display_lan), layer=3)
        all_sprites.add(LcarsButton(randomcolor(), "btn", (200, 660), "PRINTERS", self.display_printers), layer=3)
        all_sprites.add(LcarsButton(randomcolor(), "btn", (260, 660), "SENSORS", self.display_sensors), layer=3)
        self.lan_buttons = all_sprites.get_sprites_from_layer(3)

        # Pull in information
        self.loadfile(all_sprites, "routers", 4)
        self.loadfile(all_sprites, "sites", 5)
        self.toggle_sprites(self.sites, False)
        self.loadfile(all_sprites, "sensors", 6)
        self.toggle_sprites(self.sensors, False)
        self.loadfile(all_sprites, "printers", 7)
        self.toggle_sprites(self.printers, False)

        # SFX
        self.beep1 = Sound("assets/audio/panel/201.wav")
        Sound("assets/audio/hail_2.wav").play()

    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.lastClockUpdate > 1000:
            self.stardate.setText("{}".format(datetime.now().strftime("%a %b %d, %Y - %X")))
            self.lastClockUpdate = pygame.time.get_ticks()
        LcarsScreen.update(self, screenSurface, fpsClock)

    def handleEvents(self, event, fpsClock):
        LcarsScreen.handleEvents(self, event, fpsClock)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.beep1.play()

        if event.type == pygame.MOUSEBUTTONUP:
            return False

    def loadfile(self, all_sprites, target, layer):
        # Load data from file
        returnpayload = read_txt("/opt/local/var/lib/lcars/" + target)

        # Router heading
        all_sprites.add(LcarsText(colours.ORANGE, (140, 175), returnpayload[0].split(',')[0], 2), layer = layer)
        all_sprites.add(LcarsText(colours.ORANGE, (140, 400), returnpayload[0].split(',')[1].lstrip(), 2), layer = layer)

        # Loop through results
        index = 1
        ypos = 200
        while index < len(returnpayload):
            all_sprites.add(LcarsText(colours.BLUE, (ypos, 175), returnpayload[index].split(',')[0], 2), layer = layer)
            # Change color based on status
            if returnpayload[index].lstrip().split(',')[1].lstrip() == "ONLINE":
                all_sprites.add(LcarsText(colours.GREEN, (ypos, 400), "ONLINE", 2), layer = layer)
            else:
                all_sprites.add(LcarsText(colours.RED, (ypos, 400), "OFFLINE", 2), layer = layer)

            # Bump index and vertical pos
            index += 1
            ypos += 50

        # Add a little flair
        all_sprites.add(LcarsGifImage("assets/animated/fwscan.gif", (320, 556), 100), layer = layer)

        # Save layer, this is a hack
        if target == "routers":
            self.routers = all_sprites.get_sprites_from_layer(layer)
        elif target == "sensors":
            self.sensors = all_sprites.get_sprites_from_layer(layer)
        elif target == "sites":
            self.sites = all_sprites.get_sprites_from_layer(layer)
        elif target == "printers":
            self.printers = all_sprites.get_sprites_from_layer(layer)

    # Button functions
    def display_lan(self, item, event, clock):
        self.toggle_sprites(self.routers, True)
        self.toggle_sprites(self.lan_buttons, True)
        self.toggle_sprites(self.sites, False)
        self.toggle_sprites(self.sensors, False)
        self.toggle_sprites(self.printers, False)

    def display_sensors(self, item, event, clock):
        self.toggle_sprites(self.routers, False)
        self.toggle_sprites(self.sites, False)
        self.toggle_sprites(self.sensors, True)
        self.toggle_sprites(self.printers, False)
        self.toggle_sprites(self.lan_buttons, True)

    def display_printers(self, item, event, clock):
        self.toggle_sprites(self.routers, False)
        self.toggle_sprites(self.sites, False)
        self.toggle_sprites(self.sensors, False)
        self.toggle_sprites(self.printers, True)
        self.toggle_sprites(self.lan_buttons, True)

    def display_internet(self, item, event, clock):
        self.toggle_sprites(self.routers, False)
        self.toggle_sprites(self.sites, True)
        self.toggle_sprites(self.sensors, False)
        self.toggle_sprites(self.printers, False)
        self.toggle_sprites(self.lan_buttons, False)

    def toggle_sprites(self, object, status):
        for sprite in object:
            sprite.visible = status

    def nullfunction(self, item, event, clock):
        print("I am a fish.")

    def logoutHandler(self, item, event, clock):
        from screens.main import ScreenMain
        self.loadScreen(ScreenMain())
