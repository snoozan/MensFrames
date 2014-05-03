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

        for url in newurls:
            if "http://www.coastal.com" in url:

                bashCommand = "scrapy crawl coastalinfo -a url='http://www.coastal.com/r-hardy-9016-black?rsView=1&ga=M|F|Ki'"
                #-a url={0}".format(url.strip())

                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output = process.communicate()[0]
                process.wait()


            elif "http://eyefly.com" in url:
                #bashspider("eyeflyinfo -a url=" + jsonsplitter(url))
                print("eyefly")

            elif "http://mezzmer.com" in url:
                #bashspider("mezzmerinfo -a url=" + jsonsplitter(url))
                print("mezzmer")

            elif "http://glasses.com" in url:
                #bashspider("glassesinfo -a url=" + jsonsplitter(url))
                print("glasses")

            elif "http://39dollarglasses.com" in url:
                #bashspider("thirtynineinfo -a url=" + jsonsplitter(url))
                print("thirtynine")

            elif "http://warbyparker.com" in url:
                #bashspider("warbyparkerinfo -a url=" + jsonsplitter(url))
                print("warbyparker")

