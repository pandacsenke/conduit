from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

class TestConduit(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)

        # For GitHub Actions
        options.add_argument('--headless')
        # optional
        options.add_argument('--no-sandbox')
        # optional
        options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "http://localhost:1667"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
       # self.browser.quit()
         pass

    def test_registration(self):
        signUp_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'a[href="#/register"]')))
        signUp_btn.click()

        username_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
        username_input.send_keys("pandacsenke")

        email_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        email_input.send_keys("testpanda5@gmail.com")

        password_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        password_input.send_keys("Panda.test123")

        sign_up_green_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))
        sign_up_green_btn.click()

        welcome = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-title"]')))

        assert welcome.text == "Welcome!"

        ok_button = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="swal-button swal-button--confirm"]')))
        ok_button.click()

    # def test_login(self):
    #     pass
    #
    # def test_cookies(self):
    #     pass
    #
    # def test_DataList(self):
    #     pass
    #
    # def test_AllPages(self):
    #     pass
    #
    # def test_NewDataInput(self):
    #     pass
    #
    # def test_RepeatedDataInput(self):
    #     pass
    #
    # def test_DataModification(self):
    #     pass
    #
    # def test_DataDelete(self):
    #     pass
    #
    # def test_DataSave(self):
    #     pass
    #
    # def test_logout(self):
    #     pass
