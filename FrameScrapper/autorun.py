import subprocess

class AutoRunURLs():

    """
    subprocess.call("/.refreshjson", shell=True)
    print("deleted items.json")
    subprocess.call("/.coastal.sh", shell=True)
    print("coastal run")
    subprocess.call("/.eyefly.sh", shell=True)
    print("eyefly run")
    subprocess.call("/.memmzer.sh", shell=True)
    print("memmzer run")
    subprocess.call("/.glasses.sh", shell=True)
    print("glasses run")
    subprocess.call("/.thirtynine.sh", shell=True)
    print("thirtynine run")
    subprocess.call("/.warbyparker.sh", shell=True)
    print("warbyparker run")
    """
    spiders = ["coastal", "eyefly", "mezzmer", "glasses", "thirtynine", "warbyparker"]

    for spider in spiders:

        bashCommand = "scrapy crawl " + spider + " -o items.json -t json"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
