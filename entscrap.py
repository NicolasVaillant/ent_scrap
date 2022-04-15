# -*- coding: utf-8 -*-
from email import message
from re import M
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import unicodedata
import numpy as np
import smtplib
from lxml import etree
import smtplib
from email.message import EmailMessage


def authentication_failed(response):
    pass

# scrapy runspider entscrap.py

homeUrl = 'https://ent.istp-france.com/ENT/Login/Login2.aspx'
from keys import ent_username, ent_password, stmp_password, stmp_sender, stmp_receiver

def sendMail(FROM, TO, sender, mdp, subject, link, notes):
    print("Sending mail...")
    SUBJECT = "Nouvelle(s) note(s) disponible(s) sur l'ENT"
    
    TEXT = "Mail automatique - merci de ne pas y repondre.<br><br>"

    FOOTER = """<br>Consulter votre note via le lien suivant (authentification requise) : <a style="color: #5a5ad0;font-weight: bold;">{}</a>.""".format(link)

    content = ""
    for word in notes:
        e = word.split(',')
        lines = """
        <div style="padding:.5em;margin-bottom:.5em;background-color:#eee;font-family: 'Helvetica', 'Roboto', sans-serif;width:100%;border-radius: 5px;">
            <div style="font-family : 'Helvetica','Roboto', sans-serif;">Date : {}</div>
            <div style="font-family : 'Helvetica', 'Roboto', sans-serif;">Cours : {}</div>
            <div style="font-family : 'Helvetica', 'Roboto', sans-serif;">Intervenant : {}</div>
            <div style="color: #5a5ad0;font-weight: bold;">Note : {}</div>
        </div>
        """.format(e[0], e[1], e[2], e[3])

        content += str(lines)

    message = EmailMessage()
    message['Subject'] = 'Nouvelle(s) note(s) disponible(s) sur l\'ENT'
    message['From'] = FROM 
    message['To'] = TO 
    message.set_content('See below')

    contenu = """
    <!DOCTYPE html>
    <html>
        <body style="font-family:'Helvetica','Roboto', sans-serif;">
            <div style="width:100%;height:auto;color: #5a5ad0;font-weight: bold;">{}</div>
            <div style="width:100%;height:auto; padding:1em 0">{}</div>
            <div style="width:100%;height:auto;">{}</div>
        </body>
    </html>
    """.format(TEXT, content, FOOTER)

    message.set_content(contenu, subtype='html')

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, mdp)
        server.send_message(message)
        server.close()
        print('successfully sent the mail')
    except smtplib.SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        print(error_code, error_message)

class entSpider(scrapy.Spider):
    name = 'ent'
    start_urls = [
        'https://ent.istp-france.com/ENT/Eleve/Default.aspx'
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        return scrapy.FormRequest.from_response(
            response,
            formdata={'UserName': ent_username, 'Password': ent_password},
            callback=self.after_login
        )

    def after_login(self, response):

        if authentication_failed(response):
            self.logger.error("Login failed")
            return

        note = response.xpath('//*[@id="ctl00_MainContent_TabContainer1_TP2_GridView1"]').getall()

        if note is not None:
            notesEnt = []
            notesFile = []
            table = etree.HTML(str(note)).find("body/table")
            rows = iter(table)
            headers = [col.text for col in next(rows)]
            for row in rows:
                values = [col.text for col in row]
                notesEnt.append(values)
        

            values = ','.join(str(v) for v in notesEnt)
            valuesNA = ''.join((c for c in unicodedata.normalize('NFD', values) if unicodedata.category(c) != 'Mn'))
            
            arrayNote = 'note.json'

            with open(arrayNote, 'w') as fNP:
                json.dump(valuesNA, fNP)
            
            f = open(arrayNote, "r")
            
            from_ent = np.array(valuesNA)
            from_array = np.array(f.read()[1:-1])

            print(valuesNA)
            print(len(valuesNA))
            all = []
            for note in notesEnt : 
                print(note)
                notesE = ','.join(str(v) for v in note)
                notesNA = ''.join((c for c in unicodedata.normalize('NFD', notesE) if unicodedata.category(c) != 'Mn'))
                all.append(notesNA)
    

            if((from_ent == from_array).all() == True):
                sendMail(
                    stmp_sender, 
                    stmp_receiver if isinstance(stmp_receiver, list) else [stmp_receiver],
                    stmp_sender,
                    stmp_password,
                    'Nouvelle(s) note(s) disponible(s)',
                    'https://ent.istp-france.com/ENT/Eleve/MesNotes.aspx',
                    all
                )

            
if __name__ == "__main__":
    print("\nstart scraping\n")   
    # process = CrawlerProcess({
    #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    # })

    # process.crawl(entSpider)
    # process.start() # the script will block here until the crawling is finished

