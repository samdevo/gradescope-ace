from selenium import webdriver


def submit_assignment(url):
    driver = webdriver.Chrome()

    driver.get(url)

    driver.quit()
