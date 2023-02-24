from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from wcwidth import wcswidth
from openpyxl import load_workbook
import pandas as pd
import os
import time
from bs4 import BeautifulSoup as bs

abs_path = os.path.abspath(__file__)
dirt = os.path.dirname(abs_path) +'/'

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--mute-audio')  # 브라우저에 음소거 옵션을 적용합니다.
options.add_argument('incognito')  # 시크릿 모드의 브라우저가 실행됩니다.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(
    'http://www.nature.go.kr/kbi/fngs/smpl/selectFngsSmplGnrlList1.do')
driver.implicitly_wait(5)

def search_detect(name_input):
    search_box = driver.find_element(By.XPATH,'//*[@id="tmpSearchWrd"]') #search box
    search_box.send_keys(name_input)
    search_box.send_keys(Keys.RETURN)
    
    result_num = int(driver.find_element(By.XPATH,'//*[@id="txt"]/form[2]/div[1]/p/span[1]').text) #검색결과 갯수
    
    
    hund_view('2') #1차 검색결과 100개까지 보기
    time.sleep(1)

    if int(result_num) ==1: #1차 검색 결과가 1개 일때if int(result_num) == 1:
        result_s =single()
        return result_s
    else :
        result_m = multi()
        return result_m


def single():
    final_list =[]
    driver.find_element(By.XPATH,'//*[@id="txt"]/form[2]/table/tbody/tr/td[2]').click() # 첫번째 종을 클릭

    time.sleep(1)
    hund_view('3')

    id_list = crawl_id()
    
    for id in id_list:
        mid_list = col_detail(id)
        final_list.append(mid_list)

    return final_list
    
def multi():
    final_list =[]
    species_num = driver.find_elements(By.XPATH,'//*[@id="txt"]/form[2]/table/tbody/tr')
    sp_dict = {}
    for i in range(1,len(species_num)+1): #speices 수준
        driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div[2]/form[2]/table/tbody/tr[{i}]/td[2]').click()
        time.sleep(1)
        hund_view('3')

        id_list = crawl_id()
        
        driver.execute_script('window.open();')
        driver.switch_to.window(driver.window_handles[-1])

        for id in id_list: #specimen 수준
            mid_list = col_detail(id)
            final_list.append(mid_list)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        driver.back()
        driver.back()

    return final_list
       


def crawl_id():
    driver.refresh()
    current_html_1 = driver.page_source
    soup_1 = bs(current_html_1,'lxml')

    soup_2 = soup_1.find('form',{'name':'form'})
    soup_3 = soup_2.find_all('a')

    detail_info = '([^(fn_detailInfo)][[FS][ 0-9]{10})' #표본 번호 정규표현식
    
    
    smp_id = re.findall(detail_info,str(soup_3))
    smp_id = list(set(smp_id))
    
    return smp_id

 
def hund_view(pos):
    page_unit = Select(driver.find_element(By.XPATH,'//*[@id="pageUnit"]'))
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pageUnit"]')))
    page_unit.select_by_visible_text('100')
    driver.find_element(By.XPATH,'//*[@id="txt"]/form[%s]/div[1]/fieldset/a/input'% pos).click()

 
def col_detail(smpNO): 
    base_url = 'http://www.nature.go.kr/kbi/fngs/smpl/selectFngsSmplGnrlListDtl.do?fngsSmplNo='
    last_url = base_url+smpNO
    driver.get(last_url)
    driver.implicitly_wait(5)
    
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    info_list = []    
    for i in range(1,8):
        up_info = driver.find_element(By.XPATH,'//*[@id="txt"]/form[3]/div[1]/dl/dd[%s]' % i).text
        info_list.append(up_info)
        
    for j in range(1,4):
        down_info = driver.find_element(By.XPATH,'//*[@id="txt"]/form[3]/div[4]/table/tbody/tr[%s]/td' % j).text
        info_list.append(down_info)
        
    return (info_list)



def save_file(search_keyword):
    info = search_detect(search_keyword)
    

    result_KFDA_pan=pd.DataFrame(info)
    result_KFDA_pan.columns=['학명','버섯명','분류군','표본바코드번호','채집관리번호','과제명','보유기관',
                             '채집지','채집일자','채집자']

    save_time =time.strftime('%Y%m%d_%H%M',time.localtime(time.time())) 

    excel_dir = f'{dirt}{search_keyword}_KNA_result_({save_time}).xlsx'

    result_KFDA_pan.to_excel(excel_dir,sheet_name='sheet1',index=False)
    
    wb = load_workbook(filename=excel_dir, data_only=True)
    ws = wb.active
    for column_cells in ws.columns:
        length = max(wcswidth(str(cell.value)) * 1.1 for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length
    wb.save(excel_dir)
    
    
    

    print('excel 파일 저장됨')
search_keyword = 'Inonotus'    
save_file(search_keyword)


