import feedparser
import csv
import getopt
import sys
from _sqlite3 import Row
from datetime import date
from datetime import datetime

from fileinput import filename
from html_parser import Html_Parser
import pickle
import logging
import os.path
import re



from time import mktime


class Crawler:

    header=None
        
    def __init__(self,header):
        self.header = header

        crawler_start_time = datetime.now()
        logging.info( str(crawler_start_time) + ":- Starting Crawler---------")
        self.numOfMsgCrawled = 0

        path=os.path.join(header.output_dir,
                          header.crawler_output)
        csv_file=open(path, 'wb')
        self.output_writer = csv.writer(csv_file,
                            delimiter=",",
                            quotechar='"',
                            quoting=csv.QUOTE_ALL)

        self.output_writer.writerow(["ArticleTitle", "Summary", "Link",
                         "Timestamp", "Category", "Keyword",
                         "ArticleStory"])
            
        self.keywordList = self.populateKeywordList()
        self.sites = self.populateSiteInformation()
        self.siteLastCrawled = self.populateSiteLastCrawled()
        self.processSites()

        crawler_end_time = datetime.now()
        

        total_crawl_time = (crawler_end_time - crawler_start_time )\
                            .total_seconds()
        crawlerSpeed = self.numOfMsgCrawled /total_crawl_time
            
        logging.info(str(datetime.now())
                        + ":- CRAWLER SPEED :: "
                        + str(crawlerSpeed)
                        + " articles/sec" )

        logging.info(str(datetime.now()) + ":- Closing Crawler---------")
        
    
    def __del__(self):
        with open(self.header.site_timestamp_pickle_file, "wb") as fp:
            pickle.dump(self.siteLastCrawled, fp)
   
    def populateSiteLastCrawled(self):
        """
        For every site, returns the time when it was last crawled
        """
        path=os.path.join(self.header.resource_dir,
                     self.header.site_timestamp_pickle_file)
        try:
            with open(path) as fp:
                site_timestamp_info =  pickle.load(fp)
                return site_timestamp_info

        except Exception as e:
            # Create empty dictionary in case pickle file is not found.
            return dict()
        
          
    def populateKeywordList(self):
        keyword_list = []

        path=os.path.join(self.header.resource_dir,
                     self.header.keyword_file)


        with open(path, 'rt') as csvFile:
            try:
                reader = csv.reader(csvFile)
                for row in reader:
                    keyword_list.append(row[0].lower())
                                                                                                  
            finally:
                csvFile.close()
            
        return keyword_list
    
    # Parse Site Information file for which data is to be crawled.
    def populateSiteInformation(self):
        sites = []
        path = os.path.join(
                    self.header.resource_dir,
                    self.header.site_info_file)

        with open(path, 'rt') as csvFile:
            try:
                reader = csv.reader(csvFile)
                for row in reader:
                    isActive = bool(row[1])
                    if (isActive):
                        sites.append(row[0])
                                                                                                  
            finally:
                csvFile.close()
        return sites
         
    
    def processSites(self):

        logging.info(str(datetime.now()) + ":- Start crawling sites ")

        for site in self.sites:
            logging.info(str(datetime.now()) + ":- Processing site : " + site)

            if site in self.siteLastCrawled:
                lastCrawledTimeStamp = self.siteLastCrawled[site]
            else:
                lastCrawledTimeStamp = datetime.strptime('Jun 1 2005  1:33PM',
                                                         '%b %d %Y %I:%M%p')
            
            try:
                parser_output = feedparser.parse(site)
            except Exception as e:
                print "Feed parser could not parse " + site
                continue
                
            entries = parser_output.entries
            
            # This will update the latest time stamp crawled, and insert
            # the entry if no information was available for this site.
            self.siteLastCrawled[site] = datetime.now()
           
            self.processEntries(entries, lastCrawledTimeStamp )

        return None

    def processEntries(self , entries , timestamp):
        """
        For every RSS item, goes to the article page. Extarcts the HTML
         and saves it
        """

        # Remove all HTML tags from the text
        pattern = re.compile(u'<\/?\w+\s*[^>]*?\/?>',
                             re.DOTALL | re.MULTILINE |
                             re.IGNORECASE | re.UNICODE)

        for entry in entries:

            title = "NA"
            description = "NA"
            link = "NA"
            published ="NA"
            article_content = "NA"
            category = "NA"
            
            
            if "published" in entry:
                published = self.removeNonAscii(entry['published'])
                published_parsed_struct = entry['published_parsed']
                
                # In certain instances, published_parsed date is not available,
                # entry is considered  valid
                if published_parsed_struct == None:
                    break
                
                published_parsed = datetime\
                                .fromtimestamp(mktime(published_parsed_struct))
                        
              
                # Time filter to prevent redundant data collection
                #hack: Disabing time check
                #if published_parsed < timestamp:
                #    return
            
            
            if "title" in entry:
                title = self.removeNonAscii(entry['title'])
            
                
        
            if "description" in entry:
                description = pattern.sub(u" ",
                                  self.removeNonAscii(entry['description']))

            if "category" in entry:
                category = self.removeNonAscii(entry['category'])
            
            if "link" in entry:
                link = self.removeNonAscii(entry['link'])
                html_parser = Html_Parser(link, 'article')
                article_content = self.removeNonAscii(html_parser.fetchText())
            

            if self.header.key_word_filering_switch==1:
                keyword_found = self.isContainsKeyword(title)
            else:
                keyword_found = "Not Applibale"

            self.dumpParsedResult( [title,
                                    description,
                                    link,
                                    published,
                                    category,
                                    keyword_found,
                                    article_content])

        return None

    def dumpParsedResult(self , entry_value_list):


        self.numOfMsgCrawled = self.numOfMsgCrawled + 1
        logging.debug(" Message : " + ', '.join(entry_value_list))
        self.output_writer.writerow(entry_value_list)
        self.print_summary(entry_value_list)




    def removeNonAscii(self , text):

        return ''.join([i if ord(i) < 128 else ' ' for i in text])       

            
    def isContainsKeyword(self , text):
        """
        Searches for the keyword in the part of the article that has been
        specified in the confog file
        """
        for keyword in self.keywordList:
            if(keyword in text.lower()):
                return keyword
    
        return ""          


    def print_summary(self,entry_value_list):
        print "No. of artciles crawled %s. Latest link -> %s" %(
            self.numOfMsgCrawled, entry_value_list[2])
        return None










