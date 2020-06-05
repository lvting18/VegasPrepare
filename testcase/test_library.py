from appium.webdriver.webdriver import WebDriver
from page.App import App
import pytest
import allure
import custom_method.vpmethod as vm


class TestLibrary(object):
    driver = WebDriver
    _test_add_root_folder = vm.load_param('TestLibrary', 'test_add_root_folder')
    _test_create_folder_multi_lan = vm.load_param('TestLibrary', 'test_create_folder_multi_lan')
    _test_create_folder_failed = vm.load_param('TestLibrary', 'test_create_folder_failed')
    _test_rename_failed = vm.load_param('TestLibrary', 'test_rename_failed')

    @classmethod
    def setup_class(cls):
        cls.mainPage = App.main()
        # cls.mainPage.driver.maximize_window()

    @allure.feature('Prepare')
    def test_random_view_group_sort(self):
        self.mainPage.select_folder()
        self.mainPage.change_view('random')
        self.mainPage.change_group('random')
        self.mainPage.change_sort('random')

    @allure.feature("add root folder")
    @pytest.mark.parametrize(('r_path', ), _test_add_root_folder)
    def test_add_root_folder(self, r_path):
        self.mainPage.add_root_folder(r_path)

    @allure.feature("add to target collection")
    def test_cancel_add_to_target_collection(self):
        self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.add_to_target_collection()
        self.mainPage.close_set_target_collection_dialog()

    @allure.feature("add to target collection")
    def test_set_and_add_to_target_collection(self):
        self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.add_to_target_collection()
        self.mainPage.set_target_collection()

    @allure.feature("add to target collection")
    # todo: 这里可以加数据驱动，add different kinds of files to target collection, empty folder...
    def test_add_folder_to_existing_target_collection(self):
        self.mainPage.select_folder()
        self.mainPage.folder_menu()
        self.mainPage.add_to_target_collection()

    @allure.feature("create folder")
    def test_create_folder_successfully(self):
        self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.open_create_folder_dailog()
        self.mainPage.confirm_create_folder()

    @allure.feature("create folder")
    @allure.description('Chinese, Arabic, Czech, Japanese, Korean')
    @pytest.mark.parametrize(('s',), _test_create_folder_multi_lan)
    def test_create_folder_multi_lan(self, s):
        self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.open_create_folder_dailog()
        self.mainPage.confirm_create_folder(s)

    @allure.feature("create folder")
    @pytest.mark.parametrize(('s', 'm'), _test_create_folder_failed)
    def test_create_folder_failed(self, s, m):
        self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.open_create_folder_dailog()
        get_m = self.mainPage.confirm_create_folder(s)
        self.mainPage.close_create_folder_dialog()
        assert (m in get_m)

    @allure.feature("create folder")
    def test_cancel_create_folder(self):
        self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.open_create_folder_dailog()
        self.mainPage.close_create_folder_dialog()

    @allure.feature("rename folder")
    def test_rename(self):
        self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.open_rename_dialog()
        self.mainPage.confirm_rename()

    @allure.feature("rename folder")
    @pytest.mark.parametrize(('s', 'm'), _test_rename_failed)
    def test_rename_failed(self, s, m):
        self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.open_rename_dialog()
        get_m = self.mainPage.confirm_rename(s)
        self.mainPage.close_rename_dialog()
        assert (m in get_m)

    @allure.feature("rename folder")
    def test_cancel_rename(self):
        self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.open_rename_dialog()
        self.mainPage.close_rename_dialog()

    @allure.feature("delete folder")
    def test_delete_folder_from_database(self):
        folder_id = self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.open_delete_folder_dialog()
        self.mainPage.confirm_delete_folder()
        # todo: check database by folder_id, if related folder and files are removed from database

    @allure.feature("delete folder")
    def test_delete_folder_from_pc(self):
        folder_id = self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.open_delete_folder_dialog()
        self.mainPage.check_on_delete_from_pc()
        self.mainPage.confirm_delete_folder()

    @allure.feature("delete folder")
    def test_cancel_delete_folder(self):
        folder_id = self.mainPage.select_folder()
        self.mainPage.right_click()
        self.mainPage.open_delete_folder_dialog()
        self.mainPage.close_delete_folder_dialog()

    @allure.feature("export")
    @pytest.mark.skip(reason="not implemented")
    def test_export_library(self):
        pass

