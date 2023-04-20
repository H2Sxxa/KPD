from . import builder,instance

__all__=[
    "builder",
    "instance"
]

def handle_exit():
    instance.getAriaProcess().terminate()
    from os import _exit
    _exit(0)