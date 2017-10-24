from json import dumps
from requests import Session
from csv import reader
from sys import argv, exit
from argparse import ArgumentParser


class HackedEmailstoDradis(object):
    def __init__(self):
        self.arg = self.parse_args()
        print(len(argv))
        if len(argv) < 5:
            print("wrong argument amount. see HELP")
            exit(-5)
        if ".csv" not in self.arg.CompanyID_or_CSVFilename:
            if len(argv) != 13:
                print("wrong argument amount for ConnectWise. see HELP")
                exit(-13)
            else:  #If not a CSV file then ConnectWise will be configured
                # ConnectWise API Configuration
                self.connectwise_company_name = self.arg.connectwise_company_name
                self.connectwise_public_api_key = self.arg.public_api_key
                self.connectwise_private_api_key = self.arg.connectwise_private_api_key
                self.connectwise_api_site = self.arg.connectwise_api_site
                self.connectwise_all_companies_site = self.connectwise_api_site + '/company/contacts?pageSize=1000'
                self.connectwise_one_company_site = self.connectwise_api_site + '/company/contacts?conditions=company/' \
                                                                                'identifier like "{0}"& pageSize=1000'
        self.emails = []
        self.apihitcounter = 0
        self.session = Session()
        self.verify_cert = True  # change this to make requests without verifying
        
        # Dradis API Configuration
        self.dradis_api_token = self.arg.dradis_api_token
        self.dradis_project_id = self.arg.dradis_project_id
        self.dradis_url = self.arg.dradis_url
        self.dradis_issues_url = '{0}/pro/api/issues/'.format(self.dradis_url)  #https://dradis-pro.dev

    def run(self):
        self.emails = self.get_emails()
        if not isinstance(self.emails[0], dict):
            self.csv_hacked_emails_to_dradis(self.emails)
        else:
            self.connectwise_hacked_emails_to_dradis(self.emails)
        return 0

    def get_emails(self):
        if ".csv" in self.arg.CompanyID_or_CSVFilename:  #If CSV file
            contacts = []
            try:
                with open(self.arg.CompanyID_or_CSVFilename) as csvfile:  #Reading CSV file properly
                    mycsv = reader(csvfile, delimiter=',')
                    for row in mycsv:
                        for cell in row:
                            if "@" in cell:
                                print(cell)
                                contacts.append(cell)  #Storing CSV contents to list
            except Exception as e:
                print(e)
                exit(-1)
            return contacts
        elif self.arg.CompanyID_or_CSVFilename == 'all':  #If ConnectWise
            self.session.auth = (self.connectwise_company_name + '+{0}'.format(self.connectwise_public_api_key),  #Connecting to ConnectWise
                                 self.connectwise_private_api_key)
            contacts = self.session.get(self.connectwise_all_companies_site)  #Reading ConnectWise contacts for all companies
            if contacts.status_code != 200:
                print(self.arg.CompanyID_or_CSVFilename + ' - ' + contacts.text)
                exit(-1)
            self.session.auth = None
            return contacts.json()
        else:
            self.session.auth = (self.connectwise_company_name + '+{0}'.format(self.connectwise_public_api_key),
                                 self.connectwise_private_api_key)
            contacts = self.session.get(self.connectwise_one_company_site.format(self.arg.CompanyID_or_CSVFilename))  #Reading ConnectWise contacts for specified company
            if contacts.status_code != 200:
                print(self.arg.CompanyID_or_CSVFilename + ' - ' + contacts.text)
                exit(-1)
            self.session.auth = None
            return contacts.json()

    def csv_hacked_emails_to_dradis(self, emails):  #Sending compromised emails from CSV file to Dradis
        seen = set()
        uniqueEmails = []
        for email in emails:  #Creating a separate list of unique emails to remove duplicates
            if email.lower() not in seen:
                uniqueEmails.append(email.lower())
                seen.add(email.lower())
        for email in uniqueEmails:
            if self.apihitcounter == 100:
                    print("The hacked-emails API limit is 100. The script will now exit.")
                    exit(-1)
            hacked_email = self.session.get("https://hacked-emails.com/api?q={0}".format(email))  #Sending emails to website to check if compromised
            self.apihitcounter += 1
            if hacked_email.status_code != 200:
                print(email + hacked_email.text)
                continue
            elif hacked_email.json()['status'] == "notfound":
                print(email + ' has no entries in hacked-emails.com')
                continue
            else:
                self.session.headers.update({'Authorization': 'Token token="{0}"'.format(self.dradis_api_token)})
                self.session.headers.update({'Dradis-Project-Id': self.dradis_project_id})
                self.session.headers.update({'Content-type': 'application/json'})
                _data = ""
                for d in hacked_email.json()['data']:
                    _data += (
                    str(d['title']) + ' -- Date_Leaked: ' + str(d['date_leaked']) + ' -- Source_Network: ' + str(  #Storing results from hacked-emails.com
                        d['source_network']) + '\r\n')
                data = {'issue': {
                        'text': '#[Title]#\r\n' + email + ' - hacked-emails.com\r\n\r\n#[Results]#\r\n' + str(
                            hacked_email.json()['results']) + "\r\n\r\n" + _data + "\r\n\r\n"}}
                dradis = self.session.post(self.dradis_issues_url, data=dumps(data), verify=self.verify_cert)
                if dradis.status_code == 201:
                    print(email + ' was imported into Dradis')
                else:
                    print(email + ' was not imported into Dradis: ' + dradis.text)
                self.session.headers.clear()
        print("Completed.")

    def connectwise_hacked_emails_to_dradis(self, emails):  #Sending compromised emails from ConnectWise contacts to Dradis
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
                hacked_email = self.session.get("https://hacked-emails.com/api?q={0}".format(email))  #Sending emails to website to check if compromised
                self.apihitcounter += 1
                if hacked_email.status_code != 200:
                    print(email + hacked_email.text)
                    continue
                elif hacked_email.json()['status'] == "notfound":
                    print(email + ' has no entries in hacked-emails.com')
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
                    dradis = self.session.post(self.dradis_issues_url, data=dumps(data), verify= self.verify_cert)
                    if dradis.status_code == 201:
                        print(email + ' was imported into Dradis')
                    else:
                        print(email + ' was not imported into Dradis: ' + dradis.text)
                    self.session.headers.clear()
            else:
                continue

    def parse_args(self):
        # parse the arguments
        parser = ArgumentParser(epilog='\tCSV Example: \r\npython ' + argv[0] + " CompanyID_or_CSVFilename " +
                                       "Dradis_URL Dradis_Project_ID Dradis_API_Token \r\nConnectWise Example: "
                                       "\r\npython "+ argv[0] + "-c GoVanguard -s https://connectwiseapisite.com -u "
                                                                "12123 -p 41424124", 
                                description="Check ConnectWise Company Contacts' or csv of emails in the "
                                            "hacked-emails API and export the results to Dradis as issues")
        parser._optionals.title = "OPTIONS"
        parser.add_argument('-c', dest='connectwise_company_name', help="Your Company Name is ConnectWIse", required=False)
        parser.add_argument('-s', dest='connectwise_api_site', help="Your ConnectWise API site", required=False)
        parser.add_argument('-u', dest='connectwise_public_api_key',help="ConnectWise Public API Key", required=False)
        parser.add_argument('-p', dest='connectwise_private_api_key', help="ConnectWise Private API Key", required=False)

        parser.add_argument('CompanyID_or_CSVFilename', help="ConnectWise Company ID or CSV of emails")
        parser.add_argument('dradis_url', help="Dradis URL")
        parser.add_argument('dradis_project_id', help="Dradis Project ID")
        parser.add_argument('dradis_api_token', help="Dradis API Token")
        return parser.parse_args()

if __name__ == "__main__":
    a = HackedEmailstoDradis()
    a.run()