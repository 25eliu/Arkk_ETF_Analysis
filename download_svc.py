import csv
import re
from datetime import datetime, timedelta
from os import makedirs
from os.path import exists
from pathlib import Path

import requests

from ark_action import BaseService

hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

urlTable = [['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_AUTONOMOUS_TECH._&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv', 'ARKQ'],
       ['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv', 'ARKK'],
       ['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv', 'ARKF'],
       ['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv', 'ARKW'],
       ['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_GENOMIC_REVOLUTION_ETF_ARKG_HOLDINGS.csv', 'ARKG'],
       ['https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_SPACE_EXPLORATION_&_INNOVATION_ETF_ARKX_HOLDINGS.csv', 'ARKX']]

class DownloadService(BaseService):
    def startDownload(self):
        with requests.Session() as s:
            for url in urlTable:
                fundnm = url[1]
                download = s.get(url[0], headers=hdr) #, verify = "/Users/hliu/Documents/CloudflareIncECCCA-3.crt")
                content = download.content.decode('utf-8')
                print(content)

                rows = content.split('\n')
                print(len(rows))

                if len(rows) > 1:
                    currdate = rows[1].split(',')[0]
                    dt = datetime.strptime(currdate, '%m/%d/%Y')
                    dateStr = dt.strftime('%Y-%m-%d')
                    today = datetime.today()
                    folderpath = '{0}/{1}'.format(self.srcHomePath, dateStr)
                    filepath = '{0}/{1}.csv'.format(folderpath, fundnm)
                    # today.strftime('%Y-%m-%d') != dateStr):
                    if today >= dt + timedelta(days=1) and exists(folderpath) and exists(filepath):
                        print("no download since date mismatch!")
                        return False
                else:
                    continue
                print(dateStr)

                data = []
                for i in range(len(rows) - 2):
                    if i == 0:
                        tmpheader = rows[0].split(',')
                        header = [s.strip('"') for s in tmpheader]
                    else:
                        tmprow = re.split(r',(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)', rows[i])
                        row = [s.strip('"') for s in tmprow]
                        data.append(row)

                folderpath = '{0}/{1}'.format(self.srcHomePath, dateStr)
                if not exists(folderpath):
                    makedirs(folderpath)
                filepath = '{0}/{1}.csv'.format(folderpath, fundnm)
                with open(filepath, 'w', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(data)
            return True
