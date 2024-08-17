from enum import Enum
from typing import Optional
from beaupy import select

class Langauge(Enum):
    Js = 'JavaScript'
    Ts = 'TypeScript'

def ask():
    print("Choose your langauge:")
    selected: Optional[Langauge] = select(
        list(Langauge),
        preprocessor=lambda x: x.value
    )
    
    if selected is None:
        raise Exception("Invalid input")

    return selected
