# hume - simple & quick profiling for mere mortals

hume is a fun-expirement turned Python package. In short, it exposes a decorator `profile` that you can use to measure 
the execution time of functions. It goes out of its way to make its protocol clear, usage simple, and configuration flexible. 

Like many profiling libraries, hume adds overhead which means its measurements are (often) slower than real execution time when testing small pieces of code. **Don't** use it for super-scientific benchmarking.

**Note:** Python >= 3.6 required.

## Installation

You can install `hume` from [PyPI](https://pypi.org/):

    pip install hume

or:

    pipenv install hume

## ★ hume.decorators

### ★★ profile

A simple decorator to measure function execution times. 

- Supports N simulations and average times. 
- Supports, recognizes, and reports recursive functions.
- (optional) List `args` and `kwargs` as provided to the decorated function.
- (optional) Display the decorated function's return value
- (optional) Supress `print` statements in decorated functions (default is `False`, output is only reported for one simulation)


`profile` does not in any way modify what's returned by the decorated function. The only thing it will possibly augment are `print` statements.

#### ★★★ usage

Simply decorate any function:

```python
from hume.decorators import profile

@profile(6)
def slow_add(num):
    """
    slow_add sleeps one second and returns num + 1
    """

    time.sleep(1)
    return num + 1

print(slow_add(3))
```

And let it do its job:

```terminal
profiling slow_add 
------------------------------------------------
→ name: slow_add
→ simulations: 6
→ average execution time: 1.0034156345 seconds

4
```

#### ★★★ options and defaults

`profile` supports the following params:

- `nums: int = 1` → how many simulations to conduct
- `show_args: bool = False` → display `args` passed to the decorated function
- `show_kwargs: bool = False` →  display `kwargs` passed to the decorated function
- `show_result: bool = False` →  display decorated function return value
- `mute_console: bool = False` →  supress `print` statements inside the decorated function's body. Useful when you have a bunch of these that you don't want to remove just for the sake of measurement.<sup>1</sup>

<span style="font-size:12px;"><sup>1</sup> Even if `mute_console` is `False`, recursive functions will print normally and not per `nums`.</small>

#### ★★★ recursion

For recursive functions, `profile` just knows (and doesn't pollute the console):

```python
# recursive function
@profile(2)
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)


factorial(3)
```

```terminal
profiling factorial (recursive function detected) 
------------------------------------------------
→ name: factorial
→ simulations: 2
→ average execution time: 0.00011469949999964868 seconds
```

#### ★★★ changing & overriding defaults

If you don't like `profile`'s [default configuration](#-options-and-defaults), you can import the `CONFIG` dict and override them. For example, if you want `profile` to include the `return` from the decorated function by default, you would do the following:

```python
from hume.decorators import profile, CONFIG

CONFIG["show_results"] = True

@profile(2)
def return_one():
    return 1

# you can always override your own defaults:
@profile(show_result=False)
def return_two_ignored():
    return 2
```

#### ★★★ colorized output

Output is colorized, because priorities:

![console output demo](https://raw.githubusercontent.com/SHxKM/hume/master/docs/console_demo.png?token=ABSE3IVTPJ6CWFRQUHSW75C47APAU)