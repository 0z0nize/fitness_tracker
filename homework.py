from dataclasses import asdict, dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TEXT_MES: str = ('Тип тренировки: {training_type}; '
                     'Длительность: {duration:.3f} ч.; '
                     'Дистанция: {distance:.3f} км; '
                     'Ср. скорость: {speed:.3f} км/ч; '
                     'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.TEXT_MES.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    ACTION: float
    DURATION: float
    WEIGHT: float
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MINUTES: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.ACTION * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.DURATION

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Предоставьте формулу расчёта калорий')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.DURATION,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.WEIGHT / self.M_IN_KM
                * self.DURATION * self.MINUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    ACTION: float
    DURATION: float
    WEIGHT: float
    HEIGHT: float
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 2
    COEFF_CALORIE_3: float = 0.029

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1 * self.WEIGHT
                + (self.get_mean_speed()**self.COEFF_CALORIE_2 // self.HEIGHT)
                * self.COEFF_CALORIE_3 * self.WEIGHT)
                * self.DURATION * self.MINUTES)


class Swimming(Training):
    """Тренировка: плавание."""

    ACTION: float
    DURATION: float
    WEIGHT: float
    LENGTH_POOL: float
    COUNT_POOL: float
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.WEIGHT)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.LENGTH_POOL * self.COUNT_POOL
                / self.M_IN_KM / self.DURATION)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    code_class: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    code_list = ", ".join(code_class)
    if workout_type not in code_class:
        raise ValueError(f'{workout_type} - неизвестный тип тренировки;'
                         f' используйте: {code_list}')
    return code_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
