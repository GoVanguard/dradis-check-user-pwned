from pydradis3 import Pydradis3
import pypwned
from json import dumps
import csv
from sys import argv, exit, version
from argparse import ArgumentParser

class HaveIBeenPwndDradis(object):
    def __init__(self):
        self.arg = self.processArguments()
        if len(argv) != 5:
            print("Possibly missing arguments. Try HELP")
            exit(-6)
        # Dradis API Configuration
        self.verifyCert = True    # change this to make requests without verifying
        self.dradisApiToken = self.arg.dradisApiToken
        self.dradisProjectId = self.arg.dradisProjectId
        self.dradisUrl = self.arg.dradisUrl
        self.dradisDebug = False
        self.dradisSession = Pydradis3(self.dradisApiToken, self.dradisUrl, self.dradisDebug, self.verifyCert)

    def run(self):
        try:
            with open(self.arg.csvFileName)as csvfile:
                csvObj = csv.reader(csvfile, delimiter=',')
                #self.createIssues(csvObj)
                for csvRow in csvObj:
                    userEmail = csvRow[0]
                    self.performQuery(userEmail, self.dradisProjectId)
                    #print(csvRow[0]) 
        except Exception as e:
            print(e)
            exit(-1)
        self.dradisSession = None
        print("Finished.")
        return

    def searchApi(self, user: str):
        searchResults = pypwned.getAllBreachesForAccount(email=user)
        if str(searchResults) == "A server error occurred on haveibeenpwned.com. Please try again later.":
            searchResults = []
        return searchResults

    def performQuery(self, userEmail: str, projectId: str):
        pwndResults = self.searchApi(userEmail)
        if pwndResults:
            nodeId = self.createNode(userEmail, projectId)
            if nodeId:
                print("Node {0} for {1} found on projectId {2}".format(nodeId, userEmail, projectId))
                issueId = self.createIssue(userEmail, projectId, nodeId)
                if issueId:
                    print("Issue {0} for {1} created on projectId {2}".format(issueId, nodeId, projectId))
                    print(pwndResults)
                    for pwndResult in pwndResults:
                        text = '#[Title]#\r\n' + userEmail + '_breach\r\n\r\n'
                        text += '#[{0}]#\r\n'.format(pwndResult) + '{0}\r\n'.format(pwndResults[pwndResult]) + '\r\n\r\n'
                        evidenceId = self.createEvidence(nodeId, projectId, issueId, text)
                        if evidenceId:
                            print("Evidence {0} for {1} created on projectId {2}".format(evidenceId, issueId, projectId))
                        else:
                            print("Evidence creation for {0} failed on projectId {1}".format(issueId, projectId))
                else:
                    print("Issue creation for {0} failed on projectId {1}".format(nodeId, projectId))
            else:
                print("Node creation for {0} failed on projectId {1}".format(userEmail, projectId))
        else:
            print("No breach results for {0}".format(userEmail))
        
        return

    def createIssue(self, userEmail, projectId, nodeId):
        # Call create_issue_raw from pydradis3 which accepts a manually constructed payload as data
        issueTitle = "Email address {0} (node id {1}) found in one or more breaches, databases or pastebins".format(userEmail, nodeId)
        issueText = issueTitle + "\n Please review evidence for information on each instance."
        issueTags = ["##{0}##".format(nodeId), "##{0}##".format(userEmail)]
        createIssue = self.dradisSession.create_issue(projectId, issueTitle, issueText, issueTags)
        return createIssue

    def createNode(self, nodeName: str, projectId: int):
        nodeList = self.dradisSession.get_nodelist(projectId)
        for nodeEntry in nodeList:
            if str(nodeName).lower() == str(nodeEntry[0]).lower():
                print("Found node match: {0}, id {1}".format(nodeName, nodeEntry[1]))
                return nodeEntry[1]
        print("No node match for: {0}".format(nodeName))
        createNode = self.dradisSession.create_node(projectId, nodeName, 0, None, 1)
        print("Created node: {0}, id {1}".format(nodeName, createNode))
        return createNode

    def createEvidence(self, nodeId, projectId, issueId, evidenceData):
        createEvidence = self.dradisSession.create_evidence_raw(projectId, node_id=nodeId, issue_id=issueId, data=evidenceData)
        print(createEvidence)
        return createEvidence

    def processArguments(self):
        # parse the arguments
        parser = ArgumentParser(epilog='\tExample: \r\npython ' + argv[0] +
                                       " -i users.csv https://dradis-pro.dev 21 xa632ghas87d393287",
                                description="Open .CSV, check haveibeenpawned API for each email and "
                                            "post to Dradis\n\n")
        parser.add_argument('csvFileName', help=".csv filename")
        parser.add_argument('dradisUrl', help="Dradis URL")
        parser.add_argument('dradisProjectId', help="Dradis Project ID")
        parser.add_argument('dradisApiToken', help="Dradis API token")
        return parser.parse_args()

if __name__ == "__main__":
    scriptInstance = HaveIBeenPwndDradis()
    scriptInstance.run()
