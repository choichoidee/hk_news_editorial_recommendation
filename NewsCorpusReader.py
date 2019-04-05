import os
import re
import pandas as pd
from itertools import chain

class NewsCorpusReader:

    def __init__(self, path='tokenized_stoprm/', newssource='all', doccat='all', contentcat='all', daterange='all'):
        self.newssource = newssource
        self.filedir = path
        self.doccat = doccat
        self.contentcat = contentcat
        self.daterange = daterange
        self.files = []
        self.filedict = {}


    def get_files(self):

        if self.newssource == 'all':
            newssource = os.listdir(self.filedir)
        else:
            newssource = self.newssource
        # Get News sources
        for source in newssource:
            if source == '.DS_Store':
                continue
            filepath = f"{self.filedir}{source}/"
            self.filedict[source] = os.listdir(filepath)

        if self.doccat == 'all':
            doccat = r'\w+'
        else:
            doccat = r'('+"|".join(self.doccat)+')'

        if self.contentcat == 'all':
            contentcat = r'\w+'
        else:
            contentcat = r'('+"|".join(self.contentcat)+')'

        if self.daterange == 'all':
            daterange = r'\w+'
#         else:
#             self.daterange = r'('+"|".join(self.daterange)+')'

        # Define search criteria
        CATPATTERN = re.compile(doccat+'_'+contentcat+'_'+daterange+'_'+'\w*\d+')

        # Get files
        for source in newssource:
            if source == '.DS_Store':
                continue
            for file in self.filedict[source]:
                if CATPATTERN.findall(file):
                    self.files.append(self.filedir+source+'/'+file)

        print(f"{len(self.files)} Files Loaded.")

    def yieldnews(self, by_line=False, skip_topic=False):
        for file in self.files:
            with open(file, 'r') as f:
                lines = f.readlines()
                if skip_topic == True:
                    lines = lines[1:]
                data = [line.strip(' \n').split(" ") for line in lines]
                if by_line == False:
                    data = list(chain(*data))
            yield data

    def get_df(self):
        df = pd.DataFrame({'filename': self.files})
        df['NewsID'] = [f"{idx:>08d}" for idx in df.index]
        timeinfo = df['filename'].str.extract('_(\d{8})_(\d{4})')
        df['Time'] = pd.to_datetime(timeinfo[0]+timeinfo[1])
        df['DocType'] = df['filename'].str.extract('(\w+)_(\w+)_\d{8}')[0]
        df['ContentType'] = df['filename'].str.extract('(\w+)_(\w+)_\d{8}')[1]
        df['Source'] = df['filename'].str.extract('tokenized_stoprm/(\w+)/')
        return df

    def refine_criteria(self, ewssource='all', doccat='all', contentcat='all', timebefore=None, timeafter=None):
        # search df and return user-specified filelist
        pass

    def show_article(articleid='random', original=True, stopword_removed=False):
        # if original = false, show tokenized fileself.
        pass
