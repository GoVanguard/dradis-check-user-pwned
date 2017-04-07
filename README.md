
## About check-user-pwned-dradis
check-user-pwned-dradis is a python tool that searches a list of emails across multiple data breaches to see if it has been compromised and then imports findings into Dradis as issues.

## Installation

```
git clone https://github.com/GoVanguard/check-user-pwned-dradis.git
```

## Recommended Python Version:

check-user-pwned-dradis currently supports **Python 3**.

* The recommened version for Python 3 is **3.6.x**

## Dependencies:

check-user-pwned-dradis depends on the `requests`, `csv` and `argparse` python modules.

Each module can be installed independently as shown below.

#### Requests Module (http://docs.python-requests.org/en/latest/)

- Install for Windows:
```
c:\python27\python.exe -m pip install requests
```

- Install for Ubuntu/Debian:
```
sudo apt-get install python-requests
```

- Install for Centos/Redhat:
```
sudo yum install python-requests
```

- Install using pip on Linux:
```
sudo pip install requests
```

#### csv Module 

- Install for Windows:
```
c:\python27\python.exe -m pip install csv
```

- Install for Ubuntu/Debian:
```
sudo apt-get install csv  
```

- Install using pip:
```
sudo pip install csv
```

#### argparse Module

- Install for Ubuntu/Debian:
```
sudo apt-get install python-argparse
```

- Install for Centos/Redhat:
```
sudo yum install python-argparse
``` 

- Install using pip:
```
sudo pip install argparse
```

## Usage

Option        | Description
------------- | -------------------------------------------------
CompanyID     | ConnectWise Company ID of the contacts' emails that will be checked
All           | All ConnectWise Company Contacts will be checked
&#42;.csv     | Filename of .csv with emails that will be checked 

### Examples

* To see the usage syntax use -h switch:

```python hackedemails.py -h```

* To check the emails of a specific company in ConnectWise:

``python hackedemails.py GVIT``

* To check the emails of all company contacts in ConnectWise:

``python  hackedemails.py all``

* To check the emails that are in a csv file:

``python hackedemails.py example.csv``


## License

check-user-pwned-dradis is licensed under the GNU GPL license. take a look at the [LICENSE](https://github.com/GoVanguard/check-user-pwned-dradis/blob/master/LICENSE) for more information.

## Version
**Current version is 1.0**
