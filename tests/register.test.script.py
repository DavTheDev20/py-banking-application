from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
import time
import requests

# *This Test Script may only work on Windows
driver = webdriver.Edge(
    executable_path="C:/Users/Davin's Dell/Development/WebDriver/msedgedriver.exe")

# Grab random user data from randomuser.me
response = requests.get('https://randomuser.me/api')
data = response.json()
login = {
    "username": data["results"][0]["login"]["username"],
    "email": data["results"][0]["email"],
    "password": data["results"][0]["login"]["password"]
}

# Access localhost development site
driver.get("http://127.0.0.1:5000")

register_button = driver.find_element(
    by=By.XPATH, value="/html/body/div[1]/div/a[2]")
time.sleep(3)
register_button.click()

time.sleep(5)

username_field = driver.find_element(By.NAME, value="username")
email_field = driver.find_element(by=By.NAME, value="email")
password_field = driver.find_element(by=By.NAME, value="password")
submit_button = driver.find_element(
    by=By.XPATH, value="/html/body/div[1]/form/input[4]")

username_field.send_keys(login["username"])
time.sleep(2)
email_field.send_keys(login["email"])
time.sleep(2)
password_field.send_keys(login["password"])
time.sleep(2)
submit_button.click()

time.sleep(5)

driver.close()
