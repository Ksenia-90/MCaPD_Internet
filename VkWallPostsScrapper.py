import time
import unicodedata

from bs4 import BeautifulSoup
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from PostsRepository import PostsRepository


class VkWallPostsScrapper:
    def __init__(self):
        self._base_url = 'https://vk.com/'
        config = dotenv_values('.env')
        self._driver_path = config.get('driver_path')

    def upload_posts(self, group_name, search_string):
        html = self._get_body(group_name, search_string)
        posts = self._parse_html(html)
        with PostsRepository() as posts_repository:
            return posts_repository.insert_post(posts)

    def _get_body(self, group_name, search_string):
        body = ''
        limit_scroll = 10
        limit_wait = 10
        url = self._base_url + group_name
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(self._driver_path, options=options)

        try:
            driver.get(url)
            button = driver.find_element_by_class_name('ui_tab_search')
            button.click()
            input_search = driver.find_element_by_id('wall_search')
            input_search.send_keys(search_string)
            input_search.send_keys(Keys.ENTER)
            elements = driver.find_elements_by_class_name('ui_search_loading')
            loop_count = 0
            loop_run = True
            while loop_run:
                elements = driver.find_elements_by_class_name('ui_search_loading')
                if len(elements) == 0:
                    loop_run = False
                time.sleep(1)
                loop_count = loop_count + 1
                if loop_count > limit_wait:
                    raise Exception('Wait timeout expired')

            actions = ActionChains(driver)
            actions.send_keys(Keys.TAB)
            actions.perform()

            body = driver.page_source
            for x in range(limit_scroll):
                actions.send_keys(Keys.END)
                actions.perform()
                loop_count = 0
                loop_run = True
                while loop_run:
                    element = driver.find_element_by_id('wall_more_link')
                    style = element.get_attribute('style')
                    if style == 'display: none;' or len(element.text) > 0:
                        loop_run = False
                    time.sleep(1)
                    loop_count = loop_count + 1
                    if loop_count > limit_wait:
                        raise Exception('wait scroll end timeout')
                # check register window
                if len(driver.find_elements_by_class_name('JoinForm__notNow')) > 0:
                    actions.send_keys(Keys.ESCAPE)
                    actions.perform()
            body = driver.page_source
        except Exception as e:
            print(e)
        finally:
            driver.quit()

        return body

    def _parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        posts_items = soup.find_all('div', {'class': '_post_content'})
        posts = []
        for post_item in posts_items:
            # text
            post = {}
            text_div = post_item.find('div', {'class': 'wall_post_text'})
            if text_div is not None:
                # text
                post['text'] = text_div.text

                # likes
                like_div = post_item.find_all('div', {'class': 'like_button_count'})
                post['like_count'] = like_div[0].text
                post['shared_count'] = like_div[1].text

                # view
                like_view = post_item.find('div', {'class': ['like_views', '_views']})
                post['view_count'] = like_view.text

                # link
                link = post_item.find('a', {'class': 'post_link'}, href=True)
                post['link'] = self._base_url + link['href']

                # date
                date = post_item.find('span', {'class': 'rel_date'})
                post['date'] = unicodedata.normalize('NFKD', date.text)
                posts.append(post)
        return posts


if __name__ == '__main__':
    search_string  = input("Введите строку поиска: ")
    ss = VkWallPostsScrapper()
    text = ss.upload_posts('tokyofashion', search_string)
