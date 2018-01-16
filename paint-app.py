from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.slider import Slider
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from kivy.lang import Builder

from gameoflife import Golife

import numpy as np


## To do:
# - Merge start/stop buttons
# - Solve zoom problems (not centered)
# - Add grid lines


Builder.load_string('''
<MyPaintBox>:
    id: box
    orientation: 'vertical'
    MyPaintWidget:
        id: painter

    BoxLayout:
        orientation: 'horizontal'
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
        on_value: root.refresh()
    Spinner:
        id: pattern_select
        size_hint_y: None
        height: '48dp'

''')


class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        """
        Get click and add/remove point from tab.
        """
        if self.collide_point(*touch.pos):
            # Click in the paint widget
            zoom = root.ids['zoom'].value
            sq_size = (
                self.size[0]/Golife.GRID_SIZE[1]*zoom,
                self.size[1]/Golife.GRID_SIZE[0]*zoom)
            a = (
                self.pos[0] + self.size[0]/2*(1-zoom),
                self.pos[1] + self.size[1]/2*(1-zoom))
            col = int((touch.x - a[0])/sq_size[0])
            row = int((touch.y - a[1])/sq_size[1])
            if (0 <= row < Golife.GRID_SIZE[0] and 0 <= col < Golife.GRID_SIZE[1]):
                # print(row, col)
                self.parent.golife.add_point(row, col)
                self.parent.refresh()
            else:
                print("Touch outside of the grid.")

    def draw_tab(self, tab, zoom):
        """
        tab should be a numpy array, with 1 representing filled squares.
        """
        sq_size = (
            self.size[0]/tab.shape[1]*zoom,
            self.size[1]/tab.shape[0]*zoom)
        a = (
            self.pos[0] + self.size[0]/2*(1-zoom),
            self.pos[1] + self.size[1]/2*(1-zoom))
        row, col = np.nonzero(tab)
        with self.canvas:
            Color(0.757, 0.573, 0.106, mode='rgb')
            for i in range(len(row)):
                Rectangle(
                    pos = (a[0]+col[i]*sq_size[0], a[1]+row[i]*sq_size[1]),
                    size = sq_size
                )

    def clear_canvas(self):
        self.canvas.clear()
        

class MyPaintBox(BoxLayout):

    def __init__(self, **kwargs):
        super(MyPaintBox, self).__init__(**kwargs)
        self.event = None
        self.golife = Golife()

        pattern_names = Golife.PATTERNS.keys()
        spinner = self.ids['pattern_select']
        spinner.text = pattern_names[0]
        spinner.values = pattern_names
        spinner.bind(text=self.set_pattern)
        self.set_pattern(spinner, spinner.text)

        self.refresh()
        
  
    def refresh(self):
        """
        Draw current state of gameoflife on canvas
        """
        painter = self.ids['painter']
        painter.clear_canvas()
        zoom = self.ids['zoom'].value
        painter.draw_tab(tab=self.golife.tab, zoom=zoom)

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

    def set_pattern(self, spinner, text):
        print("Let's change the pattern!")
        print(text)
        self.golife.set_pattern(text)


class MyPaintApp(App):

    def build(self):
        global root
        root = MyPaintBox()
        return root


if __name__ == '__main__':
    MyPaintApp().run()


