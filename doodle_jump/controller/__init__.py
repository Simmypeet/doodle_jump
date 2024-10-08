from abc import ABC, abstractmethod

from datetime import timedelta

class Controller(ABC):
    """Controller abstract class"""

    @abstractmethod
    def update(self, delta: timedelta) -> None:
        """
        Update the controller state for getting the input. This should be called
        once per frame before retrieving the input
        """
        raise NotImplementedError()

    @abstractmethod
    def horizontal(self) -> float:
        """
        Gets the horizontal update value of the controller. 

        Positive value moves to the right, left otherwise
        """
        raise NotImplementedError()
    
    @abstractmethod
    def shoot(self) -> bool:
        """
        Gets the shoot update

        If returns `True` the character will shoot .
        """
        raise NotImplementedError()
    