from json import dumps
from requests import Session
from csv import reader
from sys import argv
from sys import exit
from argparse import ArgumentParser


class HackedEmailstoDradis(object):
    def __init__(self):
        self.arg = self.parse_args()
        self.emails = []
        self.apihitcounter = 0
        self.session = Session()

        # ConnectWise API Configuration
        self.connectwise_company_name = "xxxxxxxxxx"
        self.connectwise_public_api_key = "xxxxxxxxxxxx"
        self.connectwise_private_api_key = "xxxxxxxxxxx"
        self.connectwise_api_site = "xxxxxxxxxxx"
        self.connectwise_all_companies_site = self.connectwise_api_site +  '/company/contacts?pageSize=1000'
        self.connectwise_one_company_site = self.connectwise_api_site + '/company/contacts?conditions=company/identifier like "{0}"& pageSize=1000'
        # Dradis API Configuration
        self.dradis_api_token = 'xxxxxxxxxxxxxxx'
        self.dradis_project_id = '0'
        self.dradis_issues_url = 'https://dradis-pro.dev/pro/api/issues'

    def run(self):
        self.emails = self.get_emails()
        if not isinstance(self.emails[0], dict):
            self.csv_hacked_emails_to_dradis(self.emails)
        else:
            self.connectwise_hacked_emails_to_dradis(self.emails)
        return 0

    def get_emails(self):
        if ".csv" in self.arg.CompanyID_or_CSVFilename:
            contacts = []
            try:
                with open(self.arg.CompanyID_or_CSVFilename) as csvfile:
                    mycsv = reader(csvfile, delimiter=',')
                    for row in mycsv:
                        for cell in row:
                            if "@" in cell:
                                print(cell)
                                contacts.append(cell)
            except Exception as e:
                print(e)
                exit(-1)
            return contacts
        elif self.arg.CompanyID_or_CSVFilename == 'all':
            self.session.auth = (self.connectwise_company_name  + '+{0}'.format(self.connectwise_public_api_key),
                                 self.connectwise_private_api_key)
            contacts = self.session.get(self.connectwise_all_companies_site)
            if contacts.status_code != 200:
                print(self.arg.CompanyID_or_CSVFilename + ' - ' + contacts.text)
                exit(-1)
            self.session.auth = None
            return contacts.json()
        else:
            self.session.auth = (self.connectwise_company_name  + '+{0}'.format(self.connectwise_public_api_key),
                                 self.connectwise_private_api_key)
            contacts = self.session.get(self.connectwise_one_company_site.format(self.arg.CompanyID_or_CSVFilename))
            if contacts.status_code != 200:
                print(self.arg.CompanyID_or_CSVFilename + ' - ' + contacts.text)
                exit(-1)
            self.session.auth = None
            return contacts.json()

    def csv_hacked_emails_to_dradis(self, emails):
        for email in emails:
            if self.apihitcounter == 100:
                    print("The hacked-emails API limit is 100. The script will now exit.")
                    exit(-1) 
            hacked_email = self.session.get("https://hacked-emails.com/api?q={0}".format(email))
             self.counter += 1
            if hacked_email.status_code != 200:
                print(email + hacked_email.text)
                continue
            elif hacked_email.json()['status'] == "notfound":
                continue
            else:
                self.session.headers.update({'Authorization': 'Token token="{0}"'.format(self.dradis_api_token)})
                self.session.headers.update({'Dradis-Project-Id': self.dradis_project_id})
                self.session.headers.update({'Content-type': 'application/json'})
                _data = ""
                for d in hacked_email.json()['data']:
                    _data += (
                    str(d['title']) + ' -- Date_Leaked: ' + str(d['date_leaked']) + ' -- Source_Network: ' + str(
                        d['source_network']) + '\r\n')
                data = {'issue': {
                        'text': '#[Title]#\r\n' + email + ' - hacked-emails.com\r\n\r\n#[Results]#\r\n' + str(
                            hacked_email.json()['results']) + "\r\n\r\n" + _data + "\r\n\r\n"}}
                dradis = self.session.post(self.dradis_issues_url, data=dumps(data), verify=False)
                print(email + ' ' + str(dradis.status_code))
                self.session.headers.clear()

    def connectwise_hacked_emails_to_dradis(self, emails):
        for contact in emails:
            email = None
            if contact['communicationItems']:
                for ci in contact['communicationItems']:
                    if ci['type']['name'] == "Email":
                        email = ci['value']
                if email is None:
                    continue
                if self.apihitcounter == 100:
                    print("The hacked-emails API limit is 100. The script will now exit.")
                    exit(-1)
                hacked_email = self.session.get("https://hacked-emails.com/api?q={0}".format(email))
                 self.counter += 1
                if hacked_email.status_code != 200:
                    print(email + hacked_email.text)
                    continue
                elif hacked_email.json()['status'] == "notfound":
                    continue
                else:
                    self.session.headers.update({'Authorization': 'Token token="{0}"'.format(self.dradis_api_token)})
                    self.session.headers.update({'Dradis-Project-Id': self.dradis_project_id})
                    self.session.headers.update({'Content-type': 'application/json'})
                    _data = ""
                    for d in hacked_email.json()['data']:
                        # fields in hacked_email.json()['data'] are used when formatting the issue
                        _data += (
                        str(d['title']) + ' -- Date_Leaked: ' + str(d['date_leaked']) + ' -- Source_Network: ' + str(
                            d['source_network']) + '\r\n')
                    data = {'issue': {
                        'text': '#[Title]#\r\n' + email + ' - hacked-emails.com\r\n\r\n#[Results]#\r\n' + str(
                            hacked_email.json()['results']) + "\r\n\r\n" + _data + "\r\n\r\n"}}
                    dradis = self.session.post(self.dradis_issues_url, data=dumps(data), verify=False)
                    print(email + ' - ' + str(dradis.status_code))
                    self.session.headers.clear()
            else:
                continue

    def parse_args(self):
        # parse the arguments
        parser = ArgumentParser(epilog='\tExample: \r\npython ' + argv[0] + " -CompanyID_or_CSVFilename",
                                         description="Check contacts' or csv of emails in the hacked-emails API and "
                                                     "export the results to Dradis as issues")
        parser._optionals.title = "OPTIONS"
        parser.add_argument('CompanyID_or_CSVFilename', help="ConnectWise Company ID or CSV of emails")
        return parser.parse_args()

if __name__ == "__main__":
    a = HackedEmailstoDradis()
    a.run()
