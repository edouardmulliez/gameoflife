from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from kivy.lang import Builder

from gameoflife import Golife

import numpy as np

Builder.load_string('''
<MyPaintBox>:
    id: box
    orientation: 'vertical'
    MyPaintWidget:
        id: painter
    Button:
        text: 'Start'
        size_hint_y: None
        height: '48dp'
        on_press: root.start()
    Button:
        text: 'Stop'
        size_hint_y: None
        height: '48dp'
        on_press: root.stop()
    Button: 
        text: 'Next'
        size_hint_y: None
        height: '48dp'
        on_press: root.next()
    Slider:
        id: speed
        value: 2
        min: 1
        max: 10
        step: 1
        value_track: True
        size_hint_y: None
        height: '48dp'
        on_value: root.update_speed()
    Slider:
        id: zoom
        value: 1
        min: 1
        max: 5
        step: 1
        value_track: True
        size_hint_y: None
        height: '48dp'
        on_value: root.update_zoom()

''')


class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Click in the paint widget
            col = int((touch.x - self.pos[0])*Golife.GRID_SIZE[1]/self.size[0])
            row = int((touch.y - self.pos[1])*Golife.GRID_SIZE[0]/self.size[1])
            self.parent.golife.add_point(row, col)
            self.parent.refresh()

    def draw_shape(self, shape):
        """
        Shape should be a numpy array, with 1 representing filled squares.
        """
        sq_size = (self.size[0]/shape.shape[0], self.size[1]/shape.shape[1]) 
        color = (1,1,1)
        row, col = np.nonzero(shape)
        with self.canvas:
            Color(0.757, 0.573, 0.106, mode='rgb')
            for i in range(len(row)):
                Rectangle(
                    pos = (self.pos[0]+col[i]*sq_size[0], self.pos[1]+row[i]*sq_size[1]),
                    size = sq_size
                )

    def clear_canvas(self):
        self.canvas.clear()
        

class MyPaintBox(BoxLayout):

    def __init__(self, **kwargs):
        super(MyPaintBox, self).__init__(**kwargs)
        self.event = None
        self.golife = Golife()

        self.refresh()
        
  
    def refresh(self):
        """
        Draw current state of gameoflife on canvas
        """
        painter = self.ids['painter']
        painter.clear_canvas()
        painter.draw_shape(shape=self.golife.tab)

    def next(self, *args):
        """
        Draw next step of gameoflife
        """
        self.golife.next()
        self.refresh()

    def start(self):
        """
        Start the animation. Speed is given by slider value.
        """
        fps = self.ids['speed'].value
        self.stop()
        self.event = Clock.schedule_interval(self.next, 1.0/fps)

    def stop(self):
        """
        Stop the animation.
        """
        if self.event is not None:
            self.event.cancel()

    def update_speed(self):
        if (self.event is not None and self.event.is_triggered):
            self.start()

    def update_zoom(self):
        pass

class MyPaintApp(App):

    def build(self):
        return MyPaintBox()


if __name__ == '__main__':
    MyPaintApp().run()


