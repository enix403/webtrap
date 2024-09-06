from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

from typing import Type, TypeVar, Optional, Union
from enum import Enum

from beaupy import select

T = TypeVar('T', bound=Enum)

def select_enum(enum_class: Union[Type[T], list[T]], label: str = "Choose an option:"):
    print(label)
    
    selected: Optional[T] = select(
        list(enum_class),
        preprocessor=lambda x: x.value
    )
    
    if selected is None:
        raise Exception("Invalid input")

    return selected

skel_env = Environment(
    loader=FileSystemLoader("webtrap/skel"),
    autoescape=select_autoescape()
)

def load_skel_jinja(name: str):
    return skel_env.get_template(name)