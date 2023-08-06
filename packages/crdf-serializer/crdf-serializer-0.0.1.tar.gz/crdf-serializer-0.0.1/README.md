# Custom RDF Serializer Package - CRDF

## 1. Requirements 
This module requires the rdflib package installation:
> $ pip install rdflib

## 2. How to Install
For install this package execute the command in your environment:
> $ pip install crdf-serializer

or:
> $ pip install -i https://test.pypi.org/simple/ crdf-serializer


## 3. How to use

```python
class Person:
    nick = FOAF.nick
    name = FOAF.name
    email = FOAF.mbox

    @ObjectDecorator(FOAF.Person, None) # blank node
    @BindDecorator("dc", DC)
    @BindDecorator("foaf", FOAF)
    def __init__ (self, name, nick, email):
        self.nick = Literal(nick, lang="foo")
        self.name = Literal (name)
        self.email = URIRef(email) 

p = Person ("Donna Fales","donna", "mailto:donna@example.org")
```

