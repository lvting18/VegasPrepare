# -*- coding: utf-8 -*-
# coding : utf-8

import time
import pytest
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from page.App import App
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import custom_method.vpmethod as vm
import allure


class TestImport(object):
    driver = WebDriver
    vm.ini_vp()
    _ini_target = vm.read_yml('import_target')
    _test_view_group_sort = vm.load_param('TestImport', 'test_view_group_sort')
    _test_source_mtp = vm.load_param('TestImport', 'test_source_mtp')
    _test_source_removable_disk = vm.load_param('TestImport', 'test_source_removable_disk')
    _test_source_network_drive = vm.load_param('TestImport', 'test_source_network_drive')
    _test_source_empty_folder = vm.load_param('TestImport', 'test_source_empty_folder')
    _test_source_multifile = vm.load_param('TestImport', 'test_source_multifile')
    _test_source_wholefolder = vm.load_param('TestImport', 'test_source_wholefolder')
    _test_source_large = vm.load_param('TestImport', 'test_source_large')
    _test_import_to_existing_target = vm.load_param('TestImport', 'test_import_to_existing_target')

    @classmethod
    def setup_class(cls):
        cls.mainPage = App.main()
        cls.mainPage.driver.maximize_window()

    def setup_method(self):
        self.ImportPage = self.mainPage.gotoImport()
        self.ImportPage.iniImport()

    def teardown_method(self):
        self.ImportPage.backtomain()

    def teardown_class(self):
        self.mainPage.driver.quit()

    @allure.description('test all view/group/sort')
    @pytest.mark.parametrize(("s",), _test_view_group_sort)
    def test_view_group_sort(self, s):
        self.ImportPage.SelectSourceFolder(s)
        self.ImportPage.ChangeView()
        self.ImportPage.ChangeGroup()
        self.ImportPage.ChangeSort()

    @allure.description('import mtp device to new target folder')
    @pytest.mark.skip(reason='no mtp device')
    @pytest.mark.parametrize(("s",), _test_source_mtp)
    def test_source_mtp(self, s):
        self.ImportPage.SelectMTP(s)
        t = self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        assert self.ImportPage.IsImporting() is True
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.compare_files(s, t)

    @pytest.mark.skip(reason='no removable disk')
    @pytest.mark.parametrize(("s",), _test_source_removable_disk)
    def test_source_removable_disk(self, s):
        self.ImportPage.SelectSourceFolder(s)
        t = self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        assert self.ImportPage.IsImporting() is True
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.compare_files(s, t)

    @pytest.mark.skip(reason='no network drive')
    @pytest.mark.parametrize(("s",), _test_source_network_drive)
    def test_source_network_drive(self, s):
        self.ImportPage.SelectSourceFolder(s)
        t = self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        assert self.ImportPage.IsImporting() is True
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.compare_files(s, t)

    @allure.description('import empty folder to new target folder, import button is disabled')
    @pytest.mark.parametrize(("s",), _test_source_empty_folder)
    def test_source_empty_folder(self, s):
        self.ImportPage.SelectSourceFolder(s)
        self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        assert self.ImportPage.IsImporting() is False

    @pytest.mark.parametrize(("s",), _test_source_multifile)
    def test_source_multifile(self, s):
        self.ImportPage.SelectFile(s)
        t = self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        assert self.ImportPage.IsImporting() is True
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.compare_files(s, t) is False

    @allure.description('import several files to new target folder')
    @pytest.mark.parametrize(("s", "t"), _test_source_wholefolder)
    def test_source_wholefolder(self, s, t):
        self.ImportPage.SelectSourceFolder(s)
        t = self.ImportPage.NewTargetFolder(self._ini_target, target_name=t)
        self.ImportPage.ClickImport()
        assert self.ImportPage.IsImporting() is True
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.compare_files(s, t)

    @pytest.mark.parametrize(("s",), _test_source_large)
    def test_source_large(self, s):
        self.ImportPage.SelectSourceFolder(s)
        t = self.ImportPage.NewTargetFolder(self._ini_target)
        self.ImportPage.ClickImport()
        assert self.ImportPage.IsImporting() is True
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.compare_files(s, t)

    @allure.description('import to existing target')
    @pytest.mark.parametrize(("s", "t"), _test_import_to_existing_target)
    def test_import_to_existing_target(self, s, t):
        self.ImportPage.SelectSourceFolder(s)
        self.ImportPage.SelectTargetFolder(t)
        self.ImportPage.ClickImport()
        self.ImportPage.WaitingImportFinish()
        self.ImportPage.CloseImportDialog()
        assert vm.compare_files(s, t)


