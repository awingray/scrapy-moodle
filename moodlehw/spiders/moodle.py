# -*- coding: utf-8 -*-
import scrapy
from moodlehw.items import MoodlehwItem

class MoodleSpider(scrapy.Spider):
    name = "moodle"
    allowed_domains = ["moodle.standrews.ac.th"]
    start_urls = ('http://moodle.standrews.ac.th',)

    def parse(self, response):
        username = raw_input('Enter Username: ')
        password = raw_input('Enter Password: ')
        return scrapy.FormRequest(
                'http://moodle.standrews.ac.th/login/index.php',
                formdata={'username': username, 'password': password},
                callback=self.parseIndex)

    def parseIndex(self, response):
        # check login succeed before going on
        if "Invalid login" in response.body:
            self.log("Login failed", level=scrapy.log.ERROR)
            return
        print("Login Successful")
	return scrapy.Request("http://moodle.standrews.ac.th/mod/homework/view.php?h=2", callback=self.parseHW)

    def parseHW(self, response):
	user = MoodlehwItem()
	user['studentname'] = response.xpath("//h1[@class='studentname']/text()").extract()
	hwslider = response.xpath("//div[@id='hw_slider']/*")
	for div in hwslider.xpath(".//div[@class='title']"):
	    user['task'] = div.xpath("@title").extract()
	    yield user

    


