import undetected_chromedriver as uc
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_process_info(driver):
    try:
        title = driver.find_element(By.CSS_SELECTOR, '.LawsuitCardPersonPage-header-processInvolved').text.strip()
        process_number = driver.find_element(By.CSS_SELECTOR, '.LawsuitCardPersonPage-header-processNumber').text.strip()
        subject = driver.find_elements(By.CSS_SELECTOR, '.LawsuitCardPersonPage-body-row-item')[1].text.strip()
        tribunal = driver.find_element(By.CSS_SELECTOR, '.LawsuitCardPersonPage-body-row-item-text').text.strip().split(' · ')[0]
        return {'Title': title, 'Processo': process_number, 'Assunto': subject, 'Tribunal': tribunal}
    except Exception as e:
        print(f"Error extracting process info: {str(e)}")
        return None

def scrape_jusbrasil(search_url):
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)

    driver.get(search_url)

    try:

        while True:
            cards = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.LawsuitCardPersonPage')))
            all_process_info = []
            for card in cards:
                process_info = extract_process_info(card)
                if process_info:
                    all_process_info.append(process_info)
            save_to_csv(all_process_info)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        raise  # Re-raise the exception to terminate the script

    finally:
        driver.quit()

def save_to_csv(process_info, filename='processos.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Processo', 'Assunto', 'Tribunal']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if process_info:
            for info in process_info:
                writer.writerow(info)


search_url = "https://www.jusbrasil.com.br/processos/nome/3241840/banco-santander-brasil-sa"
process_info = scrape_jusbrasil(search_url)
