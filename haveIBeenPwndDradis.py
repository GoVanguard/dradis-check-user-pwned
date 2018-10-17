from pydradis3 import Pydradis3
from pyHaveIBeenPwned import pyHaveIBeenPwned
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
        self.querySession = pyHaveIBeenPwned()

    def run(self):
        try:
            with open(self.arg.csvFileName)as csvfile:
                csvObj = csv.reader(csvfile, delimiter=',')
                #self.createIssues(csvObj)
                for csvRow in csvObj:
                    userEmailOrDomain = csvRow[0]
                    self.performQuery(userEmailOrDomain, self.dradisProjectId)
                    #print(csvRow[0]) 
        except Exception as e:
            print(e)
            exit(-1)
        self.dradisSession = None
        print("Finished.")
        return

    def searchApi(self, query: str):
        print("Performing breach query for {0}. Be patient, this can take 4 to 20 seconds.".format(query))
        if "@" in query:
            breachList = self.querySession.getAccountBreaches(query)
            print("Performing paste query for {0}. Be patient, this can take 4 to 20 seconds.".format(query))
            pasteList = self.querySession.getAccountPastes(query)
            if type(pasteList) == type(str()):
                print(pasteList)
                pasteList = []
        else:
            breachList = self.querySession.getDomainBreaches(query)
            pasteList = []
        if type(breachList) == type(str()):
            print(breachList)
            breachList = []
            pasteList = []
        searchResults = breachList + pasteList
        return searchResults

    def performQuery(self, userEmailOrDomain: str, projectId: str):
        pwndResults = self.searchApi(userEmailOrDomain)
        if pwndResults:
            nodeId = self.createNode(userEmailOrDomain, projectId)
            if nodeId:
                print("Node {0} for {1} found on projectId {2}".format(nodeId, userEmailOrDomain, projectId))
                issueId = self.createIssue(userEmailOrDomain, projectId, nodeId)
                if issueId:
                    print("Issue {0} for {1} created on projectId {2}".format(issueId, nodeId, projectId))
                    for pwndResult in pwndResults:
                        if pwndResult.get('Source'):
                            text = '#[Title]#\r\n' + userEmailOrDomain + '_paste\r\n\r\n'
                        else:
                            text = '#[Title]#\r\n' + userEmailOrDomain + '_breach\r\n\r\n'
                        for resultKey in pwndResult:
                            text += '#[{0}]#\r\n'.format(resultKey) + '{0}\r\n'.format(pwndResult[resultKey]) + '\r\n\r\n'
                        evidenceId = self.createEvidence(nodeId, projectId, issueId, text)
                        if evidenceId:
                            print("Evidence {0} for {1} created on projectId {2}".format(evidenceId, issueId, projectId))
                        else:
                            print("Evidence creation for {0} failed on projectId {1}".format(issueId, projectId))
                else:
                    print("Issue creation for {0} failed on projectId {1}".format(nodeId, projectId))
            else:
                print("Node creation for {0} failed on projectId {1}".format(userEmailOrDomain, projectId))
        else:
            print("No breach results for {0}".format(userEmailOrDomain))
        
        return

    def createIssue(self, userEmailOrDomain, projectId, nodeId):
        # Call create_issue_raw from pydradis3 which accepts a manually constructed payload as data
        issueTitle = "{0} (node id {1}) found in one or more breaches, databases or pastebins".format(userEmailOrDomain, nodeId)
        issueText = issueTitle + "\n Please review evidence for information on each instance."
        issueTags = ["##{0}##".format(nodeId), "##{0}##".format(userEmailOrDomain)]
        createIssue = self.dradisSession.create_issue(projectId, issueTitle, issueText)
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
