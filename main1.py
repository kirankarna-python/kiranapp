import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
import openai

openai.api_key = "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"

class QuestionScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Add a horizontal box layout for the mode buttons
        self.mode_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.05))
        self.add_widget(self.mode_box)

        # Add the light mode and dark mode buttons using ToggleButton
        self.light_mode_button = ToggleButton(
            text='Light Mode',
            group='mode',
            state='down'
        )
        self.light_mode_button.bind(on_press=self.set_light_mode)
        self.mode_box.add_widget(self.light_mode_button)

        self.dark_mode_button = ToggleButton(
            text='Dark Mode',
            group='mode'
        )
        self.dark_mode_button.bind(on_press=self.set_dark_mode)
        self.mode_box.add_widget(self.dark_mode_button)

        self.question_input = TextInput(hint_text='Enter your question with KiranKarna',
                                         size_hint=(1, 0.3),
                                         font_size='18sp')
                                         
        self.answer_output = TextInput(readonly=True,
                                        size_hint=(1, None),
                                        height=500,
                                        font_size='18sp')
        self.answer_output.bind(minimum_height=self.answer_output.setter('height'))
        
        self.answer_scroll_view = ScrollView(
            size_hint=(1, 0.9),
            do_scroll_x=False,
        )
        self.answer_scroll_view.add_widget(self.answer_output)
        
        self.submit_button = Button(text='Submit',
                                    size_hint=(1, 0.1),
                                    font_size='15sp')
        self.submit_button.bind(on_press=self.get_answer)
        
        self.add_widget(self.question_input)
        self.add_widget(self.answer_scroll_view)
        self.add_widget(self.submit_button)
    
    def get_answer(self, *args):
        question = self.question_input.text
        answer = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            temperature=0.5,
            max_tokens=4000,  # Set max_tokens to 4000
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        self.answer_output.text = answer.choices[0].text

    def set_light_mode(self, *args):
        self.light_mode_button.state = 'down'
        self.dark_mode_button.state = 'normal'
        Window.clearcolor = (1, 1, 1, 1)

    def set_dark_mode(self, *args):
        self.light_mode_button.state = 'normal'
        self.dark_mode_button.state = 'down'
        Window.clearcolor = (0.1, 0.1, 0.1, 1)


class MyApp(App):
    def build(self):
        return QuestionScreen()

if __name__ == '__main__':
    MyApp().run()
