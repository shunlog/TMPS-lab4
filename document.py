#!/usr/bin/env python3
import logging
import copy
from dataclasses import dataclass, field
from typing import List, Tuple, Any, Union

from observer import Observer, Subject

class IterableElem:
    '''Children of this class must have an iterable `items` attribute'''
    def __iter__(self):
        return next(self)

    def __next__(self):
        for item in self.items:
            for i in item:
                yield i

class IterableTextElem:
    '''Like IterableElem, but these also have a text themselves.'''
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
class Heading(IterableTextElem):
    text: str
    level: int
    items: List[Union[Paragraph, 'Heading', ListElem]] = field(default_factory=list, repr=False)

@dataclass()
class DocumentContent(IterableElem):
    items: List[Union[Paragraph, Heading, ListElem]] = field(default_factory=list)


class Document(Subject):
    def __init__(self, content: DocumentContent = DocumentContent(),
                 obs : List[Observer] = []):
        super().__init__(obs)
        self.content = content

    def append_heading(self) -> None:
        self.content.items.append(Heading("New heading", 1))
        self.notify_observers()

    def set_state(self, state):
        self.content = state
        self.notify_observers()

    def get_state(self):
        return copy.deepcopy(self.content)


class Buffer:
    def __init__(self, doc: Document):
        self.doc = doc
        self.undo_hist = []

    def __save_state(self):
        self.undo_hist.append(self.doc.get_state())

    def __undo_state(self):
        try:
            self.doc.set_state(self.undo_hist.pop())
        except:
            raise RuntimeError("Nothing to undo")

    def edit(self):
        self.__save_state()
        self.doc.append_heading()
        logging.info("Made edit")

    def undo(self):
        try:
            self.__undo_state()
            logging.info("Undo edit")
        except:
            logging.info("Nothing to undo")
