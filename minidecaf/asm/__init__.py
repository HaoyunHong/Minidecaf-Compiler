from .command import *


class AsmEmitter:
    def __init__(self, fout):
        self.f = fout

    def emit(self, com):
        print(f"{com}", file=self.f)

    def __call__(self, coms):
        for com in coms:
            self.emit(com)
