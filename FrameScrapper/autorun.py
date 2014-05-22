import subprocess
import sys
import os
import json
import xml
import fileinput

class AutoRunURLs():

    def deletejson(dump):
        bashCommand = "rm items.%s" % (dump)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]


    def bashspider(spider, dump):
        bashCommand = "scrapy crawl " + spider + " -o items.%s -t %s" % (dump, dump)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]

    def bashinfospider(spider):
        bashCommand = 'scrapy crawl ' + spider
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]

    def jsonsplitter(url):
        temp = url.split('url":')
        temp =(temp[1].split('\''))
        temp =(temp[0].split('}'))
        return temp[0]


    if __name__ == "__main__":


        deletejson("json")



        spiders = ['eyefly', 'coastal', 'mezzmer', 'glasses', 'thirtynine', 'warbyparker', 'lenscrafters', 'lookmatic']
        for spider in spiders:
            bashspider(spider, "json")


        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0])))

        urls = []
        with open(os.path.join(__location__, 'items.json')) as json_items:
            lines = json_items.readlines()
            for line in lines:
                urls.append(line)

        newurls = []
        for url in urls:
            newurls.append(jsonsplitter(url))


        file = open('items.xml', 'w+b')
        file.write('<?xml version="1.0" encoding="utf-8"?>')
        file.write('\n<root>\n')
        file.close()


        for url in newurls:

            if "http://www.coastal.com" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashinfospider('coastalinfo -a url=%s' % urlstripped)


            elif "mezzmer" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashinfospider("mezzmerinfo -a url=%s" % urlstripped)
                print("mezzmer")


            elif "warbyparker" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashinfospider("warbyparkerinfo -a url=%s" % urlstripped)
                print("warbyparker")

            elif "lenscrafters" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashinfospider("lenscraftersinfo -a url=%s" % urlstripped)
                print("lenscrafters")

            elif "39dollarglasses" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashinfospider("thirtynineinfo -a url=%s" % urlstripped)
                print("thirtynine")

            elif "eyefly" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashinfospider("eyeflyinfo -a url=%s" % urlstripped)

        file = open('items.xml', 'a')
        file.write('\n</root>\n')
        file.close()

        """

            elif "glasses" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashspider("glassesinfo -a url=%s" % urlstripped,"xml")
                print("glasses")

        """

