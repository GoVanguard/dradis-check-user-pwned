
## About check-user-pwned-dradis
check-user-pwned-dradis is a python tool that searches a list of emails across multiple data breaches to see if it has been compromised and then imports findings into Dradis as issues. It checks emails from your contacts in ConnectWise or a csv. 

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

## Script Configuration

#### Connectwise API
For ConnectWise you will need to edit the following variables: self.connectwise_company_name, self.connectwise_public_api_key,        self.connectwise_private_api_key, self.connectwise_api_site.
self.connectwise_company_name is the name of your company in ConnectWise.
self.connectwise_public_api_key and self.connectwise_private_api_key can be found in one of your ConnectWise member accounts.
self.connectwise_api_site is your ConnectWise url with several modifications.
For more ConnectWise API information go to: https://developer.connectwise.com


#### Dradis API
For Dradis you need to edit the following variables: self.dradis_api_token, self.dradis_project_id, self.dradis_issues_url
self.dradis_issues_url should be the url of your Dradis server with '/pro/api/issues' added on the end. 
self.dradis_project_id is the project id of the project that you will import issues into. You can find this number when you click on     your project
self.dradis_api_token can be found by going to your dradis server's account settings which is your url with'pro/profile' added on.
For more  Dradis API information go to: https://dradisframework.com/pro/support/guides/rest_api/


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

check-user-pwned-dradis is licensed under the GNU Affero General Public License v3.0. Take a look at the [LICENSE](https://github.com/GoVanguard/check-user-pwned-dradis/blob/master/LICENSE) for more information.

## Version
**Current version is 1.0**
