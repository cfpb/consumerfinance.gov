import os
import ConfigParser
from selenium import webdriver
from steps.website import *

__author__ = 'CFPBLabs'


def before_all(context):
    config = ConfigParser.ConfigParser()
    config.read('features/environment.cfg')

    directory = config.get('general', 'testing_output')
    if not os.path.exists(directory):
        os.makedirs(directory)

    delay_secs = 5
    if config.has_option("browser_testing", "delay"):
        delay_secs = config.getint("browser_testing", "delay")

    base_url = 'http://localhost'
    if config.has_option('browser_testing', 'base_url'):
        base_url = config.get('browser_testing', 'base_url')

    context.take_screenshots = False
    if config.has_option('browser_testing', 'take_screenshots'):
        context.take_screenshots = config.getboolean(
            'browser_testing', 'take_screenshots')

    browser = 'Chrome'
    if config.has_option('browser_testing', 'browser'):
        browser = config.get('browser_testing', 'browser')

    if browser == 'Phantom':
        driver = webdriver.PhantomJS()
    else:  # Use Chrome as the default
        chromedriver_path = ''

        if config.has_option('chrome_driver', 'chromedriver_path'):
            chromedriver_path = config.get(
                'chrome_driver', 'chromedriver_path')

        driver = webdriver.Chrome(chromedriver_path)

    # Create context property for Website interaction
    context.website = Website(base_url, driver, delay_secs)


def after_all(context):
    context.website.close_browser()
