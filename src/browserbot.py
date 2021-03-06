import logging
import sys
import time

import click
import requests
from ansi.colour import fg
from flask import Flask, request
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None


def submit_assignment(url, driver=None):
    if driver is None:
        return

    driver.get(url)

    resubmit_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/section/ul/li[5]/button")
    resubmit_button.click()

    github_button = driver.find_element(By.XPATH, "/html/body/div[1]/dialog/div/div[2]/form/div[1]/div/div/span[2]")
    github_button.click()

    repo_dropdown = driver.find_element(By.XPATH, "/html/body/div[1]/dialog/div/div[2]/form/div[3]/div/div["
                                                  "1]/div/div[1]")
    repo_dropdown.click()
    repo_dropdown.click()

    selection = driver.find_element(By.XPATH, "/html/body/div[1]/dialog/div/div[2]/form/div[3]/div/div[1]/div/div["
                                              "2]/ul/div/div/div[1]/div/li")
    selection.click()

    branch_dropdown = driver.find_element(By.XPATH, "/html/body/div[1]/dialog/div/div[2]/form/div[3]/div/div["
                                                    "2]/div/div[1]")
    branch_dropdown.click()

    master_branch = driver.find_element(By.XPATH, "/html/body/div[1]/dialog/div/div[2]/form/div[3]/div/div["
                                                  "2]/div/div[2]/ul/div/div/div/div/li/div")
    master_branch.click()

    time.sleep(10)


def new_server(driver):
    app = Flask(__name__)
    log = logging.getLogger('werkzeug')
    log.disabled = True

    @app.route('/submit', methods=['GET', 'POST'])
    def result():
        url = request.args.get("url")
        submit_assignment(url, driver)
        res = {"url": url, "success": True}
        return res  # response to your request.

    app.run()


def send_submit(url):
    params = {"url": url}
    try:
        res = requests.get(url="http://localhost:5000/submit", params=params).json()
        if not res["success"]:
            click.echo("Something went wrong. Consider running gradescope-ace init and trying again")
        else:
            click.echo(fg.green("Successfully redirected"))
    except requests.exceptions.ConnectionError:
        click.echo(fg.red("Couldn't find an open gradescope-ace browser. Please run gracescope-ace init"))


def init_session():
    driver = webdriver.Chrome()
    click.echo("Opening a new browser session...")
    driver.get("https://www.gradescope.com/")
    driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/header/nav/div[2]/span[3]/button").click()
    click.echo("Waiting for successful login ???? ...")
    # new_server(driver)  # DELETE THIS LINE
    try:
        WebDriverWait(driver, 100).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'courseBox--shortname'))
        )
        click.echo(fg.brightgreen("Successful login! ????????????"))
        click.echo("Open a new terminal tab and run gracescope-ace submit to submit your work!")
        click.echo(fg.yellow("To quit, press CTRL-C"))
        new_server(driver)
    except TimeoutException:
        click.echo(fg.red("Timeout ... took too long to login"))
    finally:
        driver.quit()
