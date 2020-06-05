import time
from appium.webdriver.webdriver import WebDriver
from page.App import App
import pytest
import custom_method.vpmethod as vm
import allure
from selenium.webdriver.support import expected_conditions as EC


class TestPreview(object):
    driver = WebDriver

    # @classmethod
    # def setup_class(cls):
    #     cls.mainPage = App.main()
    #     # cls.mainPage.driver.maximize_window()

    def setup_method(self):
        self.mainPage = App.main()

    def teardown_method(self):
        self.mainPage.driver.quit()

    @allure.feature("preview")
    def test_preview_close(self):
        self.mainPage.select_folder_file()
        # time.sleep(2)
        self.mainPage.open_preview()
        assert self.mainPage.IsPreviewOpen()
        self.mainPage.close_preview()
        assert self.mainPage.IsPreviewClose()

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['picture', ], ])
    def test_preview_zoom(self, folder_path):
        self.mainPage.select_folder_file(s_path=folder_path)
        self.mainPage.open_preview()
        time.sleep(3)
        zoom_result = self.mainPage.preview_zoom()
        assert zoom_result

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['picture', ], ])
    def test_preview_rotate(self, folder_path):
        self.mainPage.select_folder_file(s_path=folder_path)
        self.mainPage.open_preview()
        rotate_result = self.mainPage.preview_rotate()
        assert rotate_result

    @allure.feature("preview")
    def test_preview_fullscreen(self):
        self.mainPage.select_folder_file()
        self.mainPage.open_preview()
        fullscreen_result = self.mainPage.preview_fullscreen()
        assert fullscreen_result

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['picture', ], ['video', ], ])
    def test_preview_switch_files(self, folder_path):
        self.mainPage.select_folder_file(s_path=folder_path)
        self.mainPage.open_preview()
        result = self.mainPage.preview_switch_file()
        assert result

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['video', ], ])
    def test_preview_play_video(self, folder_path):
        self.mainPage.select_folder_file(s_path=folder_path)
        self.mainPage.open_preview()
        result_space = self.mainPage.preview_play_space()
        result_enter = self.mainPage.preview_play_enter()
        assert (result_enter and result_space)

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['audio', ], ])
    def test_preview_play_audio(self, folder_path):
        self.mainPage.select_folder_file(s_path=folder_path)
        self.mainPage.open_preview()
        result_space = self.mainPage.preview_play_space()
        result_enter = self.mainPage.preview_play_enter()
        # todo: 不知道怎么assert

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['video', ], ['audio', ], ])
    def test_preview_clip(self, folder_path):
        self.mainPage.select_folder_file(s_path=folder_path)
        self.mainPage.open_preview()
        result_clip = self.mainPage.preview_clip()
        assert result_clip

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['video', ], ['audio', ], ])
    def test_preview_mute(self, folder_path):
        self.mainPage.select_folder_file(s_path=folder_path)
        self.mainPage.open_preview()
        result_mute = self.mainPage.preview_mute()
        assert result_mute

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['video', ], ])
    def test_preview_thumbnail(self, folder_path):
        self.mainPage.select_folder_file(s_path=folder_path)
        self.mainPage.open_preview()
        result = self.mainPage.preview_generate_thumbnail()
        assert result

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['audio', ], ])
    def test_preview_waveforms(self, folder_path):
        self.mainPage.select_folder_file(s_path=folder_path)
        self.mainPage.open_preview()
        result = self.mainPage.preview_generate_waveforms()
        assert result