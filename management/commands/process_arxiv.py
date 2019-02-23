from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from urllib.request import urlopen
from xml.dom import minidom
from os import path, makedirs
from io import BytesIO
from pdf2image import convert_from_bytes
from PIL import Image

import glob
import re
import tarfile
import shutil

class Command(BaseCommand):
    """ Search the 'new' articles on arXiv each day, record those that mention Illustris in the abstract."""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        searchStrs = ['simulation','simulate','computation','numerical']
        validExts = ['jpg','png','pdf'] # eps, ps
        baseDir = "/var/www/html/static/ac/arxiv/"
        maxImagePx = 800

        # cleanup folders older than a week or two
        cur_dirs = sorted(glob.glob(baseDir + "*"))[::-1]

        for dir in cur_dirs[3:]:
            print('Cleanup: [%s]' % dir)
            shutil.rmtree(dir)

        # no need to run when there aren't new arxiv postings
        if timezone.now().strftime("%a") in ['Sat','Sun']:
            return
        
        # get today's arxiv postings
        pubs = []

        arxivUrl = 'http://export.arxiv.org/rss/astro-ph/new?version=2.0'
        
        # get page and parse XML
        arxiv = minidom.parse(urlopen(arxivUrl))
        items = arxiv.getElementsByTagName('item')

        for item in items:
            title = item.getElementsByTagName('title')[0].childNodes[0].data
            title = title[:title.rfind(' (arXiv')]

            link  = item.getElementsByTagName('link')[0].childNodes[0].data
            id    = link[link.rfind('/')+1:]

            desc      = item.getElementsByTagName('description')[0].childNodes[0].data
            authStart = desc.find('Authors:')
            authEnd   = desc.find('</div>',authStart)
            abstract  = desc[authEnd+1:]
            abstract  = re.sub('<[^<]+?>', '', abstract).strip() # strip all html tags

            # keep if abstract contains one of our search string(s)
            for searchStr in searchStrs:
                if searchStr.lower() in abstract.lower():
                    pubs.append({'title':title,'link':link,'id':id})
                    break

        self.stdout.write('daily_arxiv_scrape: found matching [%d of %d] (%s)' % 
                          (len(pubs),len(items),timezone.now()))

        # make a directory for this day
        saveDir = baseDir + timezone.now().strftime("%Y-%U-%a") + "/"

        if not path.exists(saveDir):
            makedirs(saveDir)

        # loop over and save any new publications
        for pub in pubs:
            # grab the paper source
            source_url = "https://arxiv.org/e-print/" + pub['id']
            print(source_url)

            targz = urlopen(source_url)
            buf = BytesIO()
            buf.write(targz.read())
            buf.seek(0) # convert the string into a memory buffer allowing random seeking

            # inspect .tar.gz file
            archive = tarfile.open(mode="r:gz", fileobj=buf)

            # extract images into the paper directory
            for i, file in enumerate(archive.getnames()):
                # only proceed for valid extensions
                ext = file.rsplit('.')[-1].lower()
                if ext not in validExts:
                    continue

                out_filename = '%s_%d.%s' % (pub['id'],i,ext)

                im = archive.extractfile(file)

                if ext == 'pdf':
                    # rasterize and save
                    out_filename = out_filename.replace('.pdf','.jpg')
                    im_raster = convert_from_bytes(im.read(), dpi=75)
                    if len(im_raster):
                        im_raster[0].save(saveDir + out_filename, 'JPEG')
                else:
                    # save directly
                    with open(saveDir + out_filename,'wb') as f:
                        f.write(im.read())

                #print(' '+file, out_filename)

        # resize any excessively large images
        images = glob.glob(saveDir + "*")

        for filename in images:
            try:
                im = Image.open(filename)

                if im.size[0] <= maxImagePx and im.size[1] <= maxImagePx:
                    continue

                im.thumbnail((maxImagePx,maxImagePx), Image.ANTIALIAS)
                im.save(filename)
            except:
                pass

        # todo: filter function/algorithm (pre-trained network?), keep only vis-like (not plot-like) images
