from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.

    Описание атрибутов класса:
    'training_type' — имя класса тренировки;
    'duration' — длительность тренировки в часах;
    'distance' — дистанция в километрах, которую преодолел
    пользователь за время тренировки;
    'speed' — средняя скорость, с которой двигался пользователь;
    'calories' — количество килокалорий, которое израсходовал
    пользователь за время тренировки.
    """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self):
        """Возвращает строку сообщения."""

        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self, action: int, duration: float, weight: float, ) -> None:
        """Конструктор родительского класса, принимает следующие параметры:

        :param action: количество совершённых действий (число шагов при ходьбе
        и беге либо гребков — при плавании).
        :param duration: длительность тренировки.
        :param weight: вес спортсмена.
        :return: возвращает экземпляр класса Training/дочернего класса."""

        self.action = action
        self.duration_h = duration
        self.weight_kg = weight
        self.duration_in_min = self.duration_h * self.MIN_IN_HOUR

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_RUN_COEFFICIENT_1: int = 18
    CALORIES_RUN_COEFFICIENT_2: int = 20

    def get_spent_calories(self) -> float:
        calories_per_min = (
            (
                self.CALORIES_RUN_COEFFICIENT_1
                * self.get_mean_speed()
                - self.CALORIES_RUN_COEFFICIENT_2
            ) * self.weight_kg / self.M_IN_KM
        )

        return calories_per_min * self.duration_in_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WALKING_COEFFICIENT_1: float = 0.035
    CALORIES_WALKING_COEFFICIENT_2: int = 2
    CALORIES_WALKING_COEFFICIENT_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)

        self.height_cm = height

    def get_spent_calories(self) -> float:
        calories_per_min = (
            (
                self.CALORIES_WALKING_COEFFICIENT_1 * self.weight_kg
                + (
                    self.get_mean_speed()
                    ** self.CALORIES_WALKING_COEFFICIENT_2
                    // self.height_cm
                )
                * self.CALORIES_WALKING_COEFFICIENT_3 * self.weight_kg
            )
        )
        return calories_per_min * self.duration_in_min


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)

        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self):
        """
        Формула:
        (средняя_скорость + 1.1) * 2 * вес
        """

        CALORIES_SWIMMING_COEFFICIENT_1: float = 1.1
        CALORIES_SWIMMING_COEFFICIENT_2: int = 2

        return (
            (self.get_mean_speed() + CALORIES_SWIMMING_COEFFICIENT_1)
            * CALORIES_SWIMMING_COEFFICIENT_2
            * self.weight_kg
        )

    def get_mean_speed(self):
        return (
            self.length_pool_m
            * self.count_pool
            / self.M_IN_KM
            / self.duration_h
        )


WORKOUT_TYPES: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in WORKOUT_TYPES:
        acceptable_types_training = ', '.join(WORKOUT_TYPES)
        raise (
            f'Получен неизвестный тип тренировки - {workout_type}.'
            f'Допустимые значения - {acceptable_types_training}'
        )

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
