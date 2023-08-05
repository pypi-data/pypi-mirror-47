import time
from decimal import Decimal

_TIMES = []


def human_time_round(exact, decimals=2):
    """Trim a float to a certain number of decimal places."""
    return round(Decimal(exact), decimals)


def human_time(runtime):
    if runtime < 1:
        return str('mms: ' + str('{:f}'.format(human_time_round(runtime * 1000))))
    elif runtime < 60:
        return str('sec: ' + str('{:f}'.format(human_time_round(runtime))))
    else:
        return str('min: ' + str('{:f}'.format(human_time_round(runtime / 60))))


class Timer:
    def __init__(self, msg=None):
        self.msg = msg
        self.start = time.time()
        self.elapsed_str = None
        self.elapsed_float = None

    def __str__(self):
        return str(self.end)

    def __float__(self):
        return float(self.elapsed_float)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.msg:
            print(self.msg, self.end)
        else:
            print(self.end)

    @property
    def end(self):
        end = time.time()
        self.elapsed_float = end - self.start
        if self.elapsed_float < 60:
            self.elapsed_str = str('sec: ' + str('{:f}'.format(self.elapsed_float)))
        else:
            self.elapsed_str = str('min: ' + str('{:f}'.format(self.elapsed_float / 60)))
        return self.elapsed_str

    @staticmethod
    def decorator(func):
        """A function timer decorator."""

        def function_timer(*args, **kwargs):
            """A nested function for timing other functions."""
            # Capture start time
            start = time.time()

            # Execute function with arguments
            value = func(*args, **kwargs)

            # Capture end time
            end = time.time()

            # Calculate run time
            runtime = human_time(end - start)
            print('{func:50} --> {time}'.format(func=func.__qualname__, time=runtime))
            _TIMES.append((func.__qualname__, runtime))
            return value

        return function_timer

    @staticmethod
    def decorator_noprint(func):
        """A function timer decorator."""

        def function_timer(*args, **kwargs):
            """A nested function for timing other functions."""
            # Capture start time
            start = time.time()

            # Execute function with arguments
            value = func(*args, **kwargs)

            # Capture end time
            end = time.time()

            # Calculate run time
            runtime = human_time(end - start)
            _TIMES.append((func.__qualname__, runtime))
            return value

        return function_timer

    @property
    def times(self):
        return _TIMES

    @staticmethod
    def print_times(class_name=None):
        for index, ft in enumerate(sorted([(func, time) for func, time in Timer().times
                                           if class_name and func.startswith(class_name)],
                                          key=lambda e: e[1])):
            func, t = ft
            print('{0}.) {1:35} --> {2}'.format(index, func, t))
