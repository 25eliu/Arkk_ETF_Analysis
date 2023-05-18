from datetime import datetime
from os import listdir
from os.path import exists, isdir, isfile, join
from pathlib import Path

class BaseService:
    srcHomePath = '{0}/stock/ark'.format(Path.home())
    def __init__(self, fromDate = None, toDate = None):
        todayStr = datetime.today().strftime('%Y-%m-%d')
        self.fromDate = fromDate
        self.toDate = toDate
        if self.toDate is None:
            self.toDate = todayStr

    def needDownload(self):
        today = datetime.today().strftime('%Y-%m-%d')
        # if today != self.toDate:
        #     return False

        toPath = '{0}/{1}'.format(self.srcHomePath, self.toDate)
        isExist = exists(toPath)
        if not isExist:
            return True

        csvfiles = [f for f in listdir(toPath) if f.endswith('.csv') and isfile(join(toPath, f))]
        #csvfiles = filter(lambda f: f.endswith('.csv'), allfiles)
        if len(list(csvfiles)) == 6:
            return False

        return True

    def validSource(self, downloaded):
        allfolders = [d for d in listdir(self.srcHomePath) if isdir(join(self.srcHomePath, d))]
        allfolders.sort()
        print(allfolders)
        if downloaded == False:
            self.toDate = allfolders[len(allfolders) - 1]
        #allfolders.sort(reverse = True)
        #print(allfolders)
        tDate = datetime.strptime(self.toDate, '%Y-%m-%d')
        if self.fromDate is not None:
            fDate = datetime.strptime(self.fromDate, '%Y-%m-%d')
            if fDate >= tDate:
                print("fromDate %s should be earlier than toDate %s" % (self.fromDate, self.toDate))
                return False
            else:
                fromPath = '{0}/{1}'.format(self.srcHomePath, self.fromDate)
                if exists(fromPath) == False:
                    print("No data existed in fromPath %s " % fromPath)
                    return False
        #res = next(x for x, val in enumerate(allfolders) if val > 0.6)
        else:
            tmplist = list(filter(lambda i: i < self.toDate, allfolders))
            if len(tmplist) < 1:
                return False
            self.fromDate = tmplist[len(tmplist)- 1]
            if self.fromDate == self.toDate and len(tmplist) >= 2:
                self.fromDate = tmplist[len(tmplist) - 2]

        return True
