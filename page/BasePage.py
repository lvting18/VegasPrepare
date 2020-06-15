from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver.Client import WinClient
import yaml
import re
import shutil
import logging


class BasePage(object):

    def __init__(self):
        self.driver: WebDriver = self.getDriver()

    @classmethod
    def getDriver(cls):
        cls.driver = WinClient.driver
        return cls.driver

    @classmethod
    def getClient(cls):
        return WinClient

    def IsMain(self):
        return self.driver.find_element_by_accessibility_id('setting')

    def IsImportPage(self):
        return self.driver.find_element_by_accessibility_id('importbutton')

    def IsPreviewOpen(self):
        close_button = (
            By.XPATH,
            "//Custom[contains(@AutomationId, 'PreviewPlayer')]//Button[contains(@AutomationId, 'BarCloseButton')]")
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(close_button))
            return True
        except:
            return False

    def IsPreviewClose(self):
        detail_button = (By.XPATH, "//Button[contains(@AutomationId, 'Detailsbutton')]")
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(detail_button))
            return True
        except:
            return False

    def IsSetTargetDialogOpen(self):
        t = (By.XPATH, "//Custom[contains(@AutomationId, 'SetTargetDialog')]")
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(t))
            return True
        except:
            return False

    def WaitProgressDialogClosed(self):
        d = (By.XPATH, "//Button[contains(@AutomationId, 'Detailsbutton')]")
        try:
            WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(d))
            return True
        except:
            return False

    def find(self, by, value):
        for i in range(3):
            element = self.driver.find_element(by, value)
            return element

    def logger(self):
        logger = logging.getLogger(__name__)
        # 全局定义最低级别
        logger.setLevel(level=logging.DEBUG)
        # 文件输出信息级别
        handler = logging.FileHandler("log.txt")
        handler.setLevel(logging.DEBUG)
        # 屏幕输出信息级别
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # add formatter
        formatter = logging.Formatter('%(asctime)s - %(module)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        console.setFormatter(formatter)
        # add to logger
        logger.addHandler(handler)
        logger.addHandler(console)
        return logger
