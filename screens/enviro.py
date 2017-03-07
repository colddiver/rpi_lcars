from subprocess import call
from datetime import datetime
import pygame
from pygame.mixer import Sound

from ui.utils.loadinfo import *
from ui.utils.converters import *

from ui.colours import randomcolor

from ui import colours
from ui.widgets.background import LcarsBackgroundImage, LcarsImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import LcarsText, LcarsButton
from ui.widgets.screen import LcarsScreen

# Need to change class name to whatever screen is to be called
class ScreenEnviro(LcarsScreen):
    def setup(self, all_sprites):
        # Load BG image
        all_sprites.add(LcarsBackgroundImage("assets/lcars_bg.png"), layer=0)

        # Time/Date display
        self.stardate = LcarsText(colours.BLUE, (12, 380), "", 1.5)
        self.lastClockUpdate = 0
        all_sprites.add(self.stardate, layer=1)

        # Static text
        all_sprites.add(LcarsText(colours.BLACK, (8, 40), "LCARS 1123"), layer=1)
        all_sprites.add(LcarsText(colours.ORANGE, (0, 135), "ENVIRONMENT", 2), layer=1)

        # Interfaces
        all_sprites.add(LcarsButton(colours.RED_BROWN, "btn", (6, 660), "MAIN", self.logoutHandler), layer=2)
        all_sprites.add(LcarsButton(randomcolor(), "nav", (145, 15), "CURRENT", self.nullfunction), layer=2)
        all_sprites.add(LcarsButton(randomcolor(), "nav", (200, 15), "TODAY", self.nullfunction), layer=2)
        all_sprites.add(LcarsButton(randomcolor(), "nav", (255, 15), "TOMORROW", self.nullfunction), layer=2)
        all_sprites.add(LcarsButton(randomcolor(), "nav", (310, 15), "WEEK", self.nullfunction), layer=2)
        all_sprites.add(LcarsButton(randomcolor(), "nav", (365, 15), "", self.nullfunction), layer=2)

        # Info text
        weather = get_weather()
        
        #"%s\nTemperature: %s\nPrecipitations %s" % (current.summary, current.temperature, current.precipProbability)
        all_sprites.add(LcarsText(colours.BLUE, (150, 300), weather.summary , 1.5), layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (200, 300), "Temperature: %s C / Feels like: %s" % (weather.temperature, weather.apparentTemperature) , 1.5), layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (250, 300), "Wind: %s KPH %s" % (weather.windSpeed, degrees_to_cardinal(weather.windBearing)) , 1.5), layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (300, 300), "Precipitations: %s" % (weather.precipProbability) , 1.5), layer=3)
        #all_sprites.add(LcarsText(colours.BLUE, (350, 300), "Type: %s / Qty: %s cm" % (weather.precipType, weather.precipAccumulation) , 1.5), layer=3)
        #all_sprites.add(LcarsText(colours.BLUE, (350, 300), "Sunset: %s / Sunrise: %s cm" % (weather.precipType, weather.precipAccumulation) , 1.5), layer=3)
        
        all_sprites.add(LcarsGifImage("assets/weather/%s.gif" % (weather.icon), (100, 144), 50), layer=1)
        
        self.info_text = all_sprites.get_sprites_from_layer(3)

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

    def hideInfoText(self):
        if self.info_text[0].visible:
            for sprite in self.info_text:
                sprite.visible = False

    def nullfunction(self, item, event, clock):
        print("I am a fish.")

    def logoutHandler(self, item, event, clock):
        from screens.main import ScreenMain
        self.loadScreen(ScreenMain())
