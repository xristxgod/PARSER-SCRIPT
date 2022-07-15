from typing import Any


class StaticCRUD():
    @staticmethod
    def create(**kwargs: Any) -> bool:
        raise NotImplementedError

    @staticmethod
    def read(**kwargs: Any) -> Any:
        raise NotImplementedError

    @staticmethod
    def update(**kwargs: Any) -> bool:
        raise NotImplementedError

    @staticmethod
    def delete(**kwargs: Any) -> bool:
        raise NotImplementedError


class CRUD:
    def create(self, **kwargs: Any) -> bool:
        raise NotImplementedError

    def read(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def update(self, **kwargs: Any) -> bool:
        raise NotImplementedError

    def delete(self, **kwargs: Any) -> bool:
        raise NotImplementedError
