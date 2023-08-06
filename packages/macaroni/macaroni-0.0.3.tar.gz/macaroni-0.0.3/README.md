# Py-Macaroni

This is a library to help you avoid
[Spaghetti Code](https://en.wikipedia.org/wiki/Spaghetti_code). It helps you
express your application logic in a testable way. The whole idea for this lib
was based on some concepts from functional programming and rust, mainly the
"unwrap" concept from rust.

## Why

When creating bussiness logic for your application, sometimes it gets hard to
structure complex logic in a easy to understand way. To help with that, this
library was created. The main objective is to help you structure your
application in a clean and readable way, enabling future maintenance of the
code.

For example, if you have a CRUD application, some logic will be shared between
the Create and Update functions, the lib, in this case, can help by chaining
functions required to implement the main bussiness rule, and makes it easier to
reuse functions when required.

```python
import macaroni as mci

class BussinessLogic(mci.Macaroni):
    def validate_request(self, data):
        # ...

    def check_user_permissions(self, data):
        # ...

    def log_operation(self, data):
        # ...

    def create_item(self, data):
        # ...

    def update_item(self, data):
        # ...

    @mci.error
    def handle_error(self, data, error):
        # ...

    @mci.exception(DuplicateKey)
    def handle_duplicate_item(self, data, exception):
        # ...


def create_item(data):
    bl = BussinessLogic(data)
    result = (
        bl.validate_request()
        .check_user_permissions()
        .create_item()
        .log_operation()
        .handle_error()
        .handle_duplicate_item()
        .unwrap()
    )
    return result


def update_item(data):
    bl = BussinessLogic(data)
    result = (
        bl.validate_request()
        .check_user_permissions()
        .update_item()
        .log_operation()
        .handle_error()
        .unwrap()
    )
    return result
```

It also helps you avoid dealing with error and exception handling on each part
of your application logic, letting you handle then only at the end of the
application execution, automatically skipping steps in your application logic
when an error or exception happens.

## Installation

```
pip install macaroni
```

## Usage

More examples can be found in the [./examples](./examples) directory.

```python
import macaroni as mci

class Calculator(mci.Macaroni):
    def increment(self, value, increment=None):
        if increment is None:
            increment = 1

        return value + increment

    def divide(self, value, denominator):
        if denominator == 0:
            return mci.Error('invalid denominator {0}'.format(denominator))

        return value / denominator

    def invalid(self, value):
        raise ValueError('invalid data')


base_val = 10
calc = Calcultator(base_val)
result = calc \
    .increment(2) \
    .divide(2) \
    .unwrap() # this returns the final result
assert result == 6
```

Error handling:

```python
calc = Calculator(10)
result = calc \
    .increment(2) # this is executed \
    .divide(-3) # this causes an error \
    .increment() # this is not executed \
    .unwrap() # returns the error

assert bool(calc.error) == True
assert result == 'invalid denominator 0'
```

Exception handling:

```python
calc = Calculator(10)
try:
    calc \
        .increment(2) # this is executed \
        .invalid() # this causes an exception \
        .increment() # this is not executed \
        .unwrap() # the exception ValueError is raised on unwrap
except ValueError:
    pass

assert bool(calc.exception) == True
```

When testing, you can use the parameter `magic=False` to disable the automatic value passing, chaining and error/exception handling:

```python
def test_increment():
    calc = Calculator(magic=False)
    result = calc.increment(10, 2)
    assert result == 12

def test_error():
    calc = Calculator(magic=False)
    result = calc.divide(10, 0)
    assert calc.error is not None
    assert result = 'invalid denominator 0'

def test_exception()
    calc = Calculator(magic=False)

    raised_error = False
    try:
        calc.invalid(10)
    except ValueError:
        raised_error = True

    assert raised_error
```
