#!/usr/bin/env python3
import logging
from typing import List, Tuple, Any, Union

from observer import Observer, Subject

class Collaborator(Observer):
    def __init__(self, name: str = "Anonymous"):
        self.name = name

    def update(self, *args: Any) -> None:
        logging.info(f"Notified collaborator '{self.name}'")
