import softest
import pytest
from ddt import ddt, data, file_data, idata, unpack
from pages.amz_home import AmzHome
from pages.amz_search_results import AmzSearchResults
from utilities.utils import Utility

@pytest.mark.usefixtures("setUp")
@ddt
class TestAmzHome(softest.TestCase):
	
	ut = Utility()
	@pytest.fixture(autouse=True)
	def class_setup(self):
		self.amzh	= AmzHome(self.driver)
		self.amzsr	= AmzSearchResults(self.driver)

	#data here
	#@data(("python programming",3),("java programming",1),("datascience programming",1))
	#@unpack
	#for .json	
	#@file_data("../testdata/testdata.json")
	#for .yaml | pip install PyYAML
	#@file_data("../testdata/testdata.yaml")

	#@data(*ut.get_excel_data("./testdata/testdata.xlsx","Sheet1"))
	@data(*ut.get_csv_data("./testdata/testdata.csv"))
	@unpack
	def test_search(self, search_word, page_no):
		self.amzh.search_item(search_word, int(page_no))
		search_data = self.amzsr.get_search_data()
		items = self.ut.get_items_text(search_data)
		self.ut.display_data(items)
		