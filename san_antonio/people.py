from lxml.html import fromstring
from pupa.scrape import Scraper
from pupa.scrape import Person


class SanAntonioPersonScraper(Scraper):
    base_url = "https://www.sanantonio.gov/"

    def scrape(self):
        council_url = "{}Council".format(self.base_url)
        page_as_text = self.get(council_url).text
        page = fromstring(page_as_text)
        page.make_links_absolute(self.base_url)

        council_members_xpath = "//div[@class[starts-with(.,"\
                                "'council-featured-person-small')]]"
        role = "Council Member"
        for member_element in page.xpath(council_members_xpath):
            name = member_element.xpath("h4[2]")[0].text.replace(u"\u00a0", " ")
            image = member_element.xpath("a/img")[0].get("src")
            district_info = member_element.xpath("h4/a")[0]
            district_name = district_info.text.replace(u"\u00a0", " ")
            district_homepage = district_info.get("href")
            biography = member_element.xpath("p/a")[0].get("href")
            email = member_element.xpath("h5/a")[0].get("href")
            phone_number = member_element.xpath("h5[1]")[0].text.replace(".", "-")
            council_member = Person(
                name=name,
                role=role,
                district=district_name,
                primary_org='legislature',
                image=image,
                biography=biography
            )
            council_member.add_link(district_homepage)
            council_member.add_source(council_url)
            council_member.add_contact_detail(type="email", value=email)
            council_member.add_contact_detail(type="voice", value=phone_number)
            
            yield council_member
