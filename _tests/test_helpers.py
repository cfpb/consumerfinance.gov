from time import sleep

def click_filter_posts(test):
    test.filter_dropdown_button = test.driver.find_element_by_xpath('//button[contains(text(), "Filter posts")]/..')
    if test.filter_dropdown_button.get_attribute('aria-pressed') == 'false':
        test.filter_dropdown_button.click()
        sleep(1)

def coerce_category(category):
    if category.find(' ') != -1:
        category = category.replace(' ', '+')
    elif category.find('+') != -1:
        category = category.replace('+', ' ')

    return category

def scroll_to_element(driver, element):
    driver.execute_script(
        "window.scrollTo(" + str(element.location['x']) + ", " + str(element.location['y']) + ");"
    )