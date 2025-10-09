from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
# --- Configurações ---
url = "https://www.dfimoveis.com.br/"
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 15) # espera até 15 segundos
# Abre o combobox de Venda/Aluguel
time.sleep(10)
# --- Abre o dropdown de Tipo de Negócio ---
botao_negocio = wait.until(EC.element_to_be_clickable((By.ID, "select2-negocios-container")))
botao_negocio.click()
print("Dropdown de tipo de negócio aberto.")
# --- Seleciona a opção 'VENDA' ---
nome_opcao = "VENDA"
xpath_opcao = (
f"//li[contains(@class,'select2-results__option') "
f"and normalize-space(text())='{nome_opcao}']"
)
elemento_opcao = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_opcao)))
elemento_opcao.click()
print(f"Opção '{nome_opcao}' selecionada com sucesso!")
time.sleep(5)

# --- Abre o dropdown de Tipo de Imóvel ---
botao_tipo = wait.until(EC.element_to_be_clickable((By.ID, "select2-tipos-container")))
botao_tipo.click()
print("Dropdown de tipo de imóvel aberto.")

# --- Seleciona a opção 'APARTAMENTO' ---
nome_tipo = "APARTAMENTO"
xpath_tipo = (
    f"//li[contains(@class,'select2-results__option') "
    f"and normalize-space(text())='{nome_tipo}']"
)
elemento_tipo = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_tipo)))
elemento_tipo.click()
print(f"Opção '{nome_tipo}' selecionada com sucesso!")

time.sleep(5)

# --- Abre o dropdown de Estado ---
botao_estado = wait.until(EC.element_to_be_clickable((By.ID, "select2-estados-container")))
botao_estado.click()
print("Dropdown de estado aberto.")

# --- Seleciona a opção 'DF' ---
nome_estado = "DF"
xpath_estado = (
    f"//li[contains(@class,'select2-results__option') "
    f"and normalize-space(text())='{nome_estado}']"
)
elemento_estado = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_estado)))
elemento_estado.click()
print(f"Opção '{nome_estado}' selecionada com sucesso!")

time.sleep(5)

# --- Abre o dropdown de Cidade ---
botao_cidade = wait.until(EC.element_to_be_clickable((By.ID, "select2-cidades-container")))
botao_cidade.click()
print("Dropdown de cidade aberto.")

# --- Seleciona a opção 'BRASILIA / PLANO PILOTO' ---
nome_cidade = "BRASILIA / PLANO PILOTO"
xpath_cidade = (
    f"//li[contains(@class,'select2-results__option') "
    f"and normalize-space(text())='{nome_cidade}']"
)

elemento_cidade = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cidade)))
elemento_cidade.click()
print(f"Opção '{nome_cidade}' selecionada com sucesso!")

time.sleep(5)

# --- Abre o dropdown de Bairro ---
botao_bairro = wait.until(EC.element_to_be_clickable((By.ID, "select2-bairros-container")))
botao_bairro.click()
print("Dropdown de bairro aberto.")

# --- Seleciona a opção 'JARDIM BOTÂNICO' ---
nome_bairro = "JARDIM BOTÂNICO"
xpath_bairro = (
    "//li[contains(@class,'select2-results__option') and "
    "(normalize-space(text())='JARDIM BOTÂNICO' or normalize-space(text())='JARDIM BOTANICO')]"
)

elemento_bairro = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_bairro)))
elemento_bairro.click()
print(f"Opção '{nome_bairro}' selecionada com sucesso!")

time.sleep(5)

# --- Abre o dropdown de Bairro ---
botao_bairro = wait.until(EC.element_to_be_clickable((By.ID, "select2-bairros-container")))
botao_bairro.click()
print("Dropdown de bairro aberto.")

# --- Espera a lista de bairros carregar ---
wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class,'select2-results__option')]")))

# --- Seleciona a opção 'ASA SUL' ---
nome_bairro = "ASA SUL"
xpath_bairro = (
    f"//li[contains(@class,'select2-results__option') "
    f"and normalize-space(text())='{nome_bairro}']"
)
elemento_bairro = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_bairro)))
elemento_bairro.click()
print(f"Opção '{nome_bairro}' selecionada com sucesso!")

time.sleep(5)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# --- Configurações ---
url = "https://www.dfimoveis.com.br/venda/df/brasilia/asa-sul/apartamento"
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 15)  # Espera até 15 segundos

time.sleep(10)  # Dar tempo da página carregar totalmente

# --- Encontrar todos os cards de imóveis ---
cards = driver.find_elements(By.CSS_SELECTOR, "a.imovel-card")

# Lista para armazenar os dados
imoveis = []

for card in cards:
    info = {}
    
    # Link do imóvel
    info["link"] = card.get_attribute("href")
    
    # Localização
    localizacao = card.find_element(By.CSS_SELECTOR, "h2.ellipse-text")
    info["localizacao"] = localizacao.text.strip() if localizacao else None
    
    # Tipo e metragem
    tipo_metragem = card.find_element(By.CSS_SELECTOR, "h3.mobile-ellipse-view")
    info["tipo_metragem"] = tipo_metragem.text.strip() if tipo_metragem else None
    
    # Descrição curta
    descr_curta = card.find_elements(By.CSS_SELECTOR, "h3")[1]  # segunda h3 é a descrição curta
    info["descricao_curta"] = descr_curta.text.strip() if descr_curta else None
    
    # Preço e valor m²
    precos = card.find_elements(By.CSS_SELECTOR, "div.imovel-price h4 span.body-large.bold")
    info["preco"] = precos[0].text.strip() if len(precos) > 0 else None
    info["valor_m2"] = precos[1].text.strip() if len(precos) > 1 else None
    
    # Área e quartos
    features = card.find_elements(By.CSS_SELECTOR, "div.imovel-feature .border-1")
    info["area"] = features[0].text.strip() if len(features) > 0 else None
    info["quartos"] = features[1].text.strip() if len(features) > 1 else None
    
    # Descrição longa
    descr_longa = card.find_element(By.CSS_SELECTOR, "h3.neutral-text")
    info["descricao_longa"] = descr_longa.text.strip() if descr_longa else None
    
    # Imobiliária e CRECI
    try:
        imob_anunciante = card.find_element(By.CSS_SELECTOR, "div.imovel-anunciante")
        info["imobiliaria"] = imob_anunciante.find_element(By.CSS_SELECTOR, "img").get_attribute("alt")
        info["creci"] = imob_anunciante.find_element(By.CSS_SELECTOR, "p").text.strip()
    except:
        info["imobiliaria"] = None
        info["creci"] = None
    
    # Imagem principal
    try:
        imagem = card.find_element(By.CSS_SELECTOR, "source[media='(min-width:781px)']")
        info["imagem"] = imagem.get_attribute("srcset")
    except:
        info["imagem"] = None
    
    # Selos
    selos = card.find_elements(By.CSS_SELECTOR, "div.imovel-image-badge")
    info["selos"] = ", ".join([selo.get_attribute("title") for selo in selos]) if selos else None
    
    # ID do imóvel
    try:
        favorito = card.find_element(By.CSS_SELECTOR, "span.favorito-resultado-busca")
        info["id_imovel"] = favorito.get_attribute("data-id")
    except:
        info["id_imovel"] = None
    
    # Adiciona à lista
    imoveis.append(info)

# --- Criar DataFrame ---
df = pd.DataFrame(imoveis)

# --- Exibir resultado ---
print(df.head())

# (Opcional) Salvar em Excel
# df.to_excel("imoveis_asa_sul.xlsx", index=False)

# Fechar o navegador
driver.quit()
