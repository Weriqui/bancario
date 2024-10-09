import undetected_chromedriver as uc
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(options=options)

driver.get("https://www.listadevedores.pgfn.gov.br/")
cnds = []

try:
    input_cnpj = driver.find_element(By.CSS_SELECTOR, '#identificacaoInput')
    input_cnpj.click()
    input_cnpj.send_keys('20035478000164')
    driver.execute_script('document.querySelector("body > dev-root > dev-consulta > main > dev-filtros > div.filtros > div:nth-child(3) > div > button.btn.btn-warning").click()')
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'body > dev-root > dev-consulta > main > dev-resultados > cdk-virtual-scroll-viewport > div.cdk-virtual-scroll-content-wrapper > div > table > tbody > tr > td:nth-child(5) > a > i')))
    driver.execute_script('document.querySelector("body > dev-root > dev-consulta > main > dev-resultados > cdk-virtual-scroll-viewport > div.cdk-virtual-scroll-content-wrapper > div > table > tbody > tr > td:nth-child(5) > a > i").click()')
    time.sleep(5)
    resultado_innerText = driver.execute_script('document.querySelector("fieldset").innerText')
    print(resultado_innerText)
except TimeoutException:
    nada_encontrado = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > dev-root > dev-consulta > main > dev-resultados > p")))
except Exception as e:
    print(f"Error during scraping: {str(e)}")

driver.quit()


