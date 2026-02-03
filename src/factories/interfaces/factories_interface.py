from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")

class FactoriesInterface(Generic[T], ABC):

    @classmethod
    @abstractmethod
    def create_one(cls, session, **kwargs) -> Optional[T]:
        pass

    @classmethod
    @abstractmethod
    def create_many(cls, session, nb_users=5, **kwargs) -> List[T]:
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for method in ["create_one", "create_many"]:
            if not callable(getattr(cls, method, None)):
                raise NotImplementedError(
                    f"Classe {cls.__name__} doit implémenter la méthode {method}"
                )
