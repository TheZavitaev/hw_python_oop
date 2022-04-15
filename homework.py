from typing import Dict, Any


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        """
        :param training_type: — имя класса тренировки;
        :param duration: — длительность тренировки в часах;
        :param distance: — дистанция в километрах, которую преодолел пользователь за время тренировки;
        :param speed: — средняя скорость, с которой двигался пользователь;
        :param calories: — количество килокалорий, которое израсходовал
        пользователь за время тренировки.
        """

        self.training_type, self.duration = training_type, duration
        self.distance, self.speed, self.calories = distance, speed, calories

    def show_training_info(self):
        """Метод для вывода сообщений на экран."""

        return self.get_message()

    def get_message(self):
        """Возвращает строку сообщения."""

        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self, action: int, duration: float, weight: float, ) -> None:
        """Конструктор родительского класса, принимает следующие параметры:

        :param action: количество совершённых действий (число шагов при ходьбе и беге либо гребков — при плавании).
        :param duration: длительность тренировки.
        :param weight: вес спортсмена.
        :return: возвращает экземпляр класса Training/дочернего класса."""

        self.action = action
        self.duration = duration
        self.weight = weight
        self.duration_in_min = self.duration * self.MIN_IN_HOUR

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        return (
            (
                self.coeff_calorie_1
                * self.get_mean_speed()
                - self.coeff_calorie_2
            )
            * self.weight
            / self.M_IN_KM
            * self.duration_in_min
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_calorie_1: float = 0.035
    coeff_calorie_2: int = 2
    coeff_calorie_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)

        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.coeff_calorie_1
                * self.weight
                + (
                    self.get_mean_speed()
                    ** self.coeff_calorie_2
                    // self.height
                )
                * self.coeff_calorie_3 * self.weight
            )
            * self.duration_in_min
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self):
        """
        Формула:
        (средняя_скорость + 1.1) * 2 * вес
        """

        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2

        return (
            (self.get_mean_speed() + coeff_calorie_1)
            * coeff_calorie_2
            * self.weight
        )

    def get_mean_speed(self):
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )


WORKOUT_TYPES: Dict[str, Any] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    return WORKOUT_TYPES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
