import time

class Timer(object):
    """ 
    To time how long a particular function runs.

    Example:
        import Timer
        with Timer() as t:
            somefunction()
        print("somefunction() takes %s seconds" % t.secs)
        print("somefunction() takes %s milliseconds" % t.msecs)
    """

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000