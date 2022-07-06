from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from base.base_driver import BaseDriver
from utilities.utils import Utility

import time

class AmzHome(BaseDriver):
	
	log = Utility.custom_logger()
	LOCATOR_TYPE 	= By.XPATH
	LOCATOR		= "//input[@id='twotabsearchtextbox']"
	PAGE_LOCATOR	= "//a[contains(@class,'s-pagination-next')]"

	def __init__(self,driver):
		super().__init__(driver)
		self.driver = driver
	
	def click_search_bar(self):
		search_element = self.ec_element_to_be_clickable(self.LOCATOR_TYPE,self.LOCATOR)
		search_element.click()
		search_element.clear()
		return search_element

	def search_keyword(self,search_element,keyword,page_no):
		search_element.send_keys(keyword)
		time.sleep(2)
		search_element.send_keys(Keys.ENTER)
		if page_no>1:
			for loop in range(1,page_no):
				self.scroll_page()
				page_element = self.ec_element_to_be_clickable(self.LOCATOR_TYPE,self.PAGE_LOCATOR)
				page_element.click()
		
		self.scroll_page()
		self.scroll_page("up")

	def search_item(self,keyword,page_no=1):
		search_element = self.click_search_bar()
		self.search_keyword(search_element,keyword,page_no)
		self.log.info("Item Searched with keyword : {}".format(keyword))
		