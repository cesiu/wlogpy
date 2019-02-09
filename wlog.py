import itertools
import inspect
import ctypes


class out_loss_of_generality:
    def __init__(self, predicate):
        self.predicate = predicate
        self.shadowed_locals = {}
        self.shadowed_globals = {}

    def __enter__(self):
        # Get the parent's local and global environments.
        frame = inspect.stack()[1].frame
        local_env = frame.f_locals
        global_env = globals()
        environment = global_env.copy()
        environment.update(local_env)

        # Figure out which bindings we might need to change.
        identifiers = list(inspect.signature(self.predicate).parameters.keys())
        for identifier in identifiers:
            if identifier in local_env:
                self.shadowed_locals[identifier] = local_env[identifier]
            elif identifier in global_env:
                self.shadowed_globals[identifier] = global_env[identifier]
            else:
                raise Exception("Error: Identifier '%s' unbound." % identifier)

        # First, try all permutations of locals only.
        for bindings in itertools.permutations(local_env, len(identifiers)):
            try:
                if self.predicate(*(local_env[binding]
                                    for binding in bindings)):
                    for identifier, binding in zip(identifiers, bindings):
                        local_env[identifier] = environment[binding]
                        ctypes.pythonapi.PyFrame_LocalsToFast(
                         ctypes.py_object(frame), ctypes.c_int(0))
                    return
            except TypeError:
                pass

        # Then, try all permutations of all values in the environment.
        for bindings in itertools.permutations(environment, len(identifiers)):
            try:
                if self.predicate(*(environment[binding]
                                    for binding in bindings)):
                    for identifier, binding in zip(identifiers, bindings):
                        local_env[identifier] = environment[binding]
                        ctypes.pythonapi.PyFrame_LocalsToFast(
                         ctypes.py_object(frame), ctypes.c_int(0))
                    return
            except TypeError:
                pass

        raise Exception("Error: No satisfying assignments found.")

    def __exit__(self, exc_type, exc_value, traceback):
        # Restore the parent's local and global environments
        frame = inspect.stack()[1].frame
        local_env = frame.f_locals
        global_env = globals()

        for identifier in self.shadowed_locals:
            local_env[identifier] = self.shadowed_locals[identifier]
            ctypes.pythonapi.PyFrame_LocalsToFast(
             ctypes.py_object(frame), ctypes.c_int(0))

        for identifier in self.shadowed_globals:
            global_env[identifier] = self.shadowed_globals[identifier]

x = 0
w = 4

def main():
    x = 1
    y = 2
    z = 3

    print("Before -- x: %d y: %d z: %d w: %d" % (x, y, z, w))

    with out_loss_of_generality(lambda x, y: x > y):
        print("During -- x: %d y: %d z: %d w: %d" % (x, y, z, w))
        z = 4
        print("During -- x: %d y: %d z: %d w: %d" % (x, y, z, w))

    print("After  -- x: %d y: %d z: %d w: %d" % (x, y, z, w))


if __name__ == "__main__":
    main()
