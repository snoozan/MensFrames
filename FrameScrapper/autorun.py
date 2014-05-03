import subprocess
import sys
import os
import json

class AutoRunURLs():

    def deletejson():
        bashCommand = "rm items.json"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]


    def bashspider(spider):
        bashCommand = "scrapy crawl " + spider + " -o items.json -t json"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]

    def jsonsplitter(url):
        temp = url.split('url":')
        temp =(temp[1].split('\''))
        temp =(temp[0].split('}'))
        return temp[0]


    if __name__ == "__main__":
        deletejson()

        spiders = ['eyefly', 'coastal', 'mezzmer', 'glasses', 'thirtynine', 'warbyparker']
        for spider in spiders:
            bashspider(spider)

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0])))

        urls = []
        with open(os.path.join(__location__, 'items.json')) as json_items:
            lines = json_items.readlines()
            for line in lines:
                urls.append(line)

        newurls = []
        for url in urls:
            newurls.append(jsonsplitter(url))

        deletejson()

        for url in newurls:
            if "http://www.coastal.com" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashspider("coastalinfo -a url=%s" % urlstripped)


            elif "eyefly" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashspider("eyeflyinfo -a url=%s" % urlstripped)

            elif "mezzmer" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashspider("mezzmerinfo -a url=%s" % urlstripped)
                print("mezzmer")

            elif "39dollarglasses" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashspider("thirtynineinfo -a url=%s" % urlstripped)
                print("thirtynine")

            elif "warbyparker" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashspider("warbyparkerinfo -a url=%s" % urlstripped)
                print("warbyparker")

            """
            elif "glasses" in url:
                urlstripped = url.split("http://")
                urlstripped = urlstripped[1].strip('\"')

                bashspider("glassesinfo -a url=%s" % urlstripped)
                print("glasses")
            """


