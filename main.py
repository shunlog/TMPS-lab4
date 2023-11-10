#!/usr/bin/env python3
from typing import List, Tuple, Any, Union
import logging
from icecream import ic

from observer import Observer, Subject
from document import *
from gui import GUI
from collab import Collaborator


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')

    buf = Buffer(Document(DocumentContent([
        Paragraph("This is the Introduction"),
        Heading("First heading", 1, [
            Paragraph("Inside heading"),
            ListElem([
                ListItem("Item 1"),
                ListItem("Item 2")
            ])
        ])
    ])))

    o1 = GUI()
    o2 = Collaborator()
    buf.doc.register_observer(o1)
    buf.doc.register_observer(o2)

    ic(list(buf.doc.content))

    buf.edit()
    ic(list(buf.doc.content))

    buf.undo()
    ic(list(buf.doc.content))

    buf.undo()
    ic(list(buf.doc.content))
