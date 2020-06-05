import time
from appium.webdriver.webdriver import WebDriver
from page.App import App
import pytest
import custom_method.vpmethod as vm
import allure
from selenium.webdriver.support import expected_conditions as EC


class TestImported(object):
    driver = WebDriver

    @classmethod
    def setup_class(cls):
        cls.mainPage = App.main()
        cls.mainPage.change_group('GroupbyNone')

    def setup_method(self):
        self.mainPage = App.main()
        self.mainPage.driver.maximize_window()

    def teardown_method(self):
        time.sleep(2)
        self.mainPage.driver.quit()

    @allure.feature("add to target collection")
    def test_add_all_folder_files_to_target_collection(self):
        folder_id = self.mainPage.select_folder_file('all')
        self.mainPage.right_click()
        self.mainPage.add_to_target_collection()
        if self.mainPage.IsSetTargetDialogOpen():
            self.mainPage.set_target_collection()
        # if not vm.get_target_id():
        #     self.mainPage.set_target_collection()
        # todo: assert folder id下的所有文件都加入到target collection

    @allure.feature("add to target collection")
    def test_add_one_folder_file_to_target_collection(self):
        folder_id = self.mainPage.select_folder_file()
        self.mainPage.add_to_target_collection_by_crosshair()
        # todo: 通过vm的get_target_id方法找到target collection，判断是否增加并且只增加了一个folder id下的文件

    @allure.feature("add to target collection")
    def test_add_all_collection_files_to_target_collection(self):
        collection_id = self.mainPage.select_all_collection_file()
        self.mainPage.top_menu()
        self.mainPage.add_to_target_collection()
        # todo: assert collection id下的所有文件都加入到target collection

    @allure.feature("add to target collection")
    def test_add_random_collection_files_to_target_collection(self):
        collection_id = self.mainPage.select_random_collection_file()
        self.mainPage.file_menu()
        self.mainPage.add_to_target_collection()
        # todo: assert target collection下新增加了一些collection id下的文件

    @allure.feature("add to collection")
    def test_add_all_folder_files_to_collection(self):
        folder_id = self.mainPage.select_folder_file('all')
        self.mainPage.top_menu()
        collection_id = self.mainPage.add_to_collection()
        # todo: assert 查找folder_id下所有的file都加到collection_id下

    @allure.feature("add to collection")
    def test_add_random_collection_files_to_collection(self):
        selected_id = self.mainPage.select_random_collection_file()
        self.mainPage.file_menu()
        target_id = self.mainPage.add_to_collection()
        # todo: assert 查找selected_id下所有的file都加到target_id下

    @allure.feature("move file")
    def test_move_random_collection_file(self):
        selected_id = self.mainPage.select_random_collection_file()
        self.mainPage.top_menu()
        target_id = self.mainPage.move_collection_file()
        # todo: assert 查找selected_id下部分file移到到target_id下，通过move前后的数量对比得出结果

    @allure.feature("move file")
    def test_move_all_collection_files(self):
        selected_id = self.mainPage.select_all_collection_file()
        self.mainPage.right_click()
        target_id = self.mainPage.move_collection_file()
        # todo: assert 查找selected_id下所有file移到到target_id下，move以后selected_id下为空，target_id下数量为原先的数量加上selected_id的数量

    @allure.feature("move file")
    def test_move_folder_file(self):
        folder_id = self.mainPage.select_folder_file('all')
        self.mainPage.right_click()
        target_id = self.mainPage.move_folder_file()
        self.mainPage.WaitProgressDialogClosed()
        # todo: assert 查找selected_id下所有file移到到target_id下，move以后selected_id下为空，target_id下数量为原先的数量加上selected_id的数量。\
        #  查找move前后文件夹中（os）数量相差多少

    @allure.feature("create collection for files")
    def test_create_collection_for_folder_file(self):
        folder_id = self.mainPage.select_folder_file()
        self.mainPage.file_menu()
        self.mainPage.open_create_collection_dialog()
        new_collection = self.mainPage.create_collection_for_files()
        # todo: assert 判断folder_id下是否有一个file加入new_collection

    @allure.feature("create collection for files")
    def test_create_collection_for_collection_file_and_set_target(self):
        collection_id = self.mainPage.select_all_collection_file()
        self.mainPage.top_menu()
        self.mainPage.open_create_collection_dialog()
        self.mainPage.set_as_target_when_create_collection()
        new_collection = self.mainPage.create_collection_for_files()
        # todo: assert 判断collection_id下全部文件是否加入new_collection，并且new_collection是target collection

    @allure.feature("rename")
    def test_rename_folder_file(self):
        folder_id = self.mainPage.select_folder_file()
        self.mainPage.file_menu()
        self.mainPage.open_rename_dialog()
        self.mainPage.confirm_rename()
        # todo: assert 判断folder_id下有一个且只有一个文件的名字被修改，rename前后做对比

    @allure.feature("rename")
    def test_rename_collection_file(self):
        collection_id = self.mainPage.select_random_collection_file()
        self.mainPage.file_menu()
        self.mainPage.open_rename_dialog()
        self.mainPage.confirm_rename()
        # todo: assert 判断collection_id下有一个且只有一个文件的名字被修改，rename前后做对比

    @allure.feature("keywords")
    def test_add_assigned_keywords(self):
        self.mainPage.select_folder_file()
        self.mainPage.open_details()
        new_k = self.mainPage.add_assigned_keywords()
        # todo: assert 新的keywords是否加入数据库，关联到文件上

    @allure.feature("keywords")
    @pytest.mark.xfail(reason="一旦取消选中加了keyword的文件，再次全部选中后，找不到keyword")
    def test_add_part_assigned_keyword_to_all(self):
        # new keyword to one file
        folder_id = self.mainPage.select_folder_file()
        self.mainPage.open_details()
        new_k = self.mainPage.add_assigned_keywords()
        # add the new keyword to all files
        self.mainPage.click_page_head().click_page_head()
        self.mainPage.click_assigned_keywords(new_k)
        # todo: assert new_k 是否关联到folder_id下所有的文件
        # Click the new keyword again to remove it from Assigned keywords
        # self.mainPage.click_assigned_keywords(new_k)
        # todo: assert new_k 是否和folder_id下所有的文件解绑

    @allure.feature("keywords")
    def test_add_suggested_keyword(self):
        self.mainPage.select_folder_file()
        self.mainPage.open_details()
        new_k = self.mainPage.add_suggested_keywords()
        # todo: assert 新的keywords是否加入数据库，没有关联的文件

    @allure.feature("keywords")
    def test_add_suggested_to_assigned(self):
        pass

    @allure.feature("keywords")
    def test_remove_suggested_keyword(self):
        pass

    @allure.feature("keywords")
    def filter(self):
        pass

    @allure.feature("delete/remove file")
    def test_delete_file_from_databse(self):
        folder_id = self.mainPage.select_folder_file()
        self.mainPage.file_menu()
        self.mainPage.open_delete_dialog()
        self.mainPage.confirm_delete_files()
        # todo: assert 判断数据库里folder_id下是否删除一个文件，delete前后对比

    @allure.feature("delete/remove file")
    def test_delete_file_from_pc(self):
        folder_id = self.mainPage.select_folder_file('all')
        self.mainPage.right_click()
        self.mainPage.open_delete_dialog()
        self.mainPage.check_on_delete_from_pc()
        self.mainPage.confirm_delete_files()
        full_path = vm.db_full_path(folder_id)
        self.mainPage.WaitProgressDialogClosed()
        # todo: assert 判断数据库里folder_id下文件全部删除，full path（os）下文件全部删除

    @allure.feature("delete/remove file")
    def test_remove_file(self):
        collection_id = self.mainPage.select_all_collection_file()
        self.mainPage.right_click()
        self.mainPage.remove()
        # todo: assert 判断数据库里collection_id下所有的文件全部remove
