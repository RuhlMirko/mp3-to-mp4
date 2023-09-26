from threading import Thread
from moviepy.editor import VideoFileClip
from tkinter.filedialog import askopenfile

from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp

from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button

from kivy.core.window import Window

Window.size = (500, 500)


class App(MDApp):
    def fileChooser(self, event):
        try:
            self.file = askopenfile(mode='r', filetypes=[("mp4 files", "*.mp4")])
            self.video_file = self.file.name
            self.audio_file = self.video_file.replace("mp4", "mp3")
            self.locationLabel.text = self.video_file
            self.convertButton.pos_hint = {'center_x': 0.5, 'center_y': 0.25}

            self.statusLabel.text = ""
        except:
            self.statusLabel.color = (1, 0, 0)
            self.statusLabel.text = "Please choose a mp4 file."

    def convertToAudio(self):
        try:
            self.video = VideoFileClip(self.video_file)
            self.audio = self.video.audio

            self.audio.write_audiofile(self.audio_file)
            self.statusLabel.color = (0, 1, 0)
            self.statusLabel.text = "Conversion successful"
            self.audio.close()
            self.video.close()
        except:
            self.statusLabel.color = (1, 0, 0)
            self.statusLabel.text = "Conversion failed"

    def convert(self, event):
        thread1 = Thread(target=self.convertToAudio)
        thread1.start()

    def build(self):
        layout = MDRelativeLayout(md_bg_color=[57 / 255, 62 / 255, 84 / 255])

        self.logo = Image(source="logo.png", pos_hint={'center_x': 0.5, 'center_y': 0.80})

        self.fileChooserLabel = Label(text="Select file to convert",
                                      pos_hint={'center_x': 0.4, 'center_y': 0.45},
                                      font_size=20,
                                      )
        self.selectButton = Button(text="Select",
                                   size_hint=(None, None),
                                   pos=(320, 210),
                                   height=40,
                                   on_press=self.fileChooser
                                   )
        self.locationLabel = Label(text="",
                                   pos_hint={'center_x': 0.5, 'center_y': .35},
                                   color=[0.5, 0.5, 0.5],
                                   font_size=12,
                                   )

        self.convertButton = Button(text="Convert",
                                    pos_hint={'center_x': 0.5, 'center_y': 20},
                                    size_hint=(.2, .1),
                                    size=(75, 75),
                                    pos=(340, 100),
                                    height=40,
                                    on_press=self.convert,
                                    background_color=[0, 0, 1],
                                    )
        self.statusLabel = Label(text="",
                                 pos_hint={'center_x': 0.5, 'center_y': 0.15},
                                 color=[1, 0, 0],
                                 font_size=24,
                                 bold=True,
                                 )
        # Adding widgets to layout
        layout.add_widget(self.logo)
        layout.add_widget(self.fileChooserLabel)
        layout.add_widget(self.selectButton)
        layout.add_widget(self.locationLabel)
        layout.add_widget(self.convertButton)
        layout.add_widget(self.statusLabel)

        return layout


if __name__ == "__main__":
    App().run()
