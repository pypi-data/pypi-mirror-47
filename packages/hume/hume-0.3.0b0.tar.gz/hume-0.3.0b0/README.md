# hume - simple & quick profiling for mortals


## Installation

You can install 'hume` from [PyPI](https://pypi.org/):

    pip install hume

**Note:** Python >= 3.6 required.

## ★ hume.decorators

### ★★ profile

A simple decorator to measure function execution times. 

- Supports N simulations and average times. 
- Supports, recognizes, and reports recursive functions.
- (optional) List `args` and `kwargs` as provided to the decorated function.
- (optional) Display the decorated function's return value
- (optional) Supress `print` statements in decorated functions (default is `False`, output is only reported for one simulation)

#### ★★★ how to use

Simply decorate any function:

```python
from hume.decorators import profile

@profile(nums=3)
def slow_add(num):
    """slow_add does somethig
    """
    time.sleep(1)
    return num

print(slow_add(3))
```

And let it do its job:

```terminal
profiling slow_add 
------------
→ name: slow_add
→ simulations: 3
→ average execution time: 1.0033866766666666 seconds

3
```

`profile` supports the following params:

- `nums: int = 1` → how many simulations to conduct
- `show_args: bool = False` → display `args` passed to the decorated function
- `show_kwargs: bool = False` →  display `kwargs` passed to the decorated function
- `show_result: bool = False` →  display decorated function return value
- `mute_console: bool = False` →  supress `print` statements from the decorated function

#### ★★★ recursion

For recursive functions, `profile` just knows (and doesn't pollute the console):

```python
# recursive function
@profile(7)
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)


print(factorial(3))
```

```terminal
profiling factorial (recursive function detected) 
------------
→ name: factorial
→ simulations: 7
→ average execution time: 3.6912857141706875e-06 seconds

6
```

#### ★★★ colorized output

Output is colorized:

![console output demo](/docs/console_demo.png)