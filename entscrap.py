import scrapy
from scrapy.crawler import CrawlerProcess
import json
import numpy as np
from lxml import etree

def authentication_failed(response):
    pass

# scrapy runspider entscrap.py

homeUrl = 'https://ent.istp-france.com/ENT/Login/Login2.aspx'

class entSpider(scrapy.Spider):
    name = 'ent'
    start_urls = [
        'https://ent.istp-france.com/ENT/Eleve/Default.aspx'
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        return scrapy.FormRequest.from_response(
            response,
            formdata={'UserName': '', 'Password': ''},
            callback=self.after_login
        )

    def after_login(self, response):

        if authentication_failed(response):
            self.logger.error("Login failed")
            return


        # filename = 'res.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        note = response.xpath('//*[@id="ctl00_MainContent_TabContainer1_TP2_GridView1"]').getall()

        if note is not None:
            notesEnt = []
            notesFile = []
            table = etree.HTML(str(note)).find("body/table")
            rows = iter(table)
            headers = [col.text for col in next(rows)]
            for row in rows:
                values = [col.text for col in row]
            
                result = zip(headers, values)
                notesEnt.append(list(result))
        
            arrayNote = 'note.json'

            with open(arrayNote, 'w') as fNP:
                json.dump(notesEnt, fNP)

            print("---")

            # print(type(notes))
            print(notesEnt)
            
            print("---")
            f = open(arrayNote, "r")
            # print(type(f.read()))
            # notesFile((f.read()).split())

            print(f.read())
            
            print("---")
            
            from_ent = np.array(notesEnt)
            from_array = np.array(f.read())
            print((from_ent == from_array).all())
            
            print("---")

            for i in range(len(notesEnt)) : 
                new = {
                    'date' : notesEnt[i][0][1],
                    'cours' : notesEnt[i][1][1],
                    'intervenant' : notesEnt[i][2][1],
                    'note' : notesEnt[i][3][1]
                }

                print(new)

            
if __name__ == "__main__":
    print("\nstart scraping\n")   
   
