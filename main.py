from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests


API_KEY = "9d081b20dfa17c0a6d1bf2af8b76e4c3"

URL = "https://api.themoviedb.org/3/search/movie"


class MovieApp(App):
    def build(self):

        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.search_input = TextInput(
            text='Интерстеллар',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        root.add_widget(self.search_input)

        search_button = Button(
            text='Искать фильм',
            size_hint_y=None,
            height=50,
            background_color=(0.1, 0.5, 0.8, 1)
        )

        search_button.bind(on_press=self.on_search_click)
        root.add_widget(search_button)

        self.result_label = Label(
            text='Здесь появятся результаты поиска...',
            halign='left',
            valign='top',
            size_hint_y=None
        )

        self.result_label.bind(texture_size=self.result_label.setter('size'))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_label)
        root.add_widget(scroll)

        return root

    def on_search_click(self, instance):
        query = self.search_input.text.strip()
        if not query:
            self.result_label.text = "Введите название фильма"
            return

        headers = {
              "accept": "application/json",
              "Authorization": "Bearer..."
               }
        
        params = {
            "api_key": API_KEY,
            "query": query,
            "language": "ru-RU"
               }
    
        try:
            response = requests.get(URL, headers=headers, params=params)

            if response.status_code == 200:
               data = response.json()
               results = data.get("results", [])

            if not results:
                print("Фильмы не найдены...")
                return

            output_text = "" 

            for movie in results[:3]:
                title = movie.get("title")
                release_date = movie.get("release_date", "Дата неизвестна")
                overview = movie.get("overview", "Описание отсутствует")

                output_text = f"{title} {release_date}\n{overview[:120]}...\n" + "-"*30 + "\n\n"

                self.result_label.text = output_text

            else:
                self.result_label.text = f"Ошибка сервера {response.status_code}"

        except Exception as e:
            self.result_label.text = f"Ошибка подключения: {e}"

if __name__ == '__main__':
    MovieApp().run()