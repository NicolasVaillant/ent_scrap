# ent_scrap
A basic python scraper for extract all notes from my ENT

---

1. *pip install scrapy* to add the scraper library 
2. Change the *username* and *pass* variables 
3. Change *url* variable to POST data to php file (optionnal)
4. **Run** scrapy runspider entscrap.py

Finally, this file will create : 
- *res.html* (scraped page) 
- *note.json* (all notes with subject and average)
- *note_concat.json* (all notes one by one, ordered chronologically)
