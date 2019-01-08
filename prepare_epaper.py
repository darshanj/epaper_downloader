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
    req = requests.get("http://gujaratsamacharepaper.com/nd/gujaratsamachar.php?isid={0}".format(edition_date))
    soup = BeautifulSoup(req.text, "lxml")
    pages = soup.findAll('a', href=re.compile(".*{0}.*".format(edition_date)))
    pdfs = list()

    for page in pages:
        page_name=page['href'].split('=')[1].lstrip("{0}_".format(edition))
        file_url="http://enewspapr.com/News/{0}/{1}/{2}.PDF".format(edition.replace("_","/"),now.strftime("%Y/%m/%d"),page_name)
        print(file_url)
        pdfs.append(download_file(file_url))


    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write(edition_pdf_name(edition))

    def clean_up(files):
        for f in files:
            os.remove(f)

    clean_up(pdfs)

remove_edition("GUJARAT_RAJ")
download_edition("GUJARAT_RAJ")
remove_edition("GUJARAT_SAH")
download_edition("GUJARAT_SAH")