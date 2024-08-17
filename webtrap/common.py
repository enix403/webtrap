from typing import Type, TypeVar, Optional
from enum import Enum

from beaupy import select

T = TypeVar('T', bound=Enum)

def select_enum(enum_class: Type[T], label: str = "Choose an option:"):
    print(label)
    
    selected: Optional[T] = select(
        list(enum_class),
        preprocessor=lambda x: x.value
    )
    
    if selected is None:
        raise Exception("Invalid input")

    return selected