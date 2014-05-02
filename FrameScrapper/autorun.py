import subprocess

class AutoRunURLs():

    subprocess.call("/bashscripts/.refreshjson", shell=True)
    print("deleted items.json")
    """
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
    """
    spiders = ["coastal", "eyefly", "mezzmer", "glasses", "thirtynine", "warbyparker"]

    for spider in spiders:

        bashCommand = "scrapy crawl " + spider + " -o items.json -t json"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
