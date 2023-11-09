#!/usr/bin/env python3
from typing import List, Tuple, Any, Union
import logging

from observer import Observer, Subject
from document import *
from icecream import ic


class GUI(Observer):
    def update(self, *args: Any) -> None:
        logging.info("Notified GUI")


class Collaborator(Observer):
    def __init__(self, name: str = "Anonymous"):
        self.name = name

    def update(self, *args: Any) -> None:
        logging.info(f"Notified collaborator '{self.name}'")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')

    doc = Document(DocumentContent([
        Paragraph("This is the Introduction"),
        Heading("First heading", 1, [
            Paragraph("Inside heading"),
            ListElem([
                ListItem("Item 1"),
                ListItem("Item 2")
            ])
        ])
    ]))

    ic(list(doc.content))

    o1 = GUI()
    o2 = Collaborator()

    doc.register_observer(o1)
    doc.register_observer(o2)

    doc.edit()

    ic(list(doc.content))
