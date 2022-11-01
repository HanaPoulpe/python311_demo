# Python 3.11 new features demo
This package is designed to show the new features in python 3.11.

Files that helps understand the changes are placed in ```./scr/``` with files named after the PEP changes.

## General Changes:
All of those changes a mainly small improvements coming from this new version of Python.

### [PEP 657](https://www.python.org/dev/peps/pep-0657/): Fined grained error location
This one is pretty useful for debugging: messages for syntax errors now display the exact position of the error.

In previous versions, error messages looked like:
```
Traceback (most recent call last):
  File "/home/hana/PycharmProjects/python311_demo/src/pep657.py", line 13, in <module>
    main()
  File "/home/hana/PycharmProjects/python311_demo/src/pep657.py", line 9, in main
    print(o.missing_attribute)
AttributeError: 'MyClass' object has no attribute 'missing_attribute'
```

The new output:
```
Traceback (most recent call last):
  File "/home/hana/PycharmProjects/python311_demo/src/pep657.py", line 13, in <module>
    main()
  File "/home/hana/PycharmProjects/python311_demo/src/pep657.py", line 9, in main
    print(o.missing_attribute)
          ^^^^^^^^^^^^^^^^^^^
AttributeError: 'MyClass' object has no attribute 'missing_attribute'
```

As you can see, the new error messages points you to the exact position of the error.

### [PEP 654](https://www.python.org/dev/peps/pep-0654/): Exception Groups
I think this one is nice, but also dangerous if badly used.

In short, python now supports exception groups with ```except*``` and/or ```except ExceptionGroup```.
Those exception groups allows to propagate multiple exceptions at the same time.

I see few uses of exception groups:
1. The first one is if you face an issue within the recovery of a previous exception. A workflow like this one could go like:
   1. Let's say you want to store data in a database, the transaction fails due to a dead lock.
   2. While trying to rollback, the database throws another exception to you.

The exception groups allows you to send both exceptions back to your exception handler, and to log both exceptions together.

2. The second one is handling multiple exception from coroutine (see TaskGroup).
2. The last one would be with dependency inversion, and I want to address this because I see how it could be appealing because it's new feature you want to use 
   1. The exception will be raised deep in the execution stack, at a place where your code is not aware of the specific exception.
   2. Your code will most likely throw a new exception, proceed with general recovery actions and propagate the exception.
   3. Exception groups will allow your code to handle both exception classes to perform all recovery actions.

If this example feels farfetch, it's because it is and I would not recommend this usage.
If your design requires this behaviour, either the specific recovery needs to be handled in the interface functions that will raise exceptions that can be handled on a generic way.
If you need some context to handle those exceptions, quick fixes could be:
* pass the context to the working function.
* review your design to provide a context manager that will ensure in context clean up on exceptions

Both solution will provide a more understandable solution.

### [PEP 680](https://www.python.org/dev/peps/pep-0680/): tomllib is now part of Python standard library.
Python now onboards natively TOML lib support, this library works the same way as JSon, providing ```load```, ```loads```.

The conversion to Python objects will automatically convert values to any standard native datastructures, including:
```str```, ```int```, ```float```, ```bool```, ```datetime.{datetime, date, time}```, ```list```, ```dict``` with string keys.

