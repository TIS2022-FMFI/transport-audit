from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from pyzbar import pyzbar
import webbrowser
import cv2

from PIL import Image as Im2

kod = []

from random import randint
class Scanner(Screen):

    def __init__(self, screenManager, kody, povodnaScreen, dalsiaScreen, **kwargs):
        super().__init__(**kwargs)
        self.prveSpustenie = True
        self.i = 0
        self.screenManager = screenManager
        self.kody = kody
        self.najdene = None
        self.povodnaScreen = povodnaScreen
        self.dalsiaScreen = dalsiaScreen

        self.orientation = 'vertical'  # vertical placing of widgets

        self.cam = None
        self.img = Image(size_hint_y = 0.6, size_hint_x = 1, pos_hint = {'center_y': 0.65})
        self.skenovat = True
        self.bind(on_enter=self.zapnutieKamery)

        self.butSpat = Button(text='Späť', size_hint_y=None, height='48dp', on_press=self.spat, pos_hint = {'center_y':0.05})
        self.add_widget(self.img)

        self.add_widget(self.butSpat)
        Clock.schedule_interval(self.update, 1.0 / 30)

    #__events__ = ('on_enter')

    def zapnutieKamery(self, *args):

        if self.prveSpustenie:
            self.prveSpustenie = False

            return
        #self.skenovat = True
        

        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 1280)
        self.cam.set(4, 720)

    def update(self, dt):

        if self.cam is None:
            return
        ret, frame = self.cam.read()
        if not self.skenovat:
            return


        if ret:
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = image_texture  # display image from the texture

            #barcodes = pyzbar.decode(Im2.open(image))  # detect barcode from image (frame)
            barcodes = pyzbar.decode(frame)  # detect barcode from image
            self.pouzitKod(str(randint(100, 1000)))
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                barcodeData = barcode.data.decode("utf-8")
                if barcode.type == 'QRCODE':

                    continue
                #text = "{} ({})".format(barcodeData, barcode.type)
                #cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                self.pouzitKod(barcodeData)




    def pouzitKod(self, kod):
        self.skenovat = False
        self.najdene = kod

        self.butPouzit = Button(text=f'{kod}', size_hint_y=None, height='48dp', on_press=self.koniec,
                                pos_hint={'center_y': 0.15})
        self.add_widget(self.butPouzit)
        self.butNove = Button(text=f'skenovat dalej', size_hint_y=None, height='48dp', on_press=self.pokracovat,
                              pos_hint={'center_y': 0.25})
        self.add_widget(self.butNove)

    def pokracovat(self, *args):
        self.skenovat = True
        self.i = (self.i+1)%2
        self.remove_widget(self.butNove)
        self.remove_widget(self.butPouzit)

    def spat(self, *args):
        self.cam.release()
        self.cam = None

        self.screenManager.current = self.povodnaScreen
    def koniec(self, *args):
        self.kody.clear()
        self.kody.append(self.najdene)
        self.cam.release()
        self.cam = None
        self.screenManager.current = self.dalsiaScreen




