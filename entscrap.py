import scrapy
import json
import re
import requests

def authentication_failed(response):
    pass

# scrapy runspider entscrap.py

homeUrl = 'https://ent.istp-france.com/ENT/Login/Login2.aspx'

class entSpider(scrapy.Spider):
    name = 'ent'
    start_urls = [
        'https://ent.istp-france.com/ENT/Eleve/MesNotes.aspx'
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        return scrapy.FormRequest.from_response(
            response,
            formdata={'UserName': 'username', 'Password': 'pass'},
            callback=self.after_login
        )

    def after_login(self, response):

        if authentication_failed(response):
            self.logger.error("Login failed")
            return

        filename = 'res.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        
        username = response.xpath('//li[@class="logo-user"]/text()').get()
        note = response.xpath('//table[@class="Bulletin-table"]/tr/td/text()').getall()
        # s2 = response.xpath('//table[@id="ctl00_MainContent_TabContainer1_TP1_bulletin1_LblNote"]/text()').getall()

        if note is not None:
            r = re.compile("^((?!\r\n).)*$")

            filtered_list = list(filter(r.match, note))
            arrayNote = 'note.json'

            with open(arrayNote, 'w') as fNP:
                json.dump(filtered_list, fNP)

            print(filtered_list)
            content = []
            ru = []
            indices = [i for i, x in enumerate(filtered_list) if x == "10"]
            a = 0
            b = -1
            
            for i in indices :
                a +=1
                b +=1
                content.append(indices[b] - 1)
                ru.append(filtered_list[content[b]])

            arrayNoteC = 'web/note_concat.json'

            with open(arrayNoteC, 'w') as fNPC:
                json.dump([
                    ["title", [username]], 
                    ["notes", ru]
                ], fNPC)

            url = 'url.php'
            myobj = {'note':  [["title", [username]], ["notes", all]]}

            requests.post(url, data = myobj)

print("\nstart scraping\n")    

