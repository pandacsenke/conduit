###################################### IMPORTS #########################################################################

import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import csv

############################## BASIC FUNCTIONS #########################################################################
def login(browser):

    signIn_btn = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/login"]')))
    signIn_btn.click()

    email = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
    email.send_keys("testpanda15@gmail.com")

    password = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
    password.send_keys("Panda.test123")

    sign_in_green_btn = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))
    sign_in_green_btn.click()

########################################################################################################################
class TestConduit(object):
    def setup_method(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)

        # For GitHub Actions
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(service=service, options=options)
        URL = "http://localhost:1667"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        # self.browser.quit()
        pass

#################################### TESTS 1 - 11 ######################################################################
    @allure.title('Adatkezelési nyilatkozat használata')
    def test_cookies(self):
        cookies_accept = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))
        cookies_accept.click()

        time.sleep(5)
        cookie_panel = self.browser.find_elements(By.ID, 'cookie-policy-panel')
        assert len(cookie_panel) == 0

    @allure.title('Regisztráció')
    def test_registration(self):
        signUp_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/register"]')))
        signUp_btn.click()

        username_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
        username_input.send_keys("pandacsenke")

        email_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        email_input.send_keys("testpanda15@gmail.com")

        password_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        password_input.send_keys("Panda.test123")

        sign_up_green_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))
        sign_up_green_btn.click()

        welcome = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-title"]')))

        assert welcome.text == "Welcome!"

        ok_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="swal-button swal-button--confirm"]')))
        ok_button.click()

    @allure.title('Bejelentkezés')
    def test_login(self):
        login(self.browser)

        time.sleep(5)
        logout_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[3]

        assert logout_btn.text == " Log out"

    @allure.title('Adatok listázása')
    def test_DataList(self):
        login(self.browser)

        time.sleep(5)

        list = []
        articles = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h1')))[1::]

        for i in articles:
            list.append(i.text)

        assert len(list) != 0

    @allure.title('Több oldalas lista bejárása')
    def test_AllPages(self):
        login(self.browser)

        page_link_buttons = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="page-link"]')))

        num_of_pages = len(page_link_buttons)

        pages_clicked = 0
        for page in page_link_buttons:
            page.click()
            pages_clicked += 1

        assert num_of_pages == pages_clicked

    @allure.title('Új adat bevitel')
    def test_NewDataInput(self):
        login(self.browser)

        new_article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/editor"]')))
        new_article.click()

        # dictionary

        article_input = {
            "article_title": "This is the title of the article",
            "summary": "Here goes the summary",
            "full_article": "This will be the whole article, it is about bla bla bla ... ",
            "tags": "tag1; tag2"
        }

        article_title = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
        article_title.send_keys(article_input["article_title"])

        summary = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
        summary.send_keys(article_input["summary"])

        article = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
        article.send_keys(article_input["full_article"])

        tags = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')))
        tags.send_keys(article_input["tags"])

        publish_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
        publish_btn.click()

        banner = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))

        time.sleep(5)

        assert banner.text == article_input["article_title"]

    @allure.title('Ismételt és sorozatos adatbevitel adatforrásból')
    def test_RepeatedDataInput(self):
        login(self.browser)

        with open('data_input.csv', 'r') as data:
            data_reader = csv.reader(data, delimiter=',')
            next(data_reader)  # beolvasasbol az elso sort kihagyja

            for i in data_reader:
                new_article = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/editor"]')))
                new_article.click()
                article_title = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
                summary = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
                article = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
                tags = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')))
                publish_btn = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

                article_title.send_keys(i[0])
                summary.send_keys(i[1])
                article.send_keys(i[2])
                tags.send_keys(i[3])

                publish_btn.click()

                banner = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))

                time.sleep(5)

                assert banner.text == i[0]

    @allure.title('Meglévő adat módosítás')
    def test_DataModification(self):
        login(self.browser)

        settings = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/settings"]')))
        settings.click()

        image = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="URL of profile picture"]')))
        username = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Your username"]')))
        bio = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder="Short bio about you"]')))

        update_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        image.clear()
        image.send_keys(
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4-IasMjVLx5-PHYvqgMgTjyWYyjuoXeLlpg&usqp=CAU")
        username.clear()
        username.send_keys("housemouse")
        bio.clear()
        bio.send_keys(
            "The house mouse (Mus musculus) is a small mammal of the order Rodentia, characteristically having a pointed snout, large rounded ears, and a long and almost hairless tail. It is one of the most abundant species of the genus Mus.")
        update_btn.click()

        update_success = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-title"]')))

        assert update_success.text == "Update successful!"

    @allure.title('Adat vagy adatok törlése')
    def test_DataDelete(self):
        login(self.browser)

        time.sleep(2)
        read_more_1st_article = self.browser.find_elements(By.CSS_SELECTOR, 'h1')[1]
        read_more_1st_article.click()

        comment = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder="Write a comment..."]')))

        post_comment_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-sm btn-primary"]')))

        comment.send_keys("Ha!... Here goes my comment on this article... Cool.")
        post_comment_btn.click()

        time.sleep(1)
        my_comment = self.browser.find_elements(By.CSS_SELECTOR, 'p[class="card-text"]')[0]

        time.sleep(1)

        assert my_comment.text == "Ha!... Here goes my comment on this article... Cool."

        time.sleep(5)
        all_comments = self.browser.find_elements(By.CSS_SELECTOR, 'p[class="card-text"]')
        num_of_all_comments = len(all_comments)

        time.sleep(1)
        first_delete_icon = self.browser.find_elements(By.CSS_SELECTOR, 'i[class="ion-trash-a"]')[0]
        first_delete_icon.click()

        time.sleep(2)
        all_comments_after_del = self.browser.find_elements(By.CSS_SELECTOR, 'p[class="card-text"]')
        num_of_all_comments_after_del = len(all_comments_after_del)

        time.sleep(2)

        assert num_of_all_comments - 1 == num_of_all_comments_after_del

    # @allure.title('Adatok lementése felületről')
    # def test_SaveDataToFile(self):
    #     login(self.browser)
    #
    #     time.sleep(2)
    #     popular_tags_sidebar = self.browser.find_element(By.CSS_SELECTOR, 'div[class="sidebar"]')
    #     popular_tags = popular_tags_sidebar.find_elements(By.CSS_SELECTOR, 'a[class="tag-pill tag-default"]')
    #
    #     tags_list = []
    #     for i in popular_tags:
    #         tags_list.append(i.text)
    #
    #     with open('pop_tags.csv', 'w', encoding="UTF-8") as file_new:
    #         new = csv.writer(file_new)
    #         new.writerow(tags_list)



    @allure.title('Kijelentkezés')
    def test_logout(self):
        login(self.browser)

        time.sleep(2)
        logout_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))[3]

        logout_btn.click()

        Sign_In_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#/login"]')))

        assert Sign_In_btn.is_displayed()
