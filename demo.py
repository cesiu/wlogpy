from wlog import *

x = 327
y = 94

with out_loss_of_generality(lambda x, y: x % 2 == 0 and y % 2 == 1):
    print("x: %d\ny: %d" % (x, y))
