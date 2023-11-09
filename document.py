#!/usr/bin/env python3
import logging
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

@dataclass
class DocumentContent(IterableElem):
    items: List[Union[Paragraph, Heading, ListElem]] = field(default_factory=list)


class Document(Subject):
    def __init__(self, content: DocumentContent = DocumentContent(),
                 obs : List[Observer] = []):
        super().__init__(obs)
        self.content = content

    def edit(self) -> None:
        logging.info("Edited document")
        self.content.items.append(Heading("New heading", 1))
        self.notify_observers()
