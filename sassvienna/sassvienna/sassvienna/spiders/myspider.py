import scrapy

class SassSpider(scrapy.Spider):
    name = 'myspider'
    start_urls = [
        'https://sassvienna.com/programm',
    ]

    # Scrapy settings for automatic saving to a JSON file
    custom_settings = {
        'FEEDS': {
            'sass_events.json': {  # Name of the output file
                'format': 'json',   # File format
                'overwrite': True,  # Overwrite the file with each run
                'indent': 4,        # Pretty JSON formatting
            },
        },
    }

    def parse(self, response):
        self.log(f"Processing page: {response.url}")

        # Find all events on the page
        events = response.xpath('//div[@class="events"]/div[contains(@class, "event")]')

        for event in events:
            # Extract event data
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

            # Default location (if not otherwise specified on the event page)
            default_location = 'SASS Music Club, Karlsplatz 1, 1010 Wien'

            # Following the link to the event's detailed page
            yield response.follow(full_link, callback=self.parse_event_details, meta={
                'day': day,
                'start_date': start_date,
                'start_time': start_time,
                'end_time': end_time,
                'title': title,
                'subline': subline if subline else '',
                'lineup': lineup_cleaned,
                'link': full_link,
                'location': default_location  # Default location
            })

    def parse_event_details(self, response):
        # Retrieve event data from the previous step
        event_data = response.meta

        # Attempt to extract the location from the page (if specified)
        location = response.xpath('//p[contains(text(), "SASS Music Club")]/text()').get(event_data['location'])

        # Update the location if it was found
        event_data['location'] = location.strip() if location else event_data['location']

        # Remove unnecessary fields added by Scrapy
        filtered_event_data = {k: v for k, v in event_data.items() if k not in [
            'depth', 'download_timeout', 'download_slot', 'download_latency'
        ]}

        # Save the processed data to a JSON file
        yield filtered_event_data
