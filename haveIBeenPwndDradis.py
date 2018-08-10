import pydradis3
import pypwned
from json import dumps
import csv
from sys import argv, exit, version
from argparse import ArgumentParser

class HaveIBeenPwndDradis(object):
    def __init__(self):
        self.arg = self.parseArgs()
        if len(argv) != 4:
            print("Possibly missing arguments. Try HELP")
            exit(-6)
        # Dradis API Configuration
        self.verify_cert = True    # change this to make requests without verifying
        self.dradis_api_token = self.arg.dradis_api_token
        self.dradis_project_id = self.arg.dradis_project_id
        self.dradis_url = self.arg.dradis_url
        self.dradis_debug = False
        self.dradis_session = Pydradis3(self.dradis_api_token, self.dradis_url, self.dradis_debug, self.verify_cert)

    def run(self):
        try:
            with open(self.arg.csvFileName)as csvfile:
                csvObj = csv.reader(csvfile, delimiter=',')
                self.createIssues(csvObj)
        except Exception as e:
            print(e)
            exit(-1)
        self.dradis_session = None
        print("Finished.")
        return

    def searchApi(self, user: str):
        pypwned.getAllBreachesForAccount(email=user)
        return pypwned

    def createIssues(self, csv: object):
        counter = 0
        for row in csv:
            counter = counter + 1
            userEmail = row[0]
            text = '#[Title]#\r\n' + userEmail + '\r\n\r\n'
            # Get API results
            pwndResults = self.searchApi(userEmail)
            # Process each result into payload
            for pwndResult in pwndResults:
                text += '#[{0}]#\r\n'.format(pwndResult) + '{0}\r\n'.format(pwndResults[pwndResult]) + '\r\n\r\n'
            data = {'issue': {'text': text}}
            # Call create_issue_raw from pydradis3 which accepts a manually constructed payload as data
            createIssue = self.dradis_session.create_issue_raw(self.dradis_project_id, data=data)
            if createIssue:
                print("Row {0} Issue was exported into Dradis".format(counter))
            else:
                print("Row {0} Issue was not exported into Dradis".format(counter))
        return

    @staticmethod
    def parseArgs():
        # parse the arguments
        parser = ArgumentParser(epilog='\tExample: \r\npython ' + argv[0] +
                                       " -i users.csv https://dradis-pro.dev 21 xa632ghas87d393287",
                                description="Open .CSV, check haveibeenpawned API for each email and "
                                            "post to Dradis\n\n")
        parser.add_argument('csvFileName', help=".csv filename")
        parser.add_argument('dradis_url', help="Dradis URL")
        parser.add_argument('dradis_project_id', help="Dradis Project ID")
        parser.add_argument('dradis_api_token', help="Dradis API token")
        return parser.parse_args()

if __name__ == "__main__":
    scriptInstance = HaveIBeenPwndDradis()
    scriptInstance.run()
