from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup

result = list()

url = 'https://bbs.huaweicloud.com/blogs'
# 创建Chrome浏览器实例
driver = webdriver.Chrome()

# 打开目标页面
driver.get(url)

button = driver.find_element(By.CSS_SELECTOR, 'a.one-line[title="云计算"]')
button.click()
time.sleep(3)
# 模拟向下滚动获取更多内容，可以根据需求修改滚动次数或滚动高度
scroll_count = 3  #排除前两次下拉滚动
for _ in range(scroll_count):
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
    # 等待加载完成，可以根据网页性能调整等待时间
    time.sleep(5)
    # 模拟点击“加载更多”按钮，可以根据按钮的XPath或其他选择器来定位它
click_count = 10 # 设置变量以控制爬取数量
for _ in range(click_count):
    load_more_button = driver.find_element(By.XPATH, "//span[@class='m-blog-list-loading add-more']")
    if (load_more_button != None):
        load_more_button.click()
    time.sleep(5)
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")

# 获取滚动后的页面内容
page_content = driver.page_source
# 现在您可以使用page_content来解析和处理获取到的数据，例如使用BeautifulSoup库
soup = BeautifulSoup(page_content, 'html.parser')
articles = soup.find_all('div', class_='blogs-item')

# 遍历每篇文章并提取标题和内容
for article in articles:
    text = article.text
    text = text.split('\n')
    temp1 = list()
    temp2 = list()
    for i in range(len(text)):
        if text[i] != '' and text[i] != 'HOT':
            temp1.append(text[i])

    href = article.contents[1]['href']
    href = 'https://bbs.huaweicloud.com' + href
    temp2.append(temp1[0])
    temp2.append(temp1[1])
    temp2.append(href)

    result.append(temp2)

with open("云计算.txt", "w", encoding='utf-8') as file:
    for articles in result:
        for text in articles:
            file.write(text+"\n")
        file.write("--------------------------------------------------\n")
print(result)

driver.quit()
