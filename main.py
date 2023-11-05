import customtkinter as ctk
import random
import pyautogui
import threading
import time

class AntiAFKClickerApp(ctk.CTk):
    def __init__(self):
        """
        Инициализация приложения Anti-AFK Clicker.

        Этот класс создает графический интерфейс пользователя для управления кликером.
        """
        super().__init__()
        self.title("Anti-AFK Clicker by @ohmwraith")
        self.geometry("400x350")
        self.iconbitmap(True, "./icon.ico")


        self.resizable(False, False)

        self.click_count = 0
        self.clicker_label = ctk.CTkLabel(
            self, text=f"Clicks: {self.click_count}", font=("Helvetica", 20)
        )
        self.clicker_label.pack(pady=20)

        self.time_label = ctk.CTkLabel(
            self, text="Time Elapsed: 0h 0m 0s", font=("Helvetica", 14)
        )
        self.time_label.pack()

        self.start_button = ctk.CTkButton(self, text="Start Clicking", command=self.start_clicker)
        self.start_button.pack()

        self.stop_button = ctk.CTkButton(self, text="Stop Clicking", command=self.stop_clicker)
        self.stop_button.configure(state="disabled")
        self.stop_button.pack()

        self.auto_click = False
        self.auto_click_thread = None
        self.elapsed_time_thread = None
        self.stop_event = threading.Event()
        self.start_time = None
        self.start_click_time = None
        self.min_delay = 5  # Минимальное время ожидания в секундах
        self.random_deviation = 0  # Случайное отклонение в секундах

        self.setup_controls()

    def setup_controls(self):
        """
        Настройка элементов управления для настройки кликера.

        Этот метод создает слайдеры для настройки минимального задержки и случайного отклонения кликов.
        """
        self.delay_label = ctk.CTkLabel(self, text="Min Delay (s):")
        self.delay_label.pack()
        self.delay_slider = ctk.CTkSlider(
            self, from_=self.min_delay, to=300, orientation="horizontal", width=300, number_of_steps=100
        )
        
        self.delay_slider.set(self.min_delay)
        self.delay_slider.pack()
        self.delay_value_label = ctk.CTkLabel(self, text=str(self.min_delay))
        self.delay_value_label.pack()

        self.deviation_label = ctk.CTkLabel(self, text="Random Deviation (s):")
        self.deviation_label.pack()
        self.deviation_slider = ctk.CTkSlider(
            self, from_=self.random_deviation, to=100, orientation="horizontal", width=300, number_of_steps=100
        )
        self.deviation_slider.set(self.random_deviation)
        self.deviation_slider.pack()
        self.deviation_value_label = ctk.CTkLabel(self, text=str(self.random_deviation))
        self.deviation_value_label.pack()

        # Добавьте обработчики событий для слайдеров
        self.delay_slider.bind("<Motion>", self.update_delay_label)
        self.deviation_slider.bind("<Motion>", self.update_deviation_label)

    def update_delay_label(self, event):
        """
        Обновление значения минимальной задержки и его отображение.

        Этот метод обновляет значение минимальной задержки, когда пользователь изменяет слайдер, и отображает его на экране.
        """
        self.min_delay = self.delay_slider.get()
        self.delay_value_label.configure(text=str(round(self.min_delay)))

    def update_deviation_label(self, event):
        """
        Обновление значения случайного отклонения и его отображение.

        Этот метод обновляет значение случайного отклонения, когда пользователь изменяет слайдер, и отображает его на экране.
        """
        self.random_deviation = self.deviation_slider.get()
        self.deviation_value_label.configure(text=str(round(self.random_deviation)))

    def start_clicker(self):
        """
        Запуск кликера.

        Этот метод запускает кликер с заданными настройками минимальной задержки и случайного отклонения.
        """
        self.auto_click = True
        self.min_delay = self.delay_slider.get()
        self.random_deviation = self.deviation_slider.get()
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.start_time = time.time()
        self.start_click_time = self.start_time
        self.stop_event.clear()
        self.auto_click_thread = threading.Thread(target=self.run_clicker)
        self.auto_click_thread.start()
        self.elapsed_time_thread = threading.Thread(target=self.update_time_label)
        self.elapsed_time_thread.start()

    def stop_clicker(self):
        """
        Остановка кликера.

        Этот метод останавливает работу кликера и обновляет интерфейс пользователя.
        """
        self.auto_click = False
        self.stop_event.set()  # Установите событие для остановки потока
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def run_clicker(self):
        """
        Основная логика кликера.

        Этот метод выполняет клики с учетом заданных параметров, пока кликер активен.
        """
        while self.auto_click:
            if self.stop_event.is_set():
                break  # Проверьте событие остановки и выходите, если оно установлено
            self.click_count += 1
            self.update_click_count()
            self.perform_click()
            self.random_sleep()


    def update_click_count(self):
        """
        Обновление отображения количества кликов.

        Этот метод обновляет отображение количества кликов на экране.
        """
        self.clicker_label.configure(text=f"Clicks: {self.click_count}")

    def update_time_label(self):
        """
        Обновление отображения прошедшего времени.

        Этот метод обновляет отображение прошедшего времени на экране.
        """
        while self.auto_click:
            elapsed_time = time.time() - self.start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.configure(text=f"Time Elapsed: {int(hours)}h {int(minutes)}m {int(seconds)}s")
            if self.stop_event.is_set():
                break
            time.sleep(1)

    def random_sleep(self):
        delay = self.min_delay + random.uniform(0, self.random_deviation)
        time.sleep(delay)

    def perform_click(self):
        x, y = 500, 500  # Координаты, куда нужно выполнить щелчок
        pyautogui.click(x, y)

if __name__ == "__main__":
    app = AntiAFKClickerApp()

    app.mainloop()
