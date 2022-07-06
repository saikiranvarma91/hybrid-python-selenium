from base.base_driver import BaseDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utilities.utils import Utility

class AmzSearchResults(BaseDriver):

	log = Utility.custom_logger()
	LOCATOR_TYPE = By.XPATH
	LOCATOR	= "//div[@data-component-type='s-search-result']//h2//a//span"

	def __init__(self,driver):
		super().__init__(driver)
		self.driver = driver
	
	def get_items_searched(self):
		return self.ec_presence_of_all_elements_located(self.LOCATOR_TYPE,self.LOCATOR)

	def get_search_data(self):
		search_data = self.get_items_searched()
		self.log.info("Item Search completed.")
		return search_data

		
		
