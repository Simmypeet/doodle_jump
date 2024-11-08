from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generator, Sequence, Type, TypeVar

from datetime import timedelta
from pygame.surface import Surface
from pygame.event import Event

import pygame
import time

from doodle_jump.render_target import RenderTarget


@dataclass(frozen=True)
class FrameInfo:
    time: timedelta
    events: Sequence[Event]


class Game:
    __surface: Surface
    __scene: Scene

    __is_running: bool

    def __init__(self, starting_scene: Callable[[Game], Scene]) -> None:
        super().__init__()

        pygame.init()

        self.__surface = pygame.display.set_mode([500, 800])
        self.__scene = starting_scene(self)

        self.is_running = True

    def update(self, info: FrameInfo) -> None:
        self.__scene.update(info, self)

    def render(self, info: FrameInfo) -> None:
        pygame.draw.rect(
            self.__surface, (100, 149, 237), self.__surface.get_rect()
        )

        self.__scene.render(info, self)
        pygame.transform.rotate

        pygame.display.flip()

    @property
    def surface(self) -> pygame.Surface:
        return self.__surface

    @property
    def scene(self) -> Scene:
        return self.__scene

    def stop(self):
        pygame.quit()
        quit()
        # self.__is_running = False  # Set the running flag to False
        print(
            "Game has stopped."
        )  # Optional: print a message or take other actions

    @staticmethod
    def start(starting_scene: Callable[[Game], Scene]) -> None:
        game = Game(starting_scene)

        running = True
        time_point = time.time()

        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            new_time_point = time.time()

            dt = timedelta(seconds=new_time_point - time_point)
            dt = dt if dt.total_seconds() > 0 else timedelta(milliseconds=1)

            info = FrameInfo(dt, events)

            game.update(info)
            game.render(info)

            time_point = new_time_point


class Scene(ABC):
    """
    A scene holds all the actors that will be updated and rendered.
    """

    __actors: list[Actor]

    __appending_actors: list[Actor]
    __removing_actors: set[Actor]

    __actors_by_type: dict[type, list[Actor]]

    def __init__(self):
        self.__actors = []

        self.__appending_actors = []
        self.__removing_actors = set()

        self.__actors_by_type = {}

    def update(self, info: FrameInfo, game: Game) -> None:
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
            self.__actors_by_type.setdefault(type(actor), []).append(actor)

        self.__appending_actors.clear()

        for actor in self.__actors:
            actor.update(info, game)

        self.__actors.sort(key=lambda actor: actor.z_index)

    def render_actors(
        self, info: FrameInfo, render_target: RenderTarget, game: Game
    ):
        """
        Renders all the actors in the scene.
        """
        for actor in self.__actors:
            actor.render(info, render_target, game)

    @abstractmethod
    def render(self, info: FrameInfo, game: Game) -> None:
        """Renders the scene."""

        raise NotImplementedError()

    T = TypeVar("T")

    def get_actors_of_instance(self, t: Type[T]) -> Generator[T, None, None]:
        """
        Returns all the actors in the scene that are instances of the
        given type.
        """
        for ty, actors in self.__actors_by_type.items():
            if issubclass(t, ty):
                for actor in actors:
                    yield actor  # type: ignore

    def add_actor(self, actor: Actor) -> None:
        """Adds an actor to the scene."""
        self.__appending_actors.append(actor)

    def remove_actor(self, actor: Actor) -> None:
        """Removes an actor from the scene."""
        self.__removing_actors.add(actor)

    @property
    def actors(self) -> Sequence[Actor]:
        return self.__actors


class Actor(ABC):
    """
    An object that will be updated and rendered in the scene.
    It can be a player, an enemy, a platform, etc.
    """

    @abstractmethod
    def update(self, info: FrameInfo, game: Game) -> None:
        """Updates the actor."""
        raise NotImplementedError()

    @abstractmethod
    def render(
        self, info: FrameInfo, render_target: RenderTarget, game: Game
    ) -> None:
        """Renders the actor."""
        raise NotImplementedError()

    @property
    def z_index(self) -> int:
        """The lower the first it gets rendered and updated."""

        return 0
