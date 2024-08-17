from enum import Enum

# from typing import Optional
# from beaupy import select

class Framework(Enum):
    React = 'React'
    Remix = 'Remix'
    Next = 'Next'
    Svelte = 'Svelte'
    SvelteKit = 'SvelteKit'
    Astro = 'Astro'

# def ask():
#     print("Choose your framework:")
#     selected: Optional[Framework] = select(
#         list(Framework),
#         preprocessor=lambda x: x.value
#     )
    
#     if selected is None:
#         raise Exception("Invalid input")

#     return selected
