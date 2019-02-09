# Brings the magic of "without loss of generality" to Python programs.
# Christopher Siu (cesiu@calpoly.edu)

import itertools
import inspect
import ctypes


# Encapsulates WLOG functionality in a context manager so that it can be
#  invoked using the existing 'with' keyword.
class out_loss_of_generality:
    def __init__(self, predicate):
        self.predicate = predicate
        self.shadowed = {}

    # Tries to rebind identifiers in the caller's environment to satisfy the
    #  given predicate.
    def __enter__(self):
        # Get the caller's local and global environments.
        frame = inspect.stack()[1].frame
        local_env = frame.f_locals
        global_env = frame.f_globals
        environment = global_env.copy()
        environment.update(local_env)

        # Figure out which local bindings we might need to change.
        identifiers = list(inspect.signature(self.predicate).parameters.keys())
        for identifier in identifiers:
            if identifier in local_env:
                self.shadowed[identifier] = local_env[identifier]
            elif identifier in global_env:
                raise Exception("Error: '%s' is global." % identifier)
            else:
                raise Exception("Error: '%s' is unbound." % identifier)

        # First, try all permutations of locals, then, of all values.
        if not self.shadow(
               identifiers, local_env, local_env, environment, frame) \
           and not self.shadow(
               identifiers, local_env, environment, environment, frame):
            raise Exception("Error: No satisfying assignments found.")

    # Tries all permutations of a given set of bindings, committing the first
    #  that satifies the given predicate.
    # Returns true if a satisfying assignment was found, false otherwise.
    def shadow(self, identifiers, dest_env, src_env, environment, frame):
        for bindings in itertools.permutations(src_env, len(identifiers)):
            try:
                if self.predicate(*(src_env[binding] for binding in bindings)):
                    for identifier, binding in zip(identifiers, bindings):
                        dest_env[identifier] = environment[binding]
                        ctypes.pythonapi.PyFrame_LocalsToFast(
                         ctypes.py_object(frame), ctypes.c_int(0))
                    return True
            except:
                pass
        return False

    # Restores bindings changed by the context manager.
    def __exit__(self, exc_type, exc_value, traceback):
        # Restore the caller's local environment
        frame = inspect.stack()[1].frame
        local_env = frame.f_locals

        for identifier in self.shadowed:
            local_env[identifier] = self.shadowed[identifier]
            ctypes.pythonapi.PyFrame_LocalsToFast(
             ctypes.py_object(frame), ctypes.c_int(0))
