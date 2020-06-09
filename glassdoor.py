#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from setup import SetUpBrowser as Browser
import getopt
import getpass
import os
import random
import re
import setup
import string
import sys
import time


global glassdoor, variables, allURLs

APPLICANT_INFO = {
    "First Name": "Hello",
    "Last Name": "World",
    "Email Address": "hello@world.com",
    "Phone Number": "123-456-7890",
    "Current Company": "Python",
    "LinkedIn Profile": "https://google.com"
}


def apply():
    page = 1

    # Load the list of variables for Glassdoor
    with open("var_glassdoor.txt", "r") as f:
        global variables
        variables = {}
        for line in f:
            (key, value) = line.split('=', 1)
            value.rstrip()
            variables.update({key: value})

    # Open browser and go to Glassdoor login page.
    global glassdoor
    glassdoor = Browser(variables["url"])
    glassdoor.browser.fullscreen_window()

    # Sign In
    glassdoor.sign_in(variables["email_field_xpath"],
                      variables["password_field_xpath"], variables["signIn_button_xpath"])
    time.sleep(3)
    glassdoor.browser.fullscreen_window()

    # Perform job search
    glassdoor.perform_search(
        variables["search_field_xpath"], variables["location_field_xpath"], variables["search_button_xpath"])
    time.sleep(5)
    glassdoor.browser.fullscreen_window()

    next_url = ''
    global allURLs
    allURLs = []
    while page < 3:
        if page == 1:
            application_links = get_apply_links()
            allURLs.extend(application_links)
            page2 = glassdoor.locate_element(variables["page2_field_xpath"])
            # Get url of page 2
            next_url = page2.get_attribute("href")
            page += 1
            time.sleep(2)
        else:
            glassdoor.browser.get(next_url)
            application_links = get_apply_links()
            allURLs.extend(application_links)
            # Using regex to break the url into parts: url, pagenumber & the tailing ".htm"
            r = re.search(
                '(?P<url>[^;]*?)(?P<pagenum>)(?P<html>.htm)', next_url)
            # Increment page
            page += 1
            # Update the url to the next page
            # From page 2 on, the URL structure are the same, except for the trailing parts _IP#.htm
            # in which # indicates the current page number
            next_url = f"{r.group('url')}{page}.htm"
            time.sleep(5)

    allLinks = set(allURLs)

    for link in allLinks:
        if 'www.glassdoor.com' in link:
            apply_on_glassdoor(link)

    time.sleep(10)
    glassdoor.close_browser()


# When clicking the links with "GD_JOB_VIEW" on Glassdoor, users usually get redirected to another page.
# This function retrieves all the new urls and put them in a list
def get_redirected_links(links_list):
    chromedriver_path = "./chromedriver.exe"
    urls_list = []
    driver = webdriver.Chrome(chromedriver_path)
    for link in links_list:
        driver.get(link)
        time.sleep(3)
        temp = driver.current_url
        if temp not in urls_list:
            urls_list.append(temp)

    time.sleep(3)
    driver.quit()

    return urls_list


def get_apply_links():
    job_lists = glassdoor.browser.find_elements_by_xpath(
        variables["job_listing_card"])

    allLinks = []
    for listing in job_lists:
        href = listing.get_attribute("href")
        '''
        Replace "GD_JOB_AD" with "GD_JOB_VIEW"
        When viewing the URL with "GD_JOB_AD", users have to click "Apply" button land on application page
        With "GD_JOB_VIEW" URL, users are navigated on the direct application page.
        '''
        href = href.replace("GD_JOB_AD", "GD_JOB_VIEW")
        if href not in allLinks:
            allLinks.append(href)

    apply_links = get_redirected_links(allLinks)

    return apply_links


def apply_on_glassdoor(link):
    glassdoor.browser.get(link)
    easyApply = glassdoor.locate_element(variables["easy_apply_button_xpath"])
    easyApply.click()
    time.sleep(5)

    # Complete the application form

    # Select Resume
    resumeDropDown = glassdoor.locate_element(
        variables["gdModal_selectResume_field"])
    resumeFile = glassdoor.locate_element(
        variables["gdModal_resumeFile_field"])
    resumeDropDown.click()
    time.sleep(1)
    resumeFile.click()
    time.sleep(3)

    # Input First Name
    fName = glassdoor.locate_element(variables["gdModal_firstName_field"])
    fName.send_keys(APPLICANT_INFO["First Name"])
    time.sleep(1)

    # Input Last Name
    lName = glassdoor.locate_element(variables["gdModal_lastName_field"])
    lName.send_keys(APPLICANT_INFO["Last Name"])
    time.sleep(1)

    # Input Email Address
    eAddress = glassdoor.locate_element(
        variables["gdModal_emailAddress_field"])
    eAddress.send_keys(APPLICANT_INFO["Email Address"])
    time.sleep(1)

    # Input Phone Number
    pNumber = glassdoor.locate_element(
        variables["gdModal_phoneNumber_field"])
    pNumber.send_keys(APPLICANT_INFO["Phone Number"])

    # Apply
    pApply = glassdoor.locate_element(var["gdModal_applyButton_field"])
    pApply.click()
    time.sleep(5)

