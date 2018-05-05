import web_scraping
import extractKeywords
import merge_csv

def compileSiteDetails():
	web_scraping.web_scraper()
	extractKeywords.extractKeywords()
	merge_csv.merge_csv()

# compileSiteDetails()

