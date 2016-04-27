import unittest,time

class projectx_base(unittest.TestCase):
    def __init__(self,AUTHOR = "chfshan",moduleID = "projectx",caseID = "0000001"):
        self.AUTHOR=AUTHOR
        self.startTime = time.strftime('%H%M%S')
        self.moduleID = moduleID
        self.caseID = caseID
    def OnSetUp(self):
        pass
    def OnTearDown(self):
        pass
    def OnError(self):
        pass
    def OnFail(self):
        pass
    def Run(self):
        self.OnSetUp()
        self.OnRun()
        self.OnTearDown()
    def OnRun(self):
        pass