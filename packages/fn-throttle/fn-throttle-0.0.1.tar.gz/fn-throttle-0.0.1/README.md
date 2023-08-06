# throttle

Standalone python function call controller

## How to use

### Install

```bash
pip3 install throttle
```

### Usage

```python
from throttle import task


# two consequence foo calling own at least 0.1 second interval
@task(min_interval=0.1)
def foo(*args, **kwargs):
    print(args, kwargs)


foo(1, 2, 3)
```

## How it works

`throttle` builds a tiny local socket network with master-slave topology.

So any call of registered function is controller by the master node's controller algorithm.

## Controller

- MinIntervalController
- MockController

## TODOs

- Take dynamic local network construction and high availability into consideration
- More control algorithm choices

## About author

zhenninglang@163.com
