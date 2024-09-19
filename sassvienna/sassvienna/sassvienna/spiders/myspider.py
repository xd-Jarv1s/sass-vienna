import scrapy

class SassSpider(scrapy.Spider):
    name = 'myspider'
    start_urls = [
        'https://sassvienna.com/programm',
    ]

    # Scrapy nastavenie pre automatické ukladanie do JSON súboru
    custom_settings = {
        'FEEDS': {
            'sass_events.json': {  # Názov výstupného súboru
                'format': 'json',   # Formát súboru
                'overwrite': True,  # Prepísať súbor pri každom spustení
                'indent': 4,        # Pekné formátovanie JSON
            },
        },
    }

    def parse(self, response):
        self.log(f"Spracúvam stránku: {response.url}")

        # Nájde všetky eventy na stránke
        events = response.xpath('//div[@class="events"]/div[contains(@class, "event")]')

        for event in events:
            # Extrahovanie dát o evente
            day = event.xpath('.//div[@class="date"]//span[@class="day"]/strong/text()').get()
            start_date = event.xpath('.//div[@class="date"]//span[@class="start_date"]/text()').get()
            start_time = event.xpath('.//div[@class="time"]//span[@class="start_time"]/text()').get()
            end_time = event.xpath('.//div[@class="time"]//span[@class="end_time"]/text()').get()
            title = event.xpath('.//div[@class="title"]/h3/text()').get()
            subline = event.xpath('.//div[@class="subline"]/h4/text()').get()
            lineup = event.xpath('.//div[@class="lineup"]//text()').getall()
            lineup_cleaned = ' '.join([l.strip() for l in lineup if l.strip()])
            link = event.xpath('.//a[@class="eventlink"]/@href').get()
            full_link = response.urljoin(link)

            # Predvolená lokácia (ak nie je iná uvedená na stránke udalosti)
            default_location = 'SASS Music Club, Karlsplatz 1, 1010 Wien'

            # Sledovanie odkazu na detailnú stránku eventu
            yield response.follow(full_link, callback=self.parse_event_details, meta={
                'day': day,
                'start_date': start_date,
                'start_time': start_time,
                'end_time': end_time,
                'title': title,
                'subline': subline if subline else '',
                'lineup': lineup_cleaned,
                'link': full_link,
                'location': default_location  # Predvolená lokácia
            })

    def parse_event_details(self, response):
        # Získanie dát o evente z predošlého kroku
        event_data = response.meta

        # Pokus o extrakciu lokácie zo stránky (ak je uvedená)
        location = response.xpath('//p[contains(text(), "SASS Music Club")]/text()').get(event_data['location'])

        # Aktualizácia lokácie, ak bola nájdená
        event_data['location'] = location.strip() if location else event_data['location']

        # Odstránenie nepotrebných polí, ktoré pridáva Scrapy
        filtered_event_data = {k: v for k, v in event_data.items() if k not in [
            'depth', 'download_timeout', 'download_slot', 'download_latency'
        ]}

        # Uloženie spracovaných dát do JSON súboru
        yield filtered_event_data
