from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os

import pytest
import time
from datetime import datetime

@pytest.fixture(scope="class")
def setUp(request,browser,url):
	global driver
	if browser=='chrome' or browser==None:
		driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager(path='./utilities/chrome').install()))	
	
	elif browser=='edge':
		driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager(path="./utilities/edge").install()))

	if url==None:
		url = "https://www.amazon.in/"
			
	request.cls.driver = driver
	driver.maximize_window()
	driver.get(url)
	time.sleep(2)
	yield
	time.sleep(2)
	driver.close()


def pytest_addoption(parser):
	parser.addoption("--browser")
	parser.addoption("--url")

@pytest.fixture(scope="class",autouse=True)
def browser(request):
	return request.config.getoption("--browser")

@pytest.fixture(scope="class",autouse=True)
def url(request):
	return request.config.getoption("--url")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.htmlpath = './reports/'+datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%p_")+'report.html'

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
	pytest_html = item.config.pluginmanager.getplugin("html")
	outcome = yield
	report = outcome.get_result()
	extra = getattr(report, "extra", [])
	if report.when == "call":
		# always add url to report
		extra.append(pytest_html.extras.url(driver.current_url))
		xfail = hasattr(report, "wasxfail")
		if (report.skipped and xfail) or (report.failed and not xfail):
			# only add additional html on failure
			report_directory = "./reports/screen_shots/"
			#file_name = "test.png"
			file_name = str(int(round(time.time()*1000)))+".png"
			destinationFile = report_directory+file_name
			driver.save_screenshot(destinationFile)
			img_src = 'screen_shots/'+file_name
			
			html = ""
			if file_name:
				html = "<div><img src='{}' alt='screenshot' style='width:35%' onclick='window.open(this.src)' align='right'/></div>".format(img_src)
			extra.append(pytest_html.extras.html(html))
			report.extra = extra

def pytest_html_report_title(report):
	report.title = "Amazon Website Testing"
