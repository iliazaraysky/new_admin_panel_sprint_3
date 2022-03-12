import abc        # cursor.execute("""
        # SELECT film_work.id,
        # film_work.modified
        # FROM film_work
        # WHERE film_work.modified > '2022-03-10 21:00:00'
        # """)
import json
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as write_file:
            json.dump(state, write_file)

    def retrieve_state(self) -> dict:
        if self.file_path is not None:
            try:
                with open(self.file_path, 'r') as write_file:
                    data = json.load(write_file)
                return data
            except FileNotFoundError:
                return {}
        else:
            return {}


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        data_get = self.storage.retrieve_state()
        if data_get is not None:
            data_get[key] = value
            self.storage.save_state(data_get)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        try:
            data = self.storage.retrieve_state()
            return data[key]
        except KeyError:
            return None

file = JsonFileStorage('./file.json')
state = State(file)
# state.set_state('data_1', 1)
# set_state_test_value = state.get_state('data_1')
# assert set_state_test_value == 1
