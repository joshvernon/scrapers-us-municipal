from datetime import datetime, timedelta

from legistar.events import LegistarAPIEventScraper
from pupa.scrape import Event, Scraper


class SanAntonioEventsScraper(LegistarAPIEventScraper, Scraper):
    BASE_URL = "https://webapi.legistar.com/v1/sanantonio"
    WEB_URL = "https://sanantonio.legistar.com/"
    EVENTSPAGE = "https://sanantonio.legistar.com/Calendar.aspx"
    TIMEZONE = "America/Chicago"

    def scrape(self, window=3):
        n_days_ago = datetime.utcnow() - timedelta(days=float(window))
        for api_event, event in self.events(n_days_ago):
            event_id = str(api_event["EventId"])
            when = api_event["start"]
            body_name = api_event["EventBodyName"]

            location = api_event["EventLocation"]
            if location:
                location = location.replace("\r\n", "")
            else:
                location = "No location specified"
            
            description = "{0} - {1}".format(
                body_name, when.strftime("%m-%d-%Y %I:%M %p")
            )
            
            e = Event(
                name=body_name,
                start_date=when,
                description=description,
                location_name=location,
                status=api_event['status']
            )
            e.pupa_id = event_id
            self.addDocs(e, event, 'Agenda')
            self.addDocs(e, event, 'Minutes')
            e.add_source(
                "{0}/events/{1}".format(self.BASE_URL, event_id),
                note="api"
            )
            yield e
