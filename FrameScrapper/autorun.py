import subprocess
import sys
import os
import json

class AutoRunURLs():

    """
    subprocess.call("/bashscripts/.refreshjson", shell=True)
    print("deleted items.json")

    subprocess.call("/bashscripts/.coastal.sh", shell=True)
    print("coastal run")
    subprocess.call("/bashscripts/.eyefly.sh", shell=True)
    print("eyefly run")
    subprocess.call("/bashscripts/.memmzer.sh", shell=True)
    print("memmzer run")
    subprocess.call("/bashscripts/.glasses.sh", shell=True)
    print("glasses run")
    subprocess.call("/bashscripts/.thirtynine.sh", shell=True)
    print("thirtynine run")
    subprocess.call("/bashscripts/.warbyparker.sh", shell=True)
    print("warbyparker run")
    spiders = ["coastal", "eyefly", "mezzmer", "glasses", "thirtynine", "warbyparker"]

    for spider in spiders:
        bashspider(spider)

    """
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0])))

    urls = []
    with open(os.path.join(__location__, 'items.json')) as json_items:
        lines = json_items.readlines()
        for line in lines:
            urls.append(line)

    def bashspider(spider):
        bashCommand = "scrapy crawl " + spider + " -o items.json -t json"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]

    def jsonsplitter(url):
        temp = url.split('url":')
        temp =(temp[1].split('\''))
        temp =(temp[0].split('}'))
        return temp[0]


    subprocess.call("./.refreshjson", shell=True)

    for url in urls:
        if "http://www.coastal.com" in url:
            bashspider("coastalinfo -a " + jsonsplitter(url))

        if "http://eyefly.com" in url:
            bashspider("eyeflyinfo -a " + jsonsplitter(url))

        if "http://mezzmer.com" in url:
            bashspider("mezzmerinfo -a " + jsonsplitter(url))

        if "http://glasses.com" in url:
            bashspider("glassesinfo -a " + jsonsplitter(url))

        if "http://39dollarglasses.com" in url:
            bashspider("thirtynineinfo -a" + jsonsplitter(url))

        if "http://warbyparker.com" in url:
            bashspider("warbyparkerinfo -a" + jsonsplitter(url))

