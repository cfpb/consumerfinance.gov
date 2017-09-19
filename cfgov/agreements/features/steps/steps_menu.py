from behave import given, when, then
from hamcrest import *

__author__ = 'CFPBLabs'

agency_name = 'Consumer Financial Protection Bureau'

# Given statements


# When statements

@when('I hover over "{menu_item}" menu')
def step(context, menu_item):
    context.website.open_menu_item(menu_item)

@when('I click on "{sub_menu_link}" item')
def step(context, sub_menu_link):
    context.website.open_submenu_link(sub_menu_link)

# Then statements

