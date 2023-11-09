#!/usr/bin/env python3
from typing import List, Tuple, Any, Union
from dataclasses import dataclass, field
import logging

from observer import Observer, Subject
from icecream import ic

class IterableElem:
    '''Children of this class must have an iterable `items` attribute'''
    def __iter__(self):
        return next(self)

    def __next__(self):
        yield self
        for item in self.items:
            for i in item:
                yield i

class NonIterable:
    def __iter__(self):
        return next(self)

    def __next__(self):
        yield self


@dataclass
class Paragraph(NonIterable):
    text: str

@dataclass
class ListItem(NonIterable):
    text: str

@dataclass
class ListElem(IterableElem):
    items: List[ListItem] = field(default_factory=list)

@dataclass
class Heading(IterableElem):
    text: str
    level: int
    items: List[Union[Paragraph, 'Heading', ListElem]] = field(default_factory=list)

@dataclass
class DocumentContent(IterableElem):
    items: List[Union[Paragraph, Heading, ListElem]] = field(default_factory=list)



class GUI(Observer):
    def update(self, *args: Any) -> None:
        logging.info("Notified GUI")


class Collaborator(Observer):
    def __init__(self, name: str = "Anonymous"):
        self.name = name

    def update(self, *args: Any) -> None:
        logging.info(f"Notified collaborator '{self.name}'")


class Document(Subject):
    def __init__(self, content: DocumentContent = DocumentContent(),
                 obs : List[Observer] = []):
        super().__init__(obs)
        self.content = content

    def edit(self) -> None:
        logging.info("Edited document")
        self.notify_observers()


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
