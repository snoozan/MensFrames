# Scrapy settings for FrameScrapper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'FrameScrapper'

SPIDER_MODULES = ['FrameScrapper.spiders']
NEWSPIDER_MODULE = 'FrameScrapper.spiders'

ITEM_PIPELINES = {
    'FrameScrapper.pipelines.XmlExportPipeline'
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'FrameScrapper (+http://www.yourdomain.com)'
