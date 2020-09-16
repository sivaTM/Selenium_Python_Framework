import pytest
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions

from pageObjects.CheckoutPage import CheckOutPage
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass


class TestShoppingPage(BaseClass):

    def test_e2e(self):
        log = self.getLogger()
        homePage = HomePage(self.driver)
        checkoutpage = homePage.shopItems()
        log.info("getting all the card titles")
        cards = checkoutpage.getCardTitles()
        i = -1
        for card in cards:
            i = i + 1
            cardText = card.text
            log.info(cardText)
            if cardText == "Blackberry":
                checkoutpage.getCardFooter()[i].click()

        self.driver.find_element_by_css_selector("a[class*='btn-primary']").click()

        confirmpage = checkoutpage.checkOutItems()
        log.info("Entering country name as ind")
        self.driver.find_element_by_id("country").send_keys("ind")
        # time.sleep(5)
        self.verifyLinkPresence("India")

        self.driver.find_element_by_link_text("India").click()
        self.driver.find_element_by_xpath("//div[@class='checkbox checkbox-primary']").click()
        self.driver.find_element_by_css_selector("[type='submit']").click()
        textMatch = self.driver.find_element_by_css_selector("[class*='alert-success']").text
        log.info("Text received from application is "+textMatch)

        assert ("Success! Thank you!" in textMatch)


    def test_site(self):

        list = []
        list2 = []
        #self.driver = webdriver.Firefox(executable_path="/home/user/Downloads/Selenium_learning/geckodriver")
        self.driver.get("https://rahulshettyacademy.com/seleniumPractise/")
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector("input.search-keyword").send_keys("ber")
        time.sleep(4)
        count =len(self.driver.find_elements_by_xpath("//div[@class='products']/div"))
        assert count == 3
        buttons = self.driver.find_elements_by_xpath("//div[@class='product-action']/button")

        for button in buttons:
            list.append(button.find_element_by_xpath("parent::div/parent::div/h4").text)
            button.click()
        print(list)

        self.driver.find_element_by_css_selector("img[alt='Cart']").click()
        self.driver.find_element_by_xpath("//button[text()='PROCEED TO CHECKOUT']").click()
        wait = WebDriverWait(self.driver, 5)
        wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "promoCode")))
        veggies =self.driver.find_elements_by_css_selector("p.product-name")
        for l in veggies:
            list2.append(l.text)

        print(list2)
        assert list == list2

        amount1= self.driver.find_element_by_css_selector(".discountAmt").text

        self.driver.find_element_by_class_name("promoCode").send_keys("rahulshettyacademy")
        self.driver.find_element_by_css_selector(".promoBtn").click()
        print(self.driver.find_element_by_css_selector("span.promoInfo").text)

        amount2= self.driver.find_element_by_css_selector(".discountAmt").text

        assert int(amount1) > float(amount2)

        veggiesAmount = self.driver.find_elements_by_xpath("//tr/td[5]/p")
        sum = 0

        for v in veggiesAmount:
            sum = sum + int(v.text)

        print(sum)
        self.driver.close()
        #assert sum == int(amount2)

