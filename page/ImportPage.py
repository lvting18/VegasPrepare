from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page.BasePage import BasePage
from page.MainPage import MainPage
import time
from selenium.webdriver.common.keys import Keys
import random
import allure
import logging


class ImportPage(BasePage):

    # as set default target, every time go to Import page, need collapse C:\
    def iniImport(self):
        time.sleep(3)
        c = self.find(By.XPATH, "//Custom[contains(@AutomationId, 'TargetGridControl')]//Text[contains(@Name, 'C:')]")
        ActionChains(self.driver).double_click(c).perform()

    @allure.step('Back to mainpage from Import page')
    def backtomain(self):
        self.find(By.XPATH, '//Button[contains(@Name, "Close")]').click()
        return MainPage()

    @allure.step('Select MTP device')
    def SelectMTP(self, s_folder):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'self')]//Text[contains(@Name, '%s')]" % s_folder).click()
        self.driver.implicitly_wait(20)
        return self

    @allure.step('Select one whole folder as source')
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
        return self

    @allure.step('Select some files as source')
    def SelectFile(self, s_folder):
        self.SelectSourceFolder(s_folder)
        self.find(By.NAME, 'DMAM.Classes.LocalFile').click()
        i = 0
        j = 0
        while i < random.randint(2, 9):
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ARROW_DOWN).key_up(Keys.SHIFT).perform()
            i += 1
        while j < random.randint(2, 9):
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ARROW_RIGHT).key_up(Keys.SHIFT).perform()
            j += 1
        return self

    def GetSelectedFilesNumber(self):
        selected = self.driver.find_elements_by_xpath(
            "//Custom[contains(@AutomationId, 'ImportDetailPage')]//Button[contains(@AutomationId, 'PageheaderButton')]")[1].text
        self.logger().debug(selected)
        file_number = selected.split()[0]
        self.logger().debug(file_number)
        return int(file_number)

    @allure.step('Select target folder')
    def SelectTargetFolder(self, t_folder):
        t_list = t_folder.split('\\')
        for i in t_list:
            p = self.find(By.XPATH,
                          "//Custom[contains(@AutomationId, 'TargetGridControl')]//Text[contains(@Name, '%s')]" % i)
            ActionChains(self.driver).double_click(p).perform()

    @allure.step(r"New target folder")
    def NewTargetFolder(self, t_folder='F:', target_name='default'):
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

    @allure.step('Click Import button')
    def ClickImport(self):
        self.driver.find_element_by_accessibility_id('importbutton').click()

    @allure.step('Judge if it is importing')
    def IsImportDialogOpen(self):
        i = (By.XPATH, "//Custom[contains(@AutomationId, 'ImportFilesProgressPage')]")
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(i))
            return True
        except:
            return False

    @allure.step('Waiting for importing finished')
    def WaitingImportFinish(self):
        # wait until import finished dialog pop up
        for i in range(600):
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.NAME, 'Go to library')))
                self.logger().debug('Import successfully')
                break
            except:
                self.logger().debug('Not find Go to library')
                try:
                    WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.NAME, 'Retry')))
                    self.logger().debug('Import failed')
                    break
                except:
                    self.logger().debug('Not find Gotolibrary and Retry')
                    continue

    @allure.step('Close Import dialog, stay at Import page')
    def CloseImportDialog(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportFilesResponsePage')]"
                            "//Button[contains(@AutomationId, 'OKButton')]").click()

    @allure.step('Click Go to library button of Import dialog')
    def GoToLibrary(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'ImportFilesResponsePage')]"
                            "//Button[contains(@AutomationId, 'GoToButton')]").click()

    @allure.step('Change view')
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

    @allure.step('Change group')
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

    @allure.step('Change sort')
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

