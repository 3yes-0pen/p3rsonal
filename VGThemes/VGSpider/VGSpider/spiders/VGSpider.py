import scrapy
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter

class VGSpider(scrapy.Spider):
    name = 'VGdata'
    start_urls = [
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=1995&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=1996&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=1997&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=1998&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=1999&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2000&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2001&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2002&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2003&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2004&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2005&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2006&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2007&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2008&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2009&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2010&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2011&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2012&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2013&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2014&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2015&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2016&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2017&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2018&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2019&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2020&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2021&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2022&distribution=&sort=desc&view=detailed',
        'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=2023&distribution=&sort=desc&view=detailed',
    ]
    scraped_items = set()
    def parse(self, response):
        games = response.css(".clamp-summary-wrap")
        for game in games[:10]:
            name = game.css("a.title h3::text").get().strip()
            if name in self.scraped_items:
                continue
            self.scraped_items.add(name)
            yield {
                "name": game.css("a.title h3::text").get().strip(),
                "platform": game.css("div.platform span.data::text").get().strip(),
                "user_rating": game.css("div.metascore_w.user.large.game.positive::text, div.metascore_w.large.game.mixed::text").extract_first(default='').strip(),
                "critic_rating": game.css("div.metascore_w.large.game.positive::text").get().strip(),
                "release_date": game.css('div.clamp-details span:not(.label):not(.data)::text').get().strip(),
                "summary": game.css("div.summary::text").get().strip()
            }

class CSVPipeline:
    def open_spider(self, spider):
        self.file = open("VGoutput.csv", "wb")
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    