import inspect
import itertools


class out_log:
    def __init__(self, predicate, *bindings):
        self.predicate = predicate
        self.bindings = bindings

    def __enter__(self):
        #inspect.stack()
        for binding in itertools.permutations(self.bindings):
            if self.predicate(*binding):
                return binding

        raise Exception("You have lost generality.")

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def main():
    x = 1
    y = 2
    z = 3

    print("x: %d y: %d z: %d" % (x, y, z))

    with out_log(lambda x, y: x > y, x, y) as (x, y):
        print("x: %d y: %d z: %d" % (x, y, z))


if __name__ == "__main__":
    main()
