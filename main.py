import time
import logging
import unittest
from os import path

# 1. НАЛАШТУВАННЯ ЛОГУВАННЯ
# Логи будуть виводитися в консоль та записуватися у файл 'sims_simulation.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("sims_simulation.log", mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


# 2. ФУНКЦІЯ ДЛЯ ВИМІРЮВАННЯ ЧАСУ ТА ЛОГУВАННЯ ДІЙ
def log_action_time(action_func, sim, *args, **kwargs):
    """
    Виконує дію сіма, вимірює реальний час її виконання,
    фіксує зміни в стані персонажа та записує все в лог.
    """
    action_name = action_func.__name__.replace('_', ' ').capitalize()
    logging.info(f"==> {sim.name} починає дію: '{action_name}'...")

    start_time = time.perf_counter()
    result = action_func(sim, *args, **kwargs)
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    logging.info(f"==> {sim.name} завершив дію '{action_name}' за {execution_time:.4f} сек.")
    logging.info(f"Поточний стан {sim.name}: {sim.get_status()}\n")

    return result, execution_time


# 3. КЛАС СІМА ТА ЙОГО ДІЇ
class Sim:
    def __init__(self, name):
        self.name = name
        self.energy = 50
        self.hunger = 50
        self.happiness = 50

    def get_status(self):
        return f"Голод: {self.hunger}/100, Енергія: {self.energy}/100, Щастя: {self.happiness}/100"

    def eat_pizza(self):
        time.sleep(0.05)  # Штучна затримка симуляції їжі
        self.hunger = min(100, self.hunger + 30)
        self.happiness = min(100, self.happiness + 10)
        return "Ням-ням! Піца була смачною."

    def sleep_in_bed(self):
        time.sleep(0.1)  # Штучна затримка симуляції сну
        self.energy = min(100, self.energy + 40)
        self.hunger = max(0, self.hunger - 10)
        return "Хррр... Сім відпочив."

    def play_video_games(self, duration_modifier=1):
        time.sleep(0.02 * duration_modifier)
        self.happiness = min(100, self.happiness + 25)
        self.energy = max(0, self.energy - 15)
        return "Катка в Sims завершена!"


# 4. ТЕСТИ ДЛЯ ПЕРЕВІРКИ СИМУЛЯЦІЇ ТА ЛОГУВАННЯ
class TestSimsSimulation(unittest.TestCase):

    def setUp(self):
        """Створюємо нового сіма перед кожним тестом."""
        self.sim = Sim("поліна")

    def test_eat_pizza_logs_and_changes_stats(self):
        """Перевіряємо дію 'їсти піцу': зміну статів, результат та час."""
        res, exec_time = log_action_time(Sim.eat_pizza, self.sim)

        self.assertEqual(res, "Ням-ням! Піца була смачною.")
        self.assertEqual(self.sim.hunger, 80)
        self.assertEqual(self.sim.happiness, 60)
        self.assertGreaterEqual(exec_time, 0.05)

    def test_sleep_logs_and_changes_stats(self):
        """Перевіряємо дію 'спати': відновлення енергії та падіння ситості."""
        _, exec_time = log_action_time(Sim.sleep_in_bed, self.sim)

        self.assertEqual(self.sim.energy, 90)
        self.assertEqual(self.sim.hunger, 40)
        self.assertGreaterEqual(exec_time, 0.1)

    def test_log_file_is_created(self):
        """Перевіряємо, чи створюється фізичний файл логів на диску."""
        log_action_time(Sim.play_video_games, self.sim, duration_modifier=2)
        self.assertTrue(path.exists("sims_simulation.log"))


if __name__ == '__main__':
    # Запуск тестів
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

