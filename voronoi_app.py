import kivy
from kivy.core.window import Window

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.graphics import *

from generate_voronoi_image import *

class InputImageFile(BoxLayout):


    def __init__(self, **kwargs):
        super(InputImageFile, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [30,200]
        self.spacing = 50

        self.message = Label(text="Image to load:")
        self.add_widget(self.message)

        self.image_fname_text = TextInput(multiline=False, height=30)
        self.image_fname_text.bind(on_text_validate=self.go_button_pressed)
        self.add_widget(self.image_fname_text)

        self.go_button = Button(text="Go")
        self.go_button.bind(on_press=self.go_button_pressed)
        self.add_widget(self.go_button)

        self.points_and_weights = []
        self.weight_labels = []
        self.weight_sliders = []

    def go_button_pressed(self, instance):
        file_name = self.image_fname_text.text
        try:
            file = open(file_name, 'rb')
        except:
            self.message.text = "Couldn't open that file"
            return

        file.close()

        self.clear_widgets()
        self.orientation = 'horizontal'
        self.padding = [5,5]
        self.spacing = 10

        self.fp = file_name

        self.image = kivy.uix.image.Image(source=file_name)
        self.add_widget(self.image)
        self.image.bind(on_touch_down=self.add_point)

        self.slider_widget = SlidersAndOptions()

        self.message = Label(text="Place points of interest by clicking on your image.", height=30, size_hint=(1, None))
        self.euclid_metric = Button(text="Show Voronoi with Euclidean metric", height=30, size_hint=(0.5, None))
        self.euclid_metric.bind(on_press=self.euclid_generate)
        self.inf_metric = Button(text="Show Voronoi with L infinity metric", height=30, size_hint=(0.5, None))
        self.inf_metric.bind(on_press=self.inf_generate)
        self.manhattan_metric = Button(text="Show Voronoi with Manhattan metric", height=30, size_hint=(0.5, None))
        self.manhattan_metric.bind(on_press=self.manhattan_generate)

        self.slider_widget.add_widget(self.message)
        self.slider_widget.add_widget(self.euclid_metric)
        self.slider_widget.add_widget(self.inf_metric)
        self.slider_widget.add_widget(self.manhattan_metric)

        self.clear_points_button = Button(text="Clear points", height=30, size_hint=(0.5, None))
        self.clear_points_button.bind(on_press=self.clear_points)
        self.slider_widget.add_widget(self.clear_points_button)
        self.add_widget(self.slider_widget)

    def add_point(self, instance, mouse_event):
        if self.image.collide_point(mouse_event.pos[0], mouse_event.pos[1]):
            new_slider = Slider(min=0, max=10, value=5, size_hint=(0.5, None), height=50)
            new_label = TextInput(text="Point " + str(len(self.points_and_weights)),
                                                    height=30, size_hint=(0.5, None))

            self.weight_sliders.append(new_slider)
            self.weight_labels.append(new_label)
            self.points_and_weights.append((mouse_event.pos, 5))

            self.slider_widget.add_widget(new_label)
            self.slider_widget.add_widget(new_slider)

            self.image.canvas.add(Rectangle(pos=mouse_event.pos, size=(5, 5)))

    def clear_points(self, instance):
        for slider in self.weight_sliders:
            self.slider_widget.remove_widget(slider)
        for label in self.weight_labels:
            self.slider_widget.remove_widget(label)

        self.points_and_weights = []
        self.weight_sliders = []
        self.weight_labels = []

    def euclid_generate(self, instance):
        print(self.points_and_weights)
        self.output_fname = generate_voronoi_diagram(self.fp, GenerateInput([pw[0] for pw in self.points_and_weights],
                                                        [slider.value for slider in self.weight_sliders],
                                                        euclidean_metric,
                                                        self.image.norm_image_size,
                                                        self.image.width,
                                                        self.image.height))
        self.image.source = self.output_fname
        self.image.reload()

    def manhattan_generate(self, instance):
        self.output_fname = generate_voronoi_diagram(self.fp, GenerateInput([pw[0] for pw in self.points_and_weights],
                                                        [slider.value for slider in self.weight_sliders],
                                                        manhattan_metric,
                                                        self.image.norm_image_size,
                                                        self.image.width,
                                                        self.image.height))
        self.image.source = self.output_fname
        self.image.reload()

    def inf_generate(self, instance):
        self.output_fname = generate_voronoi_diagram(self.fp, GenerateInput([pw[0] for pw in self.points_and_weights],
                                                        [slider.value for slider in self.weight_sliders],
                                                        inf_metric,
                                                        self.image.norm_image_size,
                                                        self.image.width,
                                                        self.image.height))
        self.image.source = self.output_fname
        self.image.reload()

class SlidersAndOptions(StackLayout):


    def __init__(self, **kwargs):
        super(SlidersAndOptions, self).__init__(**kwargs)
        self.orientation = 'lr-tb'


class MyApp(App):

    def build(self):
        return InputImageFile()


if __name__ == '__main__':
    MyApp().run()