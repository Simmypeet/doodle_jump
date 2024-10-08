from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generator, Sequence, Type, TypeVar
from doodle_jump.controller import Controller
from doodle_jump.controller.keyboard import Keyboard

from datetime import timedelta

import pygame


class Game:
    __surface: pygame.Surface
    __controller: Controller
    __scene: Scene

    def __init__(self) -> None:
        super().__init__()

        pygame.init()

        self.__surface = pygame.display.set_mode([500, 500])
        self.__controller = Keyboard()

    def update(self, timedelta: timedelta) -> None:
        self.__scene.update(timedelta, self)

    def render(self, timedelta: timedelta) -> None:
        self.__scene.render(timedelta, self)

    @property
    def controller(self) -> Controller:
        return self.__controller

    @property
    def surface(self) -> pygame.Surface:
        return self.__surface

    @property
    def scene(self) -> Scene:
        return self.__scene

    @staticmethod
    def start():
        game = Game()

        running = True
        time_point = pygame.time.get_ticks()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            new_time_point = pygame.time.get_ticks()

            dt = timedelta(milliseconds=new_time_point - time_point)
            dt = dt if dt.total_seconds() > 0 else timedelta(milliseconds=1)

            game.update(dt)
            game.render(dt)

            time_point = new_time_point


class Actor(ABC):
    """
    An object that will be updated and rendered in the scene.
    It can be a player, an enemy, a platform, etc.
    """

    @abstractmethod
    def update(self, timedelta: timedelta, game: Game) -> None:
        """Updates the actor."""
        raise NotImplementedError()

    @abstractmethod
    def render(self, timedelta: timedelta, game: Game) -> None:
        """Renders the actor."""
        raise NotImplementedError()

    @property
    def z_index(self) -> int:
        """The lower the first it gets rendered and updated."""

        return 0


class Scene(ABC):
    """
    A scene holds all the actors that will be updated and rendered.
    """

    __actors: list[Actor]

    __appending_actors: list[Actor]
    __removing_actors: list[Actor]

    __actors_by_type: dict[type, list[Actor]]

    def __init__(self):
        self.__actors = []

    def update(self, timedelta: timedelta, game: Game) -> None:
        """
        Updates all the actors in the scene.

        This method should be overridden by the subclass and call the
        super method.
        """

        for actor in self.__removing_actors:
            self.__actors.remove(actor)
            self.__actors_by_type[type(actor)].remove(actor)

        self.__removing_actors.clear()

        for actor in self.__appending_actors:
            self.__actors.append(actor)
            self.__actors_by_type[type(actor)].append(actor)

        self.__appending_actors.clear()

        for actor in self.__actors:
            actor.update(timedelta, game)

        self.__actors.sort(key=lambda actor: actor.z_index)

    def render(self, timedelta: timedelta, game: Game) -> None:
        """
        Renders all the actors in the scene.

        This method should be overridden by the subclass and call the
        super method.
        """
        for actor in self.__actors:
            actor.render(timedelta, game)

    T = TypeVar("T", bound=Actor, covariant=True)

    def get_actors_of_instance(self, t: Type[T]) -> Generator[T, None, None]:
        """
        Returns all the actors in the scene that are instances of the
        given type.
        """
        for ty, actors in self.__actors_by_type.items():
            if issubclass(t, ty):
                for actor in actors:
                    yield actor  # type: ignore

    @property
    def actors(self) -> Sequence[Actor]:
        return self.__actors
