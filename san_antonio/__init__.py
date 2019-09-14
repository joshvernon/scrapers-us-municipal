# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .people import SanAntonioPersonScraper
from .events import SanAntonioEventsScraper


class SanAntonio(Jurisdiction):
    division_id = "ocd-division/country:us/state:tx/place:san_antonio"
    classification = "government"
    name = "City of San Antonio"
    url = "https://www.sanantonio.gov/"
    scrapers = {
        "people": SanAntonioPersonScraper,
        "events": SanAntonioEventsScraper,
    }

    def get_organizations(self):
        org = Organization(name="San Antonio City Council", classification="legislature")
        for i in range(1, 11):
            org.add_post(
                label="District {0}".format(i),
                role="Council Member",
                division_id="{0}/council_district:{1}".format(self.division_id, i)
            )
        
        yield org
