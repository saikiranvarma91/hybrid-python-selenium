from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

import time

class BaseDriver:
	WAIT_TIME = 10	
	def __init__(self,driver):
		self.driver = driver
		self.wait = WebDriverWait(self.driver,self.WAIT_TIME)

	def scroll_page(self,direction="down"):
		if direction == "down":
			page_length = self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);return document.body.scrollHeight;")
			time.sleep(2)
			status = True
			while status:
				temp_page_length = self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);return document.body.scrollHeight;")	
				if page_length == temp_page_length:
					status = False
				page_length = temp_page_length			

		elif direction == "up":		
			page_length = self.driver.execute_script("window.scrollTo(0,0);")


	def ec_element_to_be_clickable(self,locator_type,locator):
		try:
			return self.wait.until(EC.element_to_be_clickable((locator_type,locator)))
		except WebDriverException:
			return False

	def ec_presence_of_all_elements_located(self,locator_type,locator):
		try:
			return self.wait.until(EC.presence_of_all_elements_located((locator_type,locator)))
		except WebDriverException:
			return False
