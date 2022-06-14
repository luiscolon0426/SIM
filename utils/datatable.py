from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class ClassNameWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ClassNameApp(App):
    def build(self):
        return ClassNameWindow()

if __name__=='__main__':
    ClassNameApp()run()
