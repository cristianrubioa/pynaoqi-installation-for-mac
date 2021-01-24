# Classes useful for Expressiveness

# Class to start stop Thinking Expression with RAII pattern
class ScopedThinkingExpression():
    def __init__(self, expr):
        self.expr = expr

    def __enter__(self):
        self.expr.start()

    def __exit__(self, type, value, traceback):
        self.expr.stop()
