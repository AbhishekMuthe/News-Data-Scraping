from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import re
heading =[]
Description =[]
news_links = []
search_no = 1
search_result_no = []
number = 0
driver = webdriver.Chrome('C:/users/abhishek/Downloads/ChromeDriver/chromedriver.exe')
driver.maximize_window()
sleep(0.5)
Domain = 'https://www.google.com'
driver.get(Domain)
search_input = driver.find_element_by_name('q')
search_input.send_keys('indian crime news in english')
sleep(1)
search_input.send_keys(Keys.RETURN)
sel = Selector(text=driver.page_source)
News_Section = sel.xpath('//div[1]/div/div[2]/a/@href').extract_first()
driver.get(Domain + News_Section)
sleep(1)
while True:
	try:
		sleep(1)
		sel= Selector(text=driver.page_source)
		links = sel.xpath('//div/div/div[2]/a/@href').extract()
		news_headings = sel.xpath('//a/div/div[2]/div[2]/text()').extract()
		Descs = sel.xpath('//div/div/div[2]/a/div/div[2]/div[3]/div[1]/text()').extract()
		number = sel.xpath('//table/tbody/tr/td/text()').extract_first()
		for news_heading, Desc, link in zip(news_headings,Descs,links):
			reg = re.compile("[\w,.!?]")
			if reg.match(news_heading):
				heading.append(news_heading.replace("\n", ""))
				Description.append(Desc.replace("\n", ""))
				news_links.append(link)
				search_result_no.append(search_no)
				search_no+=1
		if(int(number) == 10):
			driver.quit()
			break
		a = driver.find_element_by_xpath('//*[@id="pnnext"]')
		a.click()
		sleep(1)
	except NoSuchElementException:
		driver.quit()
		break
df = pd.DataFrame({"search_result_number": search_result_no, "Search_Result_Title": heading, "Search_Result_URL": news_links, "Search_Result_Description": Description})
df.to_csv('news_data.csv', index=False)