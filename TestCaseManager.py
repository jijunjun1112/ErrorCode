class TestCaseManager:
    def __init__(self,case_ErrorCount, case_TotalCount, case_html_text):
        self.mPrintBody = case_html_text
        self.mPrintBody += "<table>"
        self.mPrintBody += "<tr>"
        self.mPrintBody += "<th>Author</th>"
        self.mPrintBody += "<th>ModuleID</th>"
        self.mPrintBody += "<th>CaseID</th>"
        self.mPrintBody += "<th>TestResult</th>"
        self.mPrintBody += "<th>Log</th>"
        self.mPrintBody += "</tr>"
        self.mErrorCount = case_ErrorCount
        self.mTotalCount = case_TotalCount
        pass
 
    def reportCaseResult(self,author,moduleID,caseID,caseResult,caseLog):
        self.mPrintBody += "<tr>"
        self.mPrintBody += "<td> %s </td>" %(author)
        self.mPrintBody += "<td> %s </td>" %(moduleID)
        self.mPrintBody += "<td> %s </td>" %(caseID)
 
#         if caseResult == 1:
        if str(caseResult).lower() == "pass":
            self.mPrintBody += "<td> Pass </td>"
        else:
            self.mPrintBody += "<td> <font color=red>Failed</font></td>"
            self.mErrorCount += 1
        self.mPrintBody += "<td> %s </td>" %(caseLog)
        self.mPrintBody += "</tr>"
        self.mTotalCount += 1
        pass
 
    def printHtml(self):
        self.mPrintBody += "</table>"
        self.mPrintBody = "<h2> Total test case: %d , failed case: %d, pass %f</h2>" %(self.mTotalCount, self.mErrorCount, self.mErrorCount * 1.0/self.mTotalCount) + self.mPrintBody
        print self.mPrintBody
        pass