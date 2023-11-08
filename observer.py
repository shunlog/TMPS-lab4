#!/usr/bin/env python3
from typing import List, Tuple, Any
import logging

class Observer:
    def update(self) -> None:
        raise RuntimeError("This method should be over-ridden by a child class.")


class Subject:
    def __init__(self, obs : List[Observer] = []) -> None:
        self.observers : List[Observer] = obs

    def register_observer(self, o: Observer) -> None:
        logging.debug(f"Registered observer for {self}: {o}")
        self.observers.append(o)

    def remove_observer(self, o: Observer) -> None:
        try:
            self.observers.remove(o)
            logging.debug(f"Removed observer for {self}: {o}")
        except ValueError:
            raise ValueError("Observer not in list", o)

    def notify_observers(self, *args: Any) -> None:
        logging.debug(f"Notifying all observers for {self}")
        for o in self.observers:
            o.update(*args)
