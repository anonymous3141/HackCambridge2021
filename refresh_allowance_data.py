import threading
import os
from time import sleep
from selenium import webdriver
import pandas
import numpy as np

DOWNLOADED_FILES_DESTINATION = os.getcwd()
ALLOWANCE_DATA_PATH = DOWNLOADED_FILES_DESTINATION + "/EMBER_Coal2Clean_EUETSPrices.csv"

allowance_data_past_week = None

DATA_UPDATE_INTERVAL = 60 * 60 # Seconds

HEADLESS = True

def generate_chrome_settings(headless):
    option = webdriver.ChromeOptions()
    prefs = {"download.default_directory": DOWNLOADED_FILES_DESTINATION}
    option.add_experimental_option("prefs", prefs)

    if headless:
        option.add_argument('--headless')

    return option


def download_file():
    print("Downloading allowance data...")
    driver = webdriver.Chrome(options=generate_chrome_settings(HEADLESS))
    url = "https://QU6FEUWMSKTSIJSJ.anvil.app/FUIY7TKGIS7A33N4XOCB7YM2"
    driver.get(url)

    eu_button = None

    while eu_button is None:
        results = driver.find_elements('class name', 'button-text')
        if len(results) > 0:
            eu_button = results[0]
            break

    eu_button.click()
    sleep(5)
    driver.close()
    print("Download successful!")

def update_allowance_data():
    print("Loading allowance data...")
    global allowance_data_past_week
    svg_data = np.array(pandas.read_csv(ALLOWANCE_DATA_PATH))
    new_allowance_data_past_week = [price for _, price in svg_data[-7:]]
    allowance_data_past_week = new_allowance_data_past_week
    print("Load successful!")

def update_allowance_data_regularly():
    while True:
        sleep(DATA_UPDATE_INTERVAL)
        update_allowance_data()  # TODO: Fix a mutex.


def start_allwance_data_updater():
    threading.Thread(target=update_allowance_data_regularly)

if __name__ == "__main__":
    download_file()
    update_allowance_data()
