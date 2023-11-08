#!/usr/bin/env python3
from typing import List, Tuple, Any
from observer import Observer, Subject
import logging


class GUI(Observer):
    def update(self, *args: Any) -> None:
        logging.info("Notified GUI")


class Collaborator(Observer):
    def __init__(self, name: str = "Anonymous"):
        self.name = name

    def update(self, *args: Any) -> None:
        logging.info(f"Notified collaborator '{self.name}'")


class Document(Subject):
    def edit(self) -> None:
        logging.info("Edited document")

        self.notify_observers()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')

    doc = Document()
    o1 = GUI()
    o2 = Collaborator()

    doc.register_observer(o1)
    doc.register_observer(o2)

    doc.edit()
