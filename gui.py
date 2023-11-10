#!/usr/bin/env python3
import logging
from typing import List, Tuple, Any, Union

from observer import Observer, Subject

class GUI(Observer):
    def update(self, *args: Any) -> None:
        logging.info("Notified GUI")
