# Behavioral Design Patterns

## Author: Balan Artiom

----

## Objectives:

* Get familiar with the Design Patterns;
* Choose a specific domain;
* Implement 3 BDPs for the specific domain; 

## Used Design Patterns: 

* Observer pattern
* Iterator pattern
* Memento pattern

## Implementation

The file `observer.py` has the general-purpose classes `Observer` and `Subject` which implement the **observer pattern**.
The `Document` class inherits from `Subject`, and `GUI` and `Collaborator` inherit from `Observer`.

``` python
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
```

The document structure is represented by a tree structure, and I've used the **iterator pattern** to be able to convert it to a list.
This might be helpful, for example, to move through the document element-wise.

Iterators in Python are constructed using the `__next__` method:
``` python
    def __next__(self):
        for item in self.items:
            for i in item:
                yield i
```

I've used the **memento pattern** to implement undo history. Instead of editing a `Document` directly,
users are supposed to edit `Buffer`s, borrowing the Emacs terminology.
A `Buffer` object has an associated `Document` and stores its state (`DocumentContent` objects, which are the Mementos) in an undo list. 

``` python
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
```

## Conclusions / Screenshots / Results
Here is a sample program and the output it generates:

``` python
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
```

``` 
╰─$ ./main.py
ic| list(buf.doc.content): [Paragraph(text='This is the Introduction'),
                            Heading(text='First heading', level=1),
                            Paragraph(text='Inside heading'),
                            ListItem(text='Item 1'),
                            ListItem(text='Item 2')]
INFO: Notified GUI
INFO: Notified collaborator 'Anonymous'
INFO: Made edit
ic| list(buf.doc.content): [Paragraph(text='This is the Introduction'),
                            Heading(text='First heading', level=1),
                            Paragraph(text='Inside heading'),
                            ListItem(text='Item 1'),
                            ListItem(text='Item 2'),
                            Heading(text='New heading', level=1)]
INFO: Notified GUI
INFO: Notified collaborator 'Anonymous'
INFO: Undo edit
ic| list(buf.doc.content): [Paragraph(text='This is the Introduction'),
                            Heading(text='First heading', level=1),
                            Paragraph(text='Inside heading'),
                            ListItem(text='Item 1'),
                            ListItem(text='Item 2')]
INFO: Nothing to undo
ic| list(buf.doc.content): [Paragraph(text='This is the Introduction'),
                            Heading(text='First heading', level=1),
                            Paragraph(text='Inside heading'),
                            ListItem(text='Item 1'),
                            ListItem(text='Item 2')]
```
