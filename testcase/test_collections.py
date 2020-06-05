import time

from appium.webdriver.webdriver import WebDriver
from page.App import App
import pytest
import custom_method.vpmethod as vm
import allure


class TestCollections(object):
    driver = WebDriver
    _test_create_collection_set = vm.load_param('TestCollections', 'test_create_collection_set')
    _test_create_collection_set_failed = vm.load_param('TestCollections', 'test_create_collection_set_failed')
    _test_create_collection_failed = vm.load_param('TestCollections', 'test_create_collection_failed')
    _test_rename_collection = vm.load_param('TestCollections', 'test_rename_collection')
    _test_rename_collection_failed = vm.load_param('TestCollections', 'test_rename_collection_failed')
    _test_rename_collection_set_failed = vm.load_param('TestCollections', 'test_rename_collection_set_failed')

    # @classmethod
    # def setup_class(cls):
    #     cls.mainPage = App.main()
    #     # cls.mainPage.driver.maximize_window()

    def setup_method(self):
        self.mainPage = App.main()

    def teardown_method(self):
        self.mainPage.driver.quit()

    @allure.feature('Prepare')
    def test_random_view_group_sort(self):
        self.mainPage.select_folder()
        self.mainPage.change_view('random')
        self.mainPage.change_group('random')
        self.mainPage.change_sort('random')

    @allure.feature("Create collection set")
    @pytest.mark.parametrize(('s',), _test_create_collection_set)
    def test_create_collection_set(self, s):
        selected_id = self.mainPage.select_from_Collections()
        self.mainPage.right_click()
        self.mainPage.open_create_collection_set()
        created_name = self.mainPage.confirm_create_collection_set(s)
        # todo: assert 到数据库中找created_name，能找到，并且在selected_id最近的collection set下

    @allure.feature("Create collection set")
    def test_cancel_create_collection_set(self):
        selected_id = self.mainPage.select_from_Collections()
        self.mainPage.right_click()
        self.mainPage.open_create_collection_set()
        self.mainPage.close_create_collection_set_dialog()
        # todo: assert 数据库完全没变化

    @allure.feature("Create collection set")
    @pytest.mark.parametrize(('s', 'm'), _test_create_collection_set_failed)
    def test_create_collection_set_failed(self, s, m):
        selected_id = self.mainPage.select_from_Collections()
        self.mainPage.right_click()
        self.mainPage.open_create_collection_set()
        self.mainPage.confirm_create_collection_set(s)
        err = self.mainPage.create_collection_set_error()
        self.mainPage.close_create_collection_set_dialog()
        assert (m in err)

    @allure.feature("Create collection")
    def test_create_collection(self):
        selected_id = self.mainPage.select_from_Collections()
        self.mainPage.right_click()
        self.mainPage.open_create_collection_dialog()
        created_name = self.mainPage.confirm_create_collection()
        # todo: assert 到数据库中找created_name，能找到，并且在selected_id最近的collection set下;不是target collection

    @allure.feature("Create collection")
    def test_create_collection_and_set_as_target(self):
        selected_id = self.mainPage.select_from_Collections()
        self.mainPage.right_click()
        self.mainPage.open_create_collection_dialog()
        self.mainPage.set_as_target_when_create_collection()
        created_name = self.mainPage.confirm_create_collection()
        # todo: assert 到数据库中找created_name，能找到，并且在selected_id最近的collection set下;是target collection

    @allure.feature("Create collection")
    def test_cancel_create_collection(self):
        selected_id = self.mainPage.select_from_Collections()
        self.mainPage.right_click()
        self.mainPage.open_create_collection_dialog()
        self.mainPage.close_create_collection_dialog()
        # todo: assert 数据库完全没变化

    @allure.feature("Create collection")
    @pytest.mark.parametrize(('s', 'm'), _test_create_collection_failed)
    def test_create_collection_failed(self, s, m):
        selected_id = self.mainPage.select_from_Collections()
        self.mainPage.right_click()
        self.mainPage.open_create_collection_dialog()
        self.mainPage.confirm_create_collection(s)
        err = self.mainPage.create_collection_error()
        self.mainPage.close_create_collection_dialog()
        assert (m in err)

    @allure.feature("set as target collection")
    def test_set_as_target_collection(self):
        collection_id = self.mainPage.select_collection()
        self.mainPage.right_click()
        self.mainPage.set_as_target_collection()
        t_id = int(vm.get_target_id())
        assert (collection_id == t_id)

    @allure.feature("move collection/set")
    def test_move_collection(self):
        selected_id = self.mainPage.select_collection()
        self.mainPage.right_click()
        target_id = self.mainPage.move_collection()
        # todo:assert 根据selected_id，找parent id，和target_id一致

    @allure.feature("move collection/set")
    def test_move_collection_set(self):
        selected_id = self.mainPage.select_collection_set()
        self.mainPage.right_click()
        target_id = self.mainPage.move_collection_set(selected_id)
        # todo:assert 根据selected_id，找parent id，和target_id一致

    @allure.feature("rename")
    @pytest.mark.parametrize(('s',), _test_rename_collection)
    def test_rename_collection(self, s):
        selected_id = self.mainPage.select_collection()
        self.mainPage.right_click()
        self.mainPage.open_rename_dialog()
        self.mainPage.confirm_rename(s)
        # todo: 用selected_id在数据库中找到对应的name，和s一致

    @allure.feature("rename")
    @pytest.mark.parametrize(('s', 'm'), _test_rename_collection_failed)
    def test_rename_collection_failed(self, s, m):
        selected_id = self.mainPage.select_collection()
        self.mainPage.right_click()
        self.mainPage.open_rename_dialog()
        get_err = self.mainPage.confirm_rename(s)
        assert (m in get_err)

    @allure.feature("rename")
    def test_rename_collection_set(self):
        selecte_id = self.mainPage.select_collection_set()
        self.mainPage.right_click()
        self.mainPage.open_rename_collection_set_dialog()
        self.mainPage.confirm_rename()
        # todo: rename前，rename后，用selected_id在数据库中找到对应的name，对比，是不同的

    @allure.feature("rename")
    @pytest.mark.parametrize(('s', 'm'), _test_rename_collection_set_failed)
    def test_rename_collection_set_failed(self, s, m):
        self.mainPage.select_collection_set()
        self.mainPage.right_click()
        self.mainPage.open_rename_collection_set_dialog()
        get_err = self.mainPage.confirm_rename(s)
        assert (m in get_err)

    @allure.feature("remove")
    def test_remove_collection(self):
        selected_id = self.mainPage.select_collection()
        self.mainPage.right_click()
        self.mainPage.remove()
        # todo: 数据库中查找selected_id，找不到

    @allure.feature("remove")
    def test_remove_collection_set(self):
        self.mainPage.select_collection_set()
        self.mainPage.right_click()
        self.mainPage.remove_collection_set()
        # todo: 数据库中查找selected_id，找不到

    @allure.feature("export")
    @pytest.mark.skip(reason="not implemented")
    def test_export_collections(self):
        pass
