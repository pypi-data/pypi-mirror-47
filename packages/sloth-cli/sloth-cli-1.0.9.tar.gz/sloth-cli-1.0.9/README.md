# sloth-cli

![logo](docs/sloth.jpg)

A library to speed the profile (cProfile) analyses of code performance on a per
line basis. This library allow the user to call a python script file with 
arguments and analyse what lines of code are taking longer to process.

An example output of the `sloth-cli`:

```shell
Sat Jun  8 11:56:40 2019    profileOutput.profile

         5400 function calls (5340 primitive calls) in 3.017 seconds

   Ordered by: cumulative time
   List reduced from 352 to 100 due to restriction <100>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      4/1    0.000    0.000    3.017    3.017 {built-in method builtins.exec}
        1    0.000    0.000    3.017    3.017 tester.py:1(<module>)
        1    0.000    0.000    3.014    3.014 tester.py:21(run)
        3    3.012    1.004    3.012    1.004 {built-in method time.sleep}
``` 

## Install

```
pip install sloth-cli
```

## Usage

Using a `tester.py` cli script (argsparse):

### To run `tester.py` with arguments:

```bash
sloth -f tester.py --cmd fake --fake-arg test
```

### To get the `tester.py` help:

```bash
sloth -f tester.py -l 100 --cmd --help
```
