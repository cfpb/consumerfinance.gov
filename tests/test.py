import nose

from selenose.cases import SeleniumTestCase

class NewsroomTestCase(SeleniumTestCase):
    def setUp(self):
        self.driver.get('http://refresh.demo.cfpb.gov/newsroom/')

    def test_get(self):
        assert "Newsroom" in self.driver.title

    def test_filter_display_button(self):
        filter_button = self.driver.find_element_by_class_name('expandable_target__btn__secondary')
        filter_button.click()
        filter_options = self.driver.find_element_by_class_name('padded-container')
        assert filter_options.is_displayed()

    def test_filter_oped_search(self):
        filter_button = self.driver.find_element_by_class_name('expandable_target__btn__secondary')
        filter_button.click()
        oped_checkbox = self.driver.find_element_by_xpath('//label/span[contains(text(), "Op-Ed")]/..')
        oped_checkbox.click()
        assert "is-checked" in oped_checkbox.get_attribute('class')

if __name__ == '__main__':
   nose.main()
