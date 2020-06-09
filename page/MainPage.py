import random
import sys

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from page.BasePage import BasePage
import time
import custom_method.vpmethod as vm
import custom_method.CompareImages as cs


class MainPage(BasePage):
    t = ''

    def gotoImport(self):
        from page.ImportPage import ImportPage
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'importb')]").click()
        return ImportPage()

    def gotoSettings(self):
        from page.SettingsPage import SettingsPage
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'setting')]").click()
        return SettingsPage()

    # select random item
    def select_item(self, s_type, s_path='random'):
        folder_code = ''
        xpath_list = []
        # 从数据库随机取一个id以及它的父节点，以列表的形式返回
        path_list = vm.db_random(s_type)
        # 从列表的最后一位取id
        item_id = path_list.pop()
        # 如果调用的函数的时候，传入了path，通过字符串分割法，生成列表
        if s_path is not 'random':
            path_list = s_path.split('\\')
        # 此时列表里是文件目录的名称[a,b,c], a是All下面的第一层，c是子
        # 针对library和collection，合成相应的xpath，[a_xpath, b_xpath, c_xpath]
        if s_type == 'library':
            folder_code = 'DMAM.Classes.DataDirectory'
        elif s_type == 'collection' or s_type == 'collection_set' or s_type == 'collection&set':
            folder_code = 'DMAM.Classes.CollectionDirectory'
        n = 0
        for p in path_list:
            t_xpath = "//TreeItem[contains(@Name, '%s')]" % folder_code * (n + 2)
            s_xpath = t_xpath + "//Text[contains(@Name, '%s')]" % p
            xpath_list.append(s_xpath)
            n = n+1
        print(xpath_list)
        # 返回xpath列表的长度
        l = len(xpath_list)
        i = l-1
        # 从最后的一个文件夹开始找，如果没找到，继续找上一级的文件夹
        while i >= 0:
            is_found = self.driver.find_elements_by_xpath(xpath_list[i])
            print(i)
            print(xpath_list[i])
            print(is_found)
            if not is_found:
                i = i-1
                print(i)
            else:
                print('找到了')
                for n in range(i, l):
                    MainPage.t = self.find(By.XPATH, xpath_list[n])
                    ActionChains(self.driver).double_click(MainPage.t).perform()
                break
        # folder_id目前是为了delete功能
        return item_id

    def select_folder(self, s_path='random'):
        folder_id = self.select_item('library', s_path)
        return folder_id

    def select_from_Collections(self):
        collection_id = self.select_item('collection&set')
        return collection_id

    def select_collection(self):
        collection_id = self.select_item('collection')
        return collection_id

    def select_collection_set(self):
        collection_set_id = self.select_item('collection_set')
        return collection_set_id

    def select_file(self, s_type, n='all', s_path='random'):
        f_xpath = ''
        item_id = ''
        if s_type == 'library_file':
            item_id = self.select_folder(s_path)
            f_xpath = "//ListItem[contains(@Name, 'DMAM.Classes.DataFile')]"
            while True:
                if not self.driver.find_elements_by_xpath(f_xpath):
                    item_id = self.select_folder(s_path)
                else:
                    break
        elif s_type == 'collection_file':
            item_id = self.select_from_Collections()
            f_xpath = "//ListItem[contains(@Name, 'DMAM.Classes.CollectionFile')]"
            while True:
                if not self.driver.find_elements_by_xpath(f_xpath):
                    item_id = self.select_from_Collections()
                else:
                    break
        if n == 'all':
            self.find(By.XPATH, "//Button[contains(@AutomationId, 'PageheaderButton')]").click()
        elif n == 'random':
            # click first file
            self.find(By.XPATH, f_xpath).click()
            # move down random times, <10
            i = 0
            j = 0
            while i < random.randint(1, 10):
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ARROW_DOWN).key_up(Keys.SHIFT).perform()
                i += 1
            while j < random.randint(1, 10):
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ARROW_RIGHT).key_up(Keys.SHIFT).perform()
                j += 1
        elif n == '1':
            # click first file
            self.find(By.XPATH, f_xpath).click()
            # move down random times, <10
            i = 0
            j = 0
            while i < random.randint(1, 10):
                ActionChains(self.driver).key_down(Keys.ARROW_DOWN).perform()
                i += 1
            while j < random.randint(1, 10):
                ActionChains(self.driver).key_down(Keys.ARROW_RIGHT).perform()
                j += 1
        MainPage.t = self.find(By.XPATH, "//ListItem[contains(@ClassName, 'ListBoxItem')]")
        return item_id

    def select_folder_file(self, n='1', s_path='random'):
        folder_id = self.select_file('library_file', n, s_path)
        return folder_id

    def select_random_collection_file(self):
        collection_id = self.select_file('collection_file', 'random')
        return collection_id

    def select_all_collection_file(self):
        collection_id = self.select_file('collection_file', 'all')
        return collection_id

    def click_page_head(self):
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'PageheaderButton')]").click()
        return self

    def select_all(self):
        ActionChains(self.driver).key_down(Keys.CONTROL).key_down('a').key_up(Keys.CONTROL).perform()

    def right_click(self):
        ActionChains(self.driver).context_click(MainPage.t).perform()

    def top_menu(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//Button[contains(@AutomationId, 'CollectionButton')]")))
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'CollectionButton')]").click()

    def folder_menu(self):
        ActionChains(self.driver).key_down(Keys.TAB).key_down(Keys.ENTER).perform()

    # select some files, then tab to file menu
    def file_menu(self):
        ActionChains(self.driver).key_down(Keys.TAB).key_down(Keys.TAB).key_down(Keys.TAB).key_down(Keys.ENTER).perform()

    def add_root_folder(self, folder_path):
        library_all = self.find(By.XPATH, "//TreeItem[contains(@Name, 'DMAM.Classes.DataDirectory')]"
                                          "//Text[contains(@Name, 'All')]")
        ActionChains(self.driver).context_click(library_all).perform()
        self.find(By.NAME, 'Add root folder').click()
        self.find(By.XPATH, "//Window[contains(@Name, 'Select Folder')]//Edit[contains(@Name, 'Folder:')]").send_keys(folder_path)
        self.find(By.XPATH, "//Window[contains(@Name, 'Select Folder')]//Button[contains(@Name, 'Select Folder')]").click()

    def add_to_target_collection(self):
        self.find(By.NAME, 'Add to target collection').click()

    def add_to_target_collection_by_crosshair(self):
        ActionChains(self.driver).key_down(Keys.TAB).key_down(Keys.ENTER).perform()

    def set_target_collection(self):
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'CollectionCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()

    def close_set_target_collection_dialog(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'SetTargetDialog')]"
                            "//Button[contains(@AutomationId, 'cancelbutton')]").click()

    def open_create_folder_dailog(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Create sub folder inside')]").click()

    def confirm_create_folder(self, s='default'):
        if s == 'default':
            s = time.strftime('subfolder_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'CreateImportFolderDialog')]"
                            "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(s)
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'CreateImportFolderDialog')]"
                            "//Button[contains(@AutomationId, 'okbutton')]").click()
        # find two elements, select second element, get the error message
        error_message = self.driver.find_elements_by_xpath(
                "//Custom[contains(@AutomationId, 'CreateImportFolderDialog')]//Text[contains(@ClassName, 'TextBlock')]")[1].text
        return error_message

    def close_create_folder_dialog(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'CreateImportFolderDialog')]"
                            "//Button[contains(@AutomationId, 'cancelbutton')]").click()

    def open_rename_dialog(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Rename')]").click()

    def open_rename_collection_set_dialog(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Rename collection set')]").click()

    def confirm_rename(self, s='default'):
        if s == 'default':
            s = time.strftime('rename_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'RenameDialog')]"
                            "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(s)
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'RenameDialog')]"
                            "//Button[contains(@AutomationId, 'okbutton')]").click()
        error_message = self.driver.find_elements_by_xpath(
            "//Custom[contains(@AutomationId, 'RenameDialog')]//Text[contains(@AutomationId, 'errortext')]")[
            0].text
        return error_message

    def close_rename_dialog(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'RenameDialog')]"
                            "//Button[contains(@AutomationId, 'cancelbutton')]").click()

    def open_delete_dialog(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Delete')]").click()

    def check_on_delete_from_pc(self):
        self.find(By.XPATH, "//CheckBox[contains(@AutomationId, 'DeleteHD')]").click()

    def confirm_delete_folder(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'DeleteFolderDialog')]"
                            "//Button[contains(@AutomationId, 'okbutton')]").click()
        # todo: 加显式等待

    def close_delete_folder_dialog(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'DeleteFolderDialog')]"
                            "//Button[contains(@AutomationId, 'cancelbutton')]").click()

    def confirm_delete_files(self):
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'DeleteDialog')]"
                            "//Button[contains(@AutomationId, 'okbutton')]").click()

    def open_create_collection_dialog(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Create collection')]").click()

    def set_as_target_when_create_collection(self):
        self.find(By.XPATH, "//CheckBox[contains(@AutomationId, 'TargetCollection')]").click()

    # create collection and set as target collection
    def confirm_create_collection(self, s='default'):
        if s == 'default':
            s = time.strftime('collection_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(s)
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        return s

    def create_collection_for_files(self):
        s = time.strftime('collection_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(s)
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        return s

    def create_collection_error(self):
        error_message = self.driver.find_elements_by_xpath(
            "//Custom[contains(@AutomationId, 'CreateCollectionDialog')]//Text[contains(@ClassName, 'TextBlock')]")[
            2].text
        return error_message

    def close_create_collection_dialog(self):
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'cancelbutton')]").click()

    def open_create_collection_set(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Create collection set')]").click()

    def confirm_create_collection_set(self, s='default'):
        if s == 'default':
            s = time.strftime('collection_set_%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(s)
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        return s

    def create_collection_set_error(self):
        error_message = self.driver.find_elements_by_xpath(
            "//Custom[contains(@AutomationId, 'CreateCollectionSetDialog')]//Text[contains(@ClassName, 'TextBlock')]")[
            1].text
        return error_message

    def close_create_collection_set_dialog(self):
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'cancelbutton')]").click()

    def set_as_target_collection(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Set as target collection')]").click()

    def move_collection(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Move collection')]").click()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        # 因为往下移了2位，在数据库里找到第二个collection set，就是目标set
        target_id = vm.db_random('collection_set', '2')[-1]
        return target_id

    def move_collection_set(self, moved):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Move collection set')]").click()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        target_set_id = vm.db_selected_set_when_move_collection_set(moved)
        return target_set_id

    def remove(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Remove')]").click()
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()

    def remove_collection_set(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Remove collection set')]").click()
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()

    def add_to_collection(self):
        self.find(By.XPATH, "//MenuItem[@Name='Add to collection']").click()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'CollectionCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        selected_collection_id = vm.db_selected_collection()
        return selected_collection_id

    def move_collection_file(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Move to collection')]").click()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'SetCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'CollectionCombobox')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        selected_collection_id = vm.db_selected_collection()
        return selected_collection_id

    def move_folder_file(self):
        self.find(By.XPATH, "//MenuItem[contains(@Name, 'Move to folder')]").click()
        self.find(By.XPATH, "//ComboBox[contains(@AutomationId, 'folderlist')]").click()
        ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_down(Keys.ENTER).perform()
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        selected_folder_id = vm.db_selected_folder()
        return selected_folder_id

    def change_view(self, view='all'):
        all_views = ['ViewbyList', 'ViewbyTrack', 'ViewbySmall', 'ViewbyMedium', 'ViewbyLarge']
        if view == 'random':
            random.shuffle(all_views)
            v = [all_views.pop()]
            all_views = v
        for viewby in all_views:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'deta')]"
                                "//Button[contains(@AutomationId, 'ViewbyButton')]").click()
            self.driver.find_element_by_accessibility_id(viewby).click()

    def change_group(self, group='all'):
        all_groups = []
        if group == 'random':
            random.shuffle(all_groups)
            g = [all_groups.pop()]
            all_groups = g
        elif group == 'all':
            all_groups = ['GroupbyNone', 'GroupbyDate', 'GroupbyFolder', 'GroupbyType']
        else:
            all_groups.append(group)
        for groupby in all_groups:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'deta')]"
                                "//Button[contains(@AutomationId, 'GroupbyButton')]").click()
            self.driver.find_element_by_accessibility_id(groupby).click()

    def change_sort(self, sort='all'):
        all_sorts = ['SortbyName', 'SortbyDate', 'SortbyFolder', 'SortbyType', 'SortbySize']
        if sort == 'random':
            random.shuffle(all_sorts)
            s = [all_sorts.pop()]
            all_sorts = s
        for sortby in all_sorts:
            self.find(By.XPATH, "//Custom[contains(@AutomationId, 'deta')]"
                                "//Button[contains(@AutomationId, 'SortbyButton')]").click()
            self.driver.find_element_by_accessibility_id(sortby).click()

    def open_details(self):
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'Detailsbutton')]").click()

    def add_assigned_keywords(self):
        self.find(By.XPATH, "//Custom[contains(@ClassName, 'ImageDetailUserControl')]"
                            "/Pane/Button[contains(@ClassName, 'Button')]").click()
        n = time.strftime('keyword%Y%m%d%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(n)
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        return n

    def click_assigned_keywords(self, k):
        self.find(By.XPATH, "//Button[contains(@Name, '%s')]" % k).click()

    def add_suggested_keywords(self):
        elements = self.driver.find_elements_by_xpath(
            "//Custom[contains(@ClassName, 'ImageDetailUserControl')]/Pane/Button[contains(@ClassName, 'Button')]")
        print(elements)
        elements[1].click()
        n = time.strftime('keyword%Y%m%d%H%M%S', time.localtime(time.time()))
        self.find(By.XPATH, "//Edit[contains(@AutomationId, 'EnterName')]").send_keys(n)
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'okbutton')]").click()
        return n

    # 可以截图对比，有没有打开filter。如果打开，点击keyword来过滤文件，但是有没有过滤出来并不知道
    def filter(self):
        self.find(By.XPATH, "//Button[contains(@AutomationId, 'Filterbutton')]").click()
        self.find(By.XPATH, "//ListItem[contains(@Name, 'DMAM.Classes.FilterFile')]").click()

    def open_preview(self):
        ActionChains(self.driver).key_down(Keys.ENTER).perform()

    def close_preview(self):
        ActionChains(self.driver).key_down(Keys.ESCAPE).perform()

    # zoom in/zoom out
    def preview_zoom(self):
        current_def = sys._getframe().f_code.co_name
        time.sleep(3)
        screenshot1 = vm.get_screenshot(current_def)
        ActionChains(self.driver).key_down(Keys.ADD).perform()
        time.sleep(3)
        screenshot2 = vm.get_screenshot(current_def)
        ActionChains(self.driver).key_down(Keys.SUBTRACT).perform()
        time.sleep(3)
        screenshot3 = vm.get_screenshot(current_def)
        result_in = cs.compare_image(screenshot1, screenshot2)
        result_out = cs.compare_image(screenshot1, screenshot3)
        if result_out > result_in:
            return True
        else:
            return False

    # rotate left/rotate right
    def preview_rotate(self):
        current_def = sys._getframe().f_code.co_name
        time.sleep(3)
        screenshot1 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys('l').perform()
        time.sleep(3)
        screenshot2 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys('r').perform()
        time.sleep(3)
        screenshot3 = vm.get_screenshot(current_def)
        result_l = cs.compare_image(screenshot1, screenshot2)
        result_r = cs.compare_image(screenshot1, screenshot3)
        if result_r > result_l:
            return True
        else:
            return False

    # previous file/next file
    def preview_switch_file(self):
        current_def = sys._getframe().f_code.co_name
        time.sleep(3)
        i = 0
        j = 0
        result_previous = ''
        result_next = ''
        screenshot1 = vm.get_screenshot(current_def)
        while i < random.randint(1, 10):
            # print('i')
            ActionChains(self.driver).send_keys(Keys.PAGE_UP).perform()
            time.sleep(1)
            screenshot2 = vm.get_screenshot(current_def)
            result_previous = cs.compare_image(screenshot1, screenshot2)
            if result_previous > 0.9:
                print(screenshot1)
                print(screenshot2)
                break
            screenshot1 = screenshot2
            i += 1
        while j < random.randint(1, 10):
            # print('j'+ str(j))
            ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)
            screenshot2 = vm.get_screenshot(current_def)
            # if images are same, return True
            result_next = cs.compare_image(screenshot1, screenshot2)
            if result_next > 0.9:
                print(screenshot1)
                print(screenshot2)
                break
            screenshot1 = screenshot2
            j += 1
        if result_previous < 0.9 and result_next < 0.9:
            return True
        else:
            return False

    def preview_fullscreen(self):
        current_def = sys._getframe().f_code.co_name
        time.sleep(3)
        screenshot1 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys(Keys.F11).perform()
        time.sleep(3)
        screenshot2 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys(Keys.F11).perform()
        time.sleep(3)
        screenshot3 = vm.get_screenshot(current_def)
        result_f = cs.compare_image(screenshot1, screenshot2)
        result_r = cs.compare_image(screenshot1, screenshot3)
        if result_f < 0.9 and result_r > 0.9:
            return True
        else:
            return False

    def preview_play_space(self):
        current_def = sys._getframe().f_code.co_name
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.SPACE).send_keys(Keys.SPACE).perform()
        time.sleep(1)
        screenshot1 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys(Keys.SPACE).perform()
        time.sleep(1)
        screenshot2 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys(Keys.SPACE).perform()
        time.sleep(1)
        screenshot3 = vm.get_screenshot(current_def)
        # should be different
        result_play = cs.compare_image(screenshot1, screenshot2)
        # should be same
        result_stop = cs.compare_image(screenshot1, screenshot3)
        if result_stop > result_play:
            return True
        else:
            return False

    def preview_play_enter(self):
        current_def = sys._getframe().f_code.co_name
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.SPACE).send_keys(Keys.SPACE).perform()
        time.sleep(1)
        screenshot1 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        screenshot2 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        screenshot3 = vm.get_screenshot(current_def)
        # should be different
        result_play = cs.compare_image(screenshot1, screenshot2)
        # should be different
        result_pause = cs.compare_image(screenshot1, screenshot3)
        if result_play < 0.99 and result_pause < 0.99:
            return True
        else:
            return False

    def preview_clip(self):
        current_def = sys._getframe().f_code.co_name
        time.sleep(1)
        screenshot1 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys('o').perform()
        time.sleep(1)
        screenshot2 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys('u').perform()
        time.sleep(1)
        screenshot3 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys(Keys.END).perform()
        time.sleep(1)
        screenshot4 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys('i').perform()
        time.sleep(1)
        screenshot5 = vm.get_screenshot(current_def)
        ActionChains(self.driver).send_keys('u').perform()
        time.sleep(1)
        screenshot6 = vm.get_screenshot(current_def)
        result_out = cs.compare_image(screenshot1, screenshot2)
        result_reset1 = cs.compare_image(screenshot1, screenshot3)
        result_in = cs.compare_image(screenshot4, screenshot5)
        result_reset2 = cs.compare_image(screenshot3, screenshot6)
        # pre of different images is less than similar images
        if result_out < result_reset1 and result_in < result_reset2:
            return True
        else:
            return False

    def preview_mute(self):
        current_def = sys._getframe().f_code.co_name
        time.sleep(1)
        screenshot1 = vm.get_screenshot(current_def)
        # mute
        ActionChains(self.driver).send_keys('m').perform()
        time.sleep(1)
        screenshot2 = vm.get_screenshot(current_def)
        # unmute
        ActionChains(self.driver).send_keys('m').perform()
        time.sleep(1)
        screenshot3 = vm.get_screenshot(current_def)
        result_mute = cs.compare_image(screenshot1, screenshot2)
        result_unmute = cs.compare_image(screenshot1, screenshot3)
        if result_mute < result_unmute:
            return True
        else:
            return False

    # as VEGAS Prepare crash when select folder only with video or audio,
    # so cannot right click the first file which is video or audio
    def preview_generate_thumbnail(self):
        current_def = sys._getframe().f_code.co_name
        time.sleep(3)
        screenshot1 = vm.get_screenshot(current_def)
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'PreviewPlayer')]"
                            "//Button[contains(@AutomationId, 'MoreButton')]").click()
        self.driver.find_element_by_name('Generate thumbnails').click()
        time.sleep(5)
        screenshot2 = vm.get_screenshot(current_def)
        result_thumbnail = cs.compare_image(screenshot1, screenshot2)
        if result_thumbnail < 0.95:
            return True
        else:
            return False

    def preview_generate_waveforms(self):
        current_def = sys._getframe().f_code.co_name
        time.sleep(3)
        screenshot1 = vm.get_screenshot(current_def)
        self.find(By.XPATH, "//Custom[contains(@AutomationId, 'PreviewPlayer')]"
                            "//Button[contains(@AutomationId, 'MoreButton')]").click()
        self.driver.find_element_by_name('Generate waveforms').click()
        time.sleep(5)
        screenshot2 = vm.get_screenshot(current_def)
        result_thumbnail = cs.compare_image(screenshot1, screenshot2)
        if result_thumbnail < 0.95:
            return True
        else:
            return False
