from . import builder,instance

__all__=[
    "builder",
    "instance"
]

def handle_exit():
    instance.getAriaProcess().terminate()
    from os import _exit
    _exit(0)
    
def generate_lines(*args):
    for arg in args:
        for line in arg.splitlines():
            instance.getLogger().error(line)
    handle_exit()