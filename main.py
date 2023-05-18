import argparse

from analyze_svc import AnalyzeService
from download_svc import DownloadService

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--FromDate", help = "From date (YYYY-MM-dd), previous date of ToDate if missing")
    parser.add_argument("-t", "--ToDate", help = "To date (YYYY-MM-dd), Today if missing")
    args = parser.parse_args()
    fromDate = None
    toDate = None
    if args.ToDate:
        toDate = args.ToDate
        print("To date: %s" % toDate)
    if args.FromDate:
        fromDate = args.FromDate
        print("from date: %s" % fromDate)

    downloaded = None
    downloadSvc = DownloadService(fromDate, toDate)
    if downloadSvc.needDownload():
        downloaded = downloadSvc.startDownload()
    if downloadSvc.validSource(downloaded) == False:
        print("inValid")
        exit
    analyzeSvc = AnalyzeService(downloadSvc.fromDate, downloadSvc.toDate)
    analyzeSvc.compareData()