import copy
import itertools
import inspect
import ctypes


class out_loss_of_generality:
    def __init__(self, predicate, *bindings):
        self.predicate = predicate
        self.bindings = bindings

    def __enter__(self):
        # Get the parent's frame and save the existing scope.
        scope = inspect.stack()[1].frame
        self.saved = copy.deepcopy(scope.f_locals)
        self.shadowed = []

        # Figure out which locals we might want to change.
        bindings = list(inspect.signature(self.predicate).parameters.keys())
        for binding in bindings:
            if binding not in scope.f_locals:
                raise Exception("Error: '%s' unbound." % binding)
            else:
                self.shadowed.append(binding)

        # Try all the permutations of locals.
        for locals in itertools.permutations(scope.f_locals, len(bindings)):
            if self.predicate(*(scope.f_locals[local] for local in locals)):
                for binding, local in zip(bindings, locals):
                    scope.f_locals[binding] = self.saved[local]
                    ctypes.pythonapi.PyFrame_LocalsToFast(
                     ctypes.py_object(scope), ctypes.c_int(0))
                break
        else:
            raise Exception("Error: lost generality.")


    def __exit__(self, exc_type, exc_value, traceback):
        # Get the parent's frame and restore the old scope.
        scope = inspect.stack()[1].frame

        for binding in self.shadowed:
            scope.f_locals[binding] = self.saved[binding]
            ctypes.pythonapi.PyFrame_LocalsToFast(
             ctypes.py_object(scope), ctypes.c_int(0))


def main():
    x = 1
    y = 2
    z = 3

    print("Before -- x: %d y: %d z: %d" % (x, y, z))

    with out_loss_of_generality(lambda x, y: x > y):
        print("During -- x: %d y: %d z: %d" % (x, y, z))
        z = 4
        print("During -- x: %d y: %d z: %d" % (x, y, z))

    print("After  -- x: %d y: %d z: %d" % (x, y, z))


if __name__ == "__main__":
    main()
