from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import openpyxl

def extract_comment_data(comment):
    html_content = comment.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    
    nickname_element = soup.select_one('a.nickname b')
    nickname = nickname_element.text if nickname_element else ''
    
    span_content_element = soup.select_one('p.full_content') or soup.select_one('p.content_more')
    span_content = span_content_element.text.strip() if span_content_element else ''
    
    if span_content.startswith(nickname):
        span_content = span_content[len(nickname):].strip()
    
    reaction_counts = {
        'vui': int(soup.select_one('div.item.t_r_1 strong').text) if soup.select_one('div.item.t_r_1 strong') else 0,
        'ngac_nhien': int(soup.select_one('div.item.t_r_3 strong').text) if soup.select_one('div.item.t_r_3 strong') else 0,
        'buon': int(soup.select_one('div.item.t_r_4 strong').text) if soup.select_one('div.item.t_r_4 strong') else 0
    }
    
    return nickname, span_content, reaction_counts

def extract_subcomment_data(sub_comment):
    html_content = sub_comment.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    
    nickname = soup.select_one('.nickname b').text
    span_content = (soup.select_one('.full_content') or soup.select_one('.content_more')).text.strip()
    if span_content.startswith(nickname):
        span_content = span_content[len(nickname):].strip()
    
    reaction_counts = {
        'vui': 0,
        'ngac_nhien': 0,
        'buon': 0
    }
    reactions_detail = soup.select_one('.reactions-detail')
    if reactions_detail:
        for item in reactions_detail.select('.item'):
            reaction_type = item.select_one('.icons img')['alt']
            count = int(item.select_one('strong').text)
            if reaction_type == 'Thích':
                reaction_counts['vui'] = count
            elif reaction_type == 'Ngạc nhiên':
                reaction_counts['ngac_nhien'] = count
            elif reaction_type == 'Buồn':
                reaction_counts['buon'] = count
    
    return nickname, span_content, reaction_counts

def export_to_excel(comments, subcomments):
    workbook = openpyxl.Workbook()
    sheet_comments = workbook.active
    sheet_comments.title = "Comments"
    sheet_subcomments = workbook.create_sheet(title="Subcomments")
    
    headers = ["Nickname", "Content", "Number of Vui", "Number of Ngac Nhien", "Number of Buon"]
    sheet_comments.append(headers)
    sheet_subcomments.append(headers)
    
    for comment in comments:
        row = [comment[0], comment[1], comment[2]['vui'], comment[2]['ngac_nhien'], comment[2]['buon']]
        sheet_comments.append(row)
    
    for subcomment in subcomments:
        row = [subcomment[0], subcomment[1], subcomment[2]['vui'], subcomment[2]['ngac_nhien'], subcomment[2]['buon']]
        sheet_subcomments.append(row)
    
    workbook.save("Vnexpress_comment.xlsx")

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    
    webdriver_service = Service("E:/VnExpressCrawlData/CrawVnexpress/chromedriver_win32/chromedriver.exe")
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    
    driver.get("https://vnexpress.net/ma-doc-nham-toi-nguoi-dung-iphone-viet-nguy-hiem-the-nao-4725781.html")
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "content-comment")))
    
    while True:
        load_more_buttons = driver.find_elements(By.CSS_SELECTOR, "div.view_more_coment.width_common.mb10 > a")
        for button in load_more_buttons:
            time.sleep(0.5)
            if button.is_displayed() and button.is_enabled():
                button.click()
        if len(load_more_buttons) == 1:
            break

    comments = []
    for comment in driver.find_elements(By.CLASS_NAME, "content-comment"):
        nickname, span_content, reaction_counts = extract_comment_data(comment)
        comments.append((nickname, span_content, reaction_counts))

    while True:
        found_link = False
        for comment_item in driver.find_elements(By.CLASS_NAME, "comment_item"):
            while len(comment_item.find_elements(By.CLASS_NAME, "view_all_reply")) > 0:
                try:
                    view_all_reply_link = comment_item.find_element(By.CLASS_NAME, "view_all_reply")
                    driver.execute_script("arguments[0].click();", view_all_reply_link)
                    found_link = True
                    time.sleep(0.5)
                except:
                    break
        if not found_link:
            break
            
    subcomments = []
    for sub_comment in driver.find_elements(By.CLASS_NAME, "sub_comment_item"):
        nickname, span_content, reaction_counts = extract_subcomment_data(sub_comment)
        subcomments.append((nickname, span_content, reaction_counts))

    driver.quit()

    export_to_excel(comments, subcomments)

if __name__ == "__main__":
    main()