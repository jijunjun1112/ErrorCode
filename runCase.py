import re,os,sys,time,subprocess

class runCase():
    def __init__(self,pythonExeDir):
        if pythonExeDir != 'python':
            if not os.path.exists(pythonExeDir):
                sys.exit(1)
        self.runEXE = pythonExeDir
        self.path = os.path.abspath(os.curdir)
#         self.path = os.path.abspath(currentPath + '..\..\..\..\TestCases\projectX')

    def cycleRun(self):
        r=re.compile("M\d{2,}") #match the path
        pathlist=[]
        for temp in os.listdir(self.path):
            if r.search(temp) is not None:
                tpath=os.path.join(self.path,temp)
                if os.path.exists(tpath):
                    pathlist.append(tpath)
#                 sys.exit(1)
        if len(pathlist) <= 0:
            print ("no test cases need run, please check the filename,should be :MXX")
            sys.exit(1)
        print "Script will run these cases:\n%s "%(pathlist)
        print "please chooise if or not to run them[y/n]:"
        ok=raw_input()
        if ok in ('y','ye','yes'): 
            print "start to tun"
        elif ok in ('n','no','nop','nope'): sys.exit(1)
        else: raise IOError,'bad input! exit' 
        for case in pathlist:
            print case
            timetmpstart = time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime( time.time()-5 )) 
            print "the case %s start time is %s" % (case,timetmpstart)
            cmd = "%s %s" % (self.runEXE,case)
            print cmd
            p = subprocess.Popen(cmd,shell=False)
            p.wait()
            if p.returncode != 0:
                print "Error."
                return -1  
            log = p.communicate()
            print log