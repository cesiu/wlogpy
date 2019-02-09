## wlog.py

Consider the following proof:

> _Proposition:_
> `x + y` is odd whenever `x` and `y` are integers of opposite parity.
>
> _Proof:_
> Let `x` and `y` be integers of opposite parity. Without loss of generality,
> suppose `x` is even and `y` is odd. Then there exist integers `k` and `l`
> such that `x = 2k` and `y = 2l + 1`, thus, `x + y = 2k + 2l + 1 = 2(k + l) + 1`,
> which is odd. ∎

This proof is made half-as-verbose through the use of the phrase "without loss
of generality", allowing the writer to trust his readers to mentally fill in
the blanks and apply the single given argument to any other cases.

Now, you can bring the same magic to Python, allowing programmers to trust the
interpreter to implicitly fill in the blanks and adjust any other cases to work
with a single given block of code:

```python
>>> from wlog import *
>>> x = 327
>>> y = 94
>>> with out_loss_of_generality(lambda x, y: x % 2 == 0 and y % 2 == 1):
...     print("x: %d" % x)
...     print("y: %d" % y)
... 
x: 94
y: 327
>>> x
327
>>> y
94
```