If you want more documentation about TOML format: please refer to the documentation at [toml.io](https://toml.io/en/).

### [GH-90908](https://github.com/python/cpython/issues/90908): Task Groups
Tasks Group are a nice and easy to handle multiple tasks, you can add tasks within a ```with TaskGroup() as g:``` block,
once you exist the block, it will wait until all tasks have completed, any exceptions will be propagated in an ExceptionGroup.

### [GH-34627](https://github.com/python/cpython/issues/34627/): [Atomic groups and possessive quantifier](https://www.regular-expressions.info/atomic.html) for Regular expressions
This one is a bit complex to explain as it's not exactly python related but regex support, I'll try to be really light on details, you have the link to the complete usage.

When evaluating a regular expression, by time, when entering a group the algorithm will back track, for atomic groups,
when backtracking, the match for the group cannot be changes. This is more used to optimize matching as having an atomic group like ```(?>include|insert|in)``` will be faster when backtracking
but be cautious, because if you write it ```(?>in|include|insert)``` will never match include or insert as on the first pass it will match ```in```.

Possessive quantifier are some of the same effect, by default quantifiers are greedy, will match as much occurrences as possible, then giving up at each back track.
Possessive quantifiers will not give up matching and always force the longest sub string possible before checking the next part of the expression.

### CPython optimizations:
If you are using CPython, which is most likely the case, you should see a 10 to 60% improvements on execution times.

## Typing Changes
This changes are specific to typing and type hints.

### [PEP 673](https://www.python.org/dev/peps/pep-0673/): Self type:
When working with a class you can use the type Self in type hints, it indicates an the class being defined.
This is really nice to have, as it allows your class to self reference without ```from __future__ import annotation``` or using string type name like:

```python
class MyClass:
    def do_something(self) -> 'MyClass':
        ...
```

Now it will look like:
```python
class MyClass:
    def do_something(self) -> Self:
        ...
```

### [PEP 646](https://peps.python.org/pep-0646/): Variadic Generics:
This one is really for working with generics:

You can use generic like:
```python
T1 = TypeVar("T1")
T2 = TypeVar("T2")

def to_tuple(v: Generic[T1, T2]) -> Tuple[T1, T2]:
    ...
```
to work with a generic type that have 2 parameters types, like ```dict[str, int]```.

But it's possible that you don't know how many parameters you will face for a generic.

Let's put a simple example of functions that works with shape
```python
Shape = TypeVarTuple("Shape")

def to_tuple(v: Generic[Shape]) -> Tuple[*Shape]:
    ...
```
This new example will enable to work with generic types with unknown parameters count.

### [PEP 675](https://www.python.org/dev/peps/pep-0675/): Literal Strings
This one is a great security feature, we remember last's year Log4J security issue, and a good way to ensure that critical parts
of our execution are safe from injection is to enforce using literal strings instead of constructed strings.

An good example is for queries:

```python
def execute(connection: Connection, sql: LiteralString, parameters: Iterable[str])...
```

### [PEP 655](https://peps.python.org/pep-0655/): Required dict member for TypeDict
When using TypeDict, previously it was all or nothing when defining the types:
```python
class All(TypedDict):
    year: int
    month: int

class Nothing(TypedDict, total=False):
    year: int
    month: int
```
In the first example, you will need both year and month to create a new All class. \
In the second, no attributes are required for Nothing

It was possible to create a 2 level hierarchy combining ```total = True``` and ```total = False``` to set part of the attributes
mandatory and other not, but it's quite dirty.

Not you can use:
```python
class Part(TypedDict):
   mandatoy: str
   not_mandatory: NotRequired[str]
```

### [PEP 681](https://peps.python.org/pep-0681/): Dataclass transform
A bit of context here: dataclasses are a metaclass that helps you deal with data oriented classes.
Using dataclass decorator, ```__init__```, ```__hash__```, ```__eq__``` and other dunder methods can be generated.

All the dunder methods are following the same logic, you would need to provide arguments in your dataclass definition to not create said methods,
then define all of them in your dataclass definition that kind of defeat the goal of dataclasses.

Dataclass transform is  a way to provide your implementation to those classes to create a new dataclass decorator that will 
use your defined implementation for any of those methods you need to override.

```python
T = TypeVar("T")

@dataclass_transform
def overwrites_eq_dataclass(cls: Type[T]) -> Type[T]:
    cls.__eq__ = lambda self, o: self.id == o.id
    return cls

@overwrites_eq_dataclass
class DataclassWithId:
    id: str
    name: str

print(DataclassWithId("my_id", "name1") == DataclassWithId("my_id", "name2"))
# Will return True
```

This is a quick example of possibilities, even if this feature is not a massive improvements, it can really be useful in certain situations.
