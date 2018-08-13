
## About check-user-pwned-dradis
check-user-pwned-dradis is a python tool that searches a CSV of emails across multiple data breaches to see if it has been compromised and then imports findings into Dradis as issues. 

## Installation

```
git clone https://github.com/GoVanguard/check-user-pwned-dradis.git
```

## Recommended Python Version:

check-user-pwned-dradis currently supports **Python 3**.

* The recommened version for Python 3 is **3.6.x**

## Dependencies:

check-user-pwned-dradis depends on the `PyDradis3`, `pyHaveIBeenPwned`, `csv` and `argparse` python modules.

Each module can be installed independently as shown below.

#### PyDradis3 Python library

- Install for Windows:
```
c:\python27\python.exe -m pip install pydradis3
```
- Install using pip on Linux:
```
sudo pip install pydradis3
```

#### pyHaveIBeenPwned Python library

- Install for Windows:
```
c:\python27\python.exe -m pip install pyHaveIBeenPwned
```
- Install using pip on Linux:
```
sudo pip install pyHaveIBeenPwned
```

#### csv Python library

- Install for Windows:
```
c:\python27\python.exe -m pip install csv
```
- Install using pip:
```
sudo pip install csv
```

#### argparse Module

- Install for Windows:
```
c:\python27\python.exe -m pip install argparse
```
- Install using pip:
```
sudo pip install argparse
```

### Examples

* To see the usage syntax and examples use HELP switch


## License

check-user-pwned-dradis is licensed under the GNU Affero General Public License v3.0. Take a look at the [LICENSE](https://github.com/GoVanguard/check-user-pwned-dradis/blob/master/LICENSE) for more information.
