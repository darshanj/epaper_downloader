from bs4 import BeautifulSoup
import requests
import re
import lxml
import datetime
import os
import glob
import contextlib

from PyPDF2 import PdfFileMerger

now = datetime.datetime.now()
date=now.strftime("%Y%m%d")

def download_file(url):
    path = url.split('/')[-1].split('?')[0]
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    return path

def edition_pdf_name(edition):
    return "{0}.pdf".format(edition)

def remove_edition(edition):
    with contextlib.suppress(FileNotFoundError):
        os.remove(edition_pdf_name(edition))

def download_edition(edition):
    edition_date = "{0}_{1}".format(edition,date)
    u = "http://gujaratsamacharepaper.com/nd/gujaratsamachar.php?isid={0}".format(edition_date)
    req = requests.get(u)
    soup = BeautifulSoup(req.text, "lxml")
    pages = soup.findAll('a', href=re.compile(".*{0}.*".format(edition_date)))
    pdfs = list()

    if len(pages) == 0:
        print("No pages found for edition: {0}. URL: {1}".format(edition,u))
        return

    for page in pages:
        page_name=page['href'].split('=')[1].lstrip("{0}_".format(edition))
        file_url="http://enewspapr.com/News/{0}/{1}/{2}.PDF".format(edition.replace("_","/"),now.strftime("%Y/%m/%d"),page_name)
        print("Downloading : {0}".format(file_url))
        pdfs.append(download_file(file_url))

    print("Merging all PDFs for {0} ...".format(edition_date))

    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)

    edition_file_name = edition_pdf_name(edition)
    merger.write(edition_file_name)


    def clean_up(files):
        for f in files:
            print("Removing file : {0}".format(f))
            os.remove(f)

    clean_up(pdfs)
    print("Merged PDF {0} is ready".format(edition_file_name))


remove_edition("GUJARAT_RAJ")
download_edition("GUJARAT_RAJ")
remove_edition("GUJARAT_SAH")
download_edition("GUJARAT_SAH")
remove_edition("GUJARAT_SHA")
download_edition("GUJARAT_SHA")
remove_edition("GUJARAT_RAV")
download_edition("GUJARAT_RAV")