import undetected_chromedriver as uc
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def consulta_certidao(search_url):
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)

    driver.get(search_url)
    cnds = []
    while True:
        try:
            input_cnpj = driver.find_element(By.CSS_SELECTOR, '#Ni')
            input_cnpj.click()
            input_cnpj.send_keys('00012413000196')
            input_emissao = driver.find_element(By.CSS_SELECTOR, '#frmInfParam > div.linha > div > div:nth-child(2) > div:nth-child(3) > label > label')
            input_emissao.click()
            periodo_inicio = driver.find_element(By.CSS_SELECTOR, "#PeriodoInicio")
            periodo_inicio.click()
            periodo_inicio.send_keys('11042023')
            periodo_fim = driver.find_element(By.CSS_SELECTOR, "#PeriodoFim")
            periodo_fim.click()
            periodo_fim.send_keys('11042024')
            botao_consulta = driver.find_element(By.CSS_SELECTOR, "#validar")
            botao_consulta.click()
            data_emissao = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#resultado > table > tbody > tr:nth-child(1) > td:nth-child(4)')))[0].text.strip()
            if data_emissao:
                ultima_cnd = {}
        except TimeoutException:
            print("TimeoutException: Waiting for elements took too long. Retrying after 10 seconds...")
            time.sleep(10)  # Pause for 10 seconds before retrying
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            break  # Break the loop if there's an unexpected error

    driver.quit()

def save_to_csv(process_info, filename='resultados.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Processo', 'Assunto', 'Tribunal']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if process_info:
            for info in process_info:
                writer.writerow(info)

search_url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/Consultar"
consulta_certidao(search_url)

