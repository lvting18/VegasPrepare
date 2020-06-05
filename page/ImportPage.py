from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page.BasePage import BasePage
from page.MainPage import MainPage
import time
from selenium.webdriver.common.keys import Keys
import random


class ImportPage(BasePage):

    # as set default target, every time go to Import page, need collapse C:\
    def iniImport(self):
        time.sleep(3)
        c = self.find(By.XPATH, "//Custom[contains(@AutomationId, 'TargetGridControl')]//Text[contains(@Name, 'C:')]")
        ActionChains(self.driver).double_click(c).perform()

    # Back to mainpage from Import page
    def backtomain(self):
        self.find(By.XPATH, '//Button[contains(@Name, "Close")]').click()
        return MainPage()

    def SelectMTP(self, s_folder):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'self')]//Text[contains(@Name, '%s')]" % s_folder).click()

    # Select one whole folder as source
    def SelectSourceFolder(self, s_folder):
        folder_code = 'DMAM.Classes.LocalDirectory'
        s_list = s_folder.split('\\')
        for i in s_list:
            n = s_list.index(i)
            # print(n)
            s_xpath = "//TreeItem[contains(@Name, '%s')]" % folder_code * (n + 1) + "//Text[contains(@Name, '%s')]" % i
            # print(s_xpath)
            p = self.find(By.XPATH, s_xpath)
            ActionChains(self.driver).double_click(p).perform()

    # Select some files as source
    def SelectFile(self, s_folder):
        self.SelectSourceFolder(s_folder)
        self.find(By.NAME, 'DMAM.Classes.LocalFile').click()
        i = 0
        j = 0
        while i < random.randint(1, 5):
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ARROW_DOWN).key_up(Keys.SHIFT).perform()
            i += 1
        while j < random.randint(1, 5):
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ARROW_RIGHT).key_up(Keys.SHIFT).perform()
            j += 1

    # Select target folder
    def SelectTargetFolder(self, t_folder):
        t_list = t_folder.split('\\')
        for i in t_list:
            p = self.find(By.XPATH,
                          "//Custom[contains(@AutomationId, 'TargetGridControl')]//Text[contains(@Name, '%s')]" % i)
            ActionChains(self.driver).double_click(p).perform()

    # New target folder to G:\ as default
    def NewTargetFolder(self, t_folder='G:', target_name='default'):
        t_list = t_folder.split('\\')
        # print(t_list)
        for i in t_list:
            p = self.find(By.XPATH,
                          "//Custom[contains(@AutomationId, 'TargetGridControl')]//Text[contains(@Name, '%s')]" % i)
            ActionChains(self.driver).double_click(p).perform()
        # # use G:\ as target folder as default, select [4]
        # self.driver.find_elements_by_accessibility_id('AddButton')[4].click()
        ActionChains(self.driver).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        if target_name == 'default':
            target_name = time.strftime('target_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.driver.find_element_by_accessibility_id("EnterName").send_keys(target_name)
        self.driver.find_element_by_accessibility_id('okbutton').click()
        t_list.append(target_name)
        target_path = "\\".join(t_list)
        return target_path

    def ClickImport(self):
        self.driver.find_element_by_accessibility_id('importbutton').click()

    def IsImporting(self):
        if self.driver.find_elements_by_accessibility_id('OKButton'):
            return True
        else:
            return False

    def WaitingImportFinish(self):
        # wait until import finished dialog pop up
        WebDriverWait(self.driver, 3600, 1).until(
            EC.visibility_of_element_located((By.NAME, 'Go to library')))

    def CloseImportDialog(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportFilesResponsePage')]"
                            "//Button[contains(@AutomationId, 'OKButton')]").click()

    def GoToLibrary(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportFilesResponsePage')]"
                            "//Button[contains(@AutomationId, 'GoToButton')]").click()

    def ChangeView(self, view='all'):
        all_views = ['ViewbyList', 'ViewbySmall', 'ViewbyMedium', 'ViewbyLarge']
        random.shuffle(all_views)
        if view == 'random':
            v = [all_views.pop()]
            all_views = v
        for viewby in all_views:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportDetailPage')]"
                                "//Button[contains(@AutomationId, 'ViewbyButton')]").click()
            self.driver.find_element_by_accessibility_id(viewby).click()

    def ChangeGroup(self, group='all'):
        all_groups = ['GroupbyNone', 'GroupbyDate', 'GroupbyType']
        random.shuffle(all_groups)
        if group == 'random':
            g = [all_groups.pop()]
            all_groups = g
        for groupby in all_groups:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportDetailPage')]"
                                "//Button[contains(@AutomationId, 'GroupbyButton')]").click()
            self.driver.find_element_by_accessibility_id(groupby).click()

    def ChangeSort(self, sort='all'):
        all_sorts = ['SortbyName', 'SortbyDate', 'SortbyFolder', 'SortbyType', 'SortbySize']
        random.shuffle(all_sorts)
        if sort == 'random':
            random.shuffle(all_sorts)
            s = [all_sorts.pop()]
            all_sorts = s
        for sortby in all_sorts:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportDetailPage')]"
                                "//Button[contains(@AutomationId, 'SortbyButton')]").click()
            self.driver.find_element_by_accessibility_id(sortby).click()

