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


Builder.load_string('''
<MyPaintBox>:
    id: box
    orientation: 'vertical'
    padding: [4,4,4,4]
    spacing: 4
    MyPaintWidget:
        id: painter
        size_hint_y: 1

    BoxLayout:
        id: commands
        orientation: 'horizontal'
        spacing: 2
        size_hint_y: None
        height: '48dp'
        Button:
            id: start
            text: 'Start'
            size_hint_y: None
            height: '48dp'
            on_press: root.start_stop_action()
        Button: 
            text: 'Next'
            size_hint_y: None
            height: '48dp'
            on_press: root.next()
        Image:
            source: 'images/speed-resized.jpg'
            size_hint_x: None
            height: '45dp'
            width: '45dp'
        Slider:
            id: speed
            value: 2
            min: 1
            max: 50
            step: 2
            value_track: True
            size_hint_y: None
            height: '48dp'
            on_value: root.update_speed()
        Image:
            source: 'images/zoom-resized.jpg'
            size_hint_x: None
            height: '45dp'
            width: '45dp'
        Slider:
            id: zoom
            value: 12
            min: 3
            max: 20
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

            a = ((zoom-1.0)/(2*zoom), (zoom+1.0)/(2*zoom))
            idx = [int(i*j) for j in Golife.GRID_SIZE for i in a]
            # idx = (int(a[0]*tab.shape[0]), int(a[1]*tab.shape[0]),
            #     int(a[0]*tab.shape[1]), int(a[1]*tab.shape[1]))
            sq_size = (
                1.0 * self.size[0]/(idx[3]-idx[2]),
                1.0 * self.size[1]/(idx[1]-idx[0]))
            a = (
                self.pos[0] + self.size[0]/2*(1-zoom),
                self.pos[1] + self.size[1]/2*(1-zoom))
            col = int((touch.x - self.pos[0])/sq_size[0]) + idx[2]
            row = int((touch.y - self.pos[1])/sq_size[1]) + idx[0]
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
        alpha = 1 # Print smaller squares to show space between squares

        # Only consider needed portion of tab (zoom)
        a = ((zoom-1.0)/(2*zoom), (zoom+1.0)/(2*zoom))
        tab = tab[int(a[0]*tab.shape[0]):int(a[1]*tab.shape[0]), int(a[0]*tab.shape[1]):int(a[1]*tab.shape[1])]
        sq_size = (
            1.0 * self.size[0]/tab.shape[1],
            1.0 * self.size[1]/tab.shape[0])
        row, col = np.nonzero(tab)
        with self.canvas:
            # Background
            Color(0.69, 0.70, 0.72, mode='rgb') # Grey
            Rectangle(pos=self.pos, size=self.size)

            # Cells
            Color(0.757, 0.573, 0.106, mode='rgb') # Orange
            for i in range(len(row)):
                Rectangle(
                    pos = (int(self.pos[0]+col[i]*sq_size[0]), int(self.pos[1]+row[i]*sq_size[1])),
                    size = (int(alpha*sq_size[0]), int(alpha*sq_size[1]))
                )

            # Grid
            Color(0.6,0.6,0.6, mode='rgb') # black
            for i in range(tab.shape[0]):
                Line(points = 
                    [self.pos[0],
                    int(self.pos[1] + i*sq_size[1]),
                    self.pos[0] + self.size[0],
                    int(self.pos[1] + i*sq_size[1])],
                    width = 1
                    )
            for i in range(tab.shape[1]):
                Line(points = 
                    [int(self.pos[0] + i*sq_size[0]),
                    self.pos[1],
                    int(self.pos[0] + i*sq_size[0]),
                    self.pos[1] + self.size[1]],
                    width = 0.5
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
        self.golife.set_pattern(text)
        self.refresh()

    def start_stop_action(self):
        """
        Deals with the start/stop button
        """
        btn = self.ids['start']
        if (self.event is not None and self.event.is_triggered):
            self.stop()
            btn.text = 'Start'
        else:
            self.start()
            btn.text = 'Stop'



class GameOfLifeApp(App):

    def build(self):
        global root
        root = MyPaintBox()
        return root


if __name__ == '__main__':
    GameOfLifeApp().run()


