from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import base64
from dotenv import load_dotenv
import time
import datetime
import asyncio


async def take_screenshot():
    # fetch login credentials
    load_dotenv(".env")
    PA_STUDENT_ID = os.environ["PA_STUDENT_ID"]
    PA_USERNAME = os.environ["PA_USERNAME"]

    # initiate webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # hit the login page url and wait until it loads
    driver.get("https://pixel-art.netsoc.com/users/login")

    # get references to the form elements
    login_form = driver.find_element(by=By.TAG_NAME, value="form")
    student_id_input = driver.find_element(by=By.NAME, value="student_id")
    username_input = driver.find_element(by=By.NAME, value="username")

    # fill out form fields and submit form
    student_id_input.send_keys(PA_STUDENT_ID)
    username_input.send_keys(PA_USERNAME)
    login_form.submit()

    # wait at most 5 seconds for the url to change i.e. to be successfully logged
    # in
    WebDriverWait(driver, 5).until(EC.url_to_be("https://pixel-art.netsoc.com/users/"))

    # go the webpage with the canvas
    driver.get("https://pixel-art.netsoc.com/players")

    # wait a couple seconds for the JavaScript to render the canvas
    await asyncio.sleep(5)

    # fetch the canvas and use some native JavaScript to convert it to a base64
    # encoded PNG image
    canvas = driver.find_element(by=By.TAG_NAME, value="canvas")
    canvas_base64 = driver.execute_script(
        "return arguments[0].toDataURL('image/png').substring(21);", canvas
    )

    # decode the base64 string and write it to a timestamped file
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%Y_%m_%d-%H%M%S")

    with open(f"screenshots/{timestamp}.png", "wb") as image_output:
        image_output.write(base64.b64decode(canvas_base64))

    # exit the driver
    driver.quit()

    return f"screenshots/{timestamp}.png"
