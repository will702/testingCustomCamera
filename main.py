import os ,certifi
from kivymd.uix.dialog import  MDDialog
#IMPORT DIALOG FROM KIVYMD
from kivymd.uix.button import MDFlatButton,MDRaisedButton
#IMPORT BUTTON FROM KIVYMD
import requests
#IMPORT APP TO INHERIT THE MAIN FUNCTION WITH App.get_running_app().function_name() or use variable from the main function like App.get_running_app().variable_name

#INITIALIZE MD APP
from kivymd.app import MDApp
#IMPORT THE KIVY.APP TO INITIALIZE OR MAKING APP
from kivymd.uix.snackbar import  Snackbar
#IMPORT LAYOUT TO ASSEMBLY THE CAMERA ,LABEL,IMAGE,BUTTON,ELSE PERFECTLY

#FOR CANVAS THAT MIRRORING CAMERA

from kivymd.uix.screen import MDScreen#IMPORT SCREEN TO BE PUT ON THE SCREEN
 #IMPORT LIBRARIES TO READ AND WRITE JSON
from kivymd.uix.list import OneLineListItem
#IMPORTING CAMERA
from kivy.lang import Builder
#IMPORTING BUILDER TO INITIALIZE KV LANGUAGE

import json
import cv2
from kivy.utils import platform
#USE UTILS TO CHECK WHETHER IT IS ANDROID OR OTHERS
from kivy.core.window import Window
#SIZING WINDOW
from kivy.uix.screenmanager import SlideTransition
#MAKING TRANSITION
if platform == 'macosx':

    Window.size = (450, 750)
    #IF YOUR DEVICE IS MACOS IT WILL BE RESIZED INTO X : 450 AND Y : 750
else:
    #OTHERS WILL BE PASSED
    pass


Builder.load_file("main.kv")
from kivy.graphics.texture import Texture
import numpy as np
from kivy.clock import Clock

#LOAD THE DESIGN LANGUAGE FILE

from kivymd.theming import  ThemeManager
#MAKING CUSTOM BUTTON
from kivy_garden.xcamera.xcamera import XCamera

class AndroidCamera(XCamera):
    camera_resolution =(640,480)
    def _camera_loaded(self, *largs):
        #MIRRORING THE CAMERA TO TEXTURE

        self.texture = Texture.create(size=np.flip(self.camera_resolution), colorfmt='rgb')
        #READ AS RGB
        self.texture_size = list(self.texture.size)

        Clock.schedule_interval(lambda df:self.canvas.ask_update(),0.1)

        #SAVE TEXTURE_SIZE AS LIST

    def on_tex(self, *l):
        # EXECUTING BELOW METHODS WHEN THE CAMERA IS USED

        if self._camera._buffer is None:
            return None

        frame = self.frame_from_buf()
        # MAKING FRAME FROM BUFFER
        self.frame_to_screen(frame)
        # PUT FRAME TO SCREEN
        super(AndroidCamera, self).on_tex(*l)

    def frame_from_buf(self):
        #MAKE A FRAME FROM BUFFER
        w, h = self.resolution
        #INITIALIZE WIDTH AND HEIGHT OF THE CAMERA
        frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((h + h // 2, w))


        frame_bgr = cv2.cvtColor(frame, 93)

        return np.rot90(frame_bgr, 3)
        #ROTATE THE FRAME 90 DEGREES

    def frame_to_screen(self, frame):
        # MAKE A FRAME TO SCREEN

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        if self.index == 1:
            # IF ON SELFIE ROTATE 180 DEGREES
            frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_180)
        # DETECTING THE EYES



        flipped = np.flip(frame_rgb, 0)
        buf = flipped.tostring()
        # CHANGE TO STRING
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')


#MAKING CUSTOM CAMERA
#CHANGED TO XCAMERA

class MyLayout(MDScreen):
    #INITIALIZE THE MAINSCREEN/PARENT FOR THE CAMERA

    pass


os.environ['SSL_CERT_FILE'] = certifi.where()


class MyApp(MDApp):
    def __init__(self,**kwargs):


        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        #INHERIT BASIC FUNCTION ON KIVYMD
        self.data = ''
        self.theme_cls.primary_palette = 'Orange'
        #MAKING THE THEME PRIMARY PALETTE TO BE ORANGE

        self.theme_cls.primary_style = 'Light'
        #CHANGE THE THEME TO LIGHT


    def build(self):

        #APP SETUP
        self.layout = MyLayout()
        #APP VALUE TO CHANGE TO SELFIE OR FRONT
        self.value = 0

        return self.layout
        #RETURNING THE LAYOUT
    def go_back(self):
        #GO BACK FROM OTHER SCREEN TO MAINSCREEN
        self.layout.ids.screen_manager.transition  = SlideTransition(direction="right")
        self.change_screen("mainscreen")
        self.layout.ids.screen_manager.transition = SlideTransition(direction="left")
    def show_dialog5(self, *args, text):
        #CHANGE DICT_KEYS TO LIST
        a = list(self.layout.ids.camera.data[text].keys())
        #SHOWING ALL THE LOGS TO THE DIALOGS
        self.dialog = MDDialog(title='RESULTS', text=f'FIRST: {self.layout.ids.camera.data[text][a[0]]}\n'
                                                     f'SECOND: {self.layout.ids.camera.data[text][a[1]]}\n'
                                                     f'THIRD: {self.layout.ids.camera.data[text][a[2]]}\n'
                                                     f'FOURTH: {self.layout.ids.camera.data[text][a[3]]}\n'
                                                     f'FIFTH: {self.layout.ids.camera.data[text][a[4]]}\n'

                               ,

                               size_hint=(0.8, 1),
                               buttons=[MDFlatButton(text='Close', on_release=self.close_dialog),
                                        MDRaisedButton(text='Delete', on_release=lambda x, item=text: self.delete(item))
                                        ])

        self.dialog.open()
        #OPEN DIALOG

    def close_dialog(self, *args):
        #CLOSE DIALOGS
        self.dialog.dismiss()

    def delete(self, *name):
        #DELETE THE TEST THAT HAD BEEN CHOSEN

        name = name[0]
        self.close_dialog()
        print(name)
        from kivymd.toast import toast
        toast('Delete Success')
        del self.layout.ids.camera.data[name]
        with open('data/date.json', 'w') as f:

            json.dump(self.layout.ids.camera.data, f)
        self.visualize_json()

    def reset(self,*args):
        self.layout.ids.label.text = ''
    def change_screen(self,text):
        #CHANGE_SCREEN TO THE SPECIFIC SCREEN THAT CAN BE WRITTEN self.change_screen("yourscreenname"),or in kv language app.change_screen("yourscreenname")
        self.layout.ids.screen_manager.current = text
    def go_friend(self):
        try:
            #it will be executed when u want to see the logs
            self.change_screen("log_list")
            if list(self.layout.ids.camera.data.keys()) == []:
                snackbar = Snackbar(text="You Haven't Test Anything Yet", duration=0.8)
                snackbar.show()
            if list(self.layout.ids.camera.data.keys()) != []:

                self.layout.ids.container.clear_widgets()
                for i in self.layout.ids.camera.data.keys():
                    isi = OneLineListItem(text=i, on_press=lambda x, item=i: self.show_dialog5(text=i))

                    self.layout.ids.container.add_widget(isi)
        except:
            pass


    def visualize_json(self,*args):


        #refresh the widget after deleting some items
        self.layout.ids.container.clear_widgets()
        if list(self.layout.ids.camera.data.keys()) != []:
            for i in self.layout.ids.camera.data.keys():
                isi = OneLineListItem(text=i, on_press=lambda x, item=i: self.show_dialog5(text=i))

                self.layout.ids.container.add_widget(isi)
                #put the widget back to the screen if there are some value in the dict
    def swap(self):

        self.value+=1
        #IF VALUE MODULO  BY 2 IS NOT 0 THEN IT CHANGED TO SELFIE
        if self.value % 2 != 0 :

            self.layout.ids.camera.index = 1
        #IF VALUE MODULO BY 2 IS 0 IT CHANGED TO FRONT CAMERA
        if self.value % 2 == 0 :
            self.layout.ids.camera.index = 0
    def requesting(self,obj,filename):






        resp = requests.post('https://tes-det.herokuapp.com/', files={'file': open(filename,'rb')})
        resp = resp.json()
        resp = resp['hasil']
        self.data+=f'\n{resp}'





    def activate(self):
        #TRIGGERING APP TO SCAN IRIS
        for i in range(5):
            self.layout.ids.camera.shoot()
        self.layout.ids.label.text =  str(self.data)



    def show_snackbar(self,text):

        self.layout.ids.label.text = text








if __name__ == '__main__':
    #PREVENT APP FROM OTHER DISRUPTION
    MyApp().run()





    # Detect the faces




# Release the VideoCapture object




