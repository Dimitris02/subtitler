from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.firefox.options import Options

c = Options()
c.headless = 1
TRANSLATE_TO=''
driver = webdriver.Firefox(options=c)
driver.get("https://www.deepl.com/en/translator")
inp_box = driver.find_element(By.CSS_SELECTOR , 'd-textarea.min-h-0 > div:nth-child(1)')


while True:
    try:
        inp_box = driver.find_element(By.CSS_SELECTOR , 'd-textarea.min-h-0 > div:nth-child(1)')
        break
    except:
        sleep(1)

def pick_lang(l):

    inp_box.send_keys(l)

    if TRANSLATE_TO=='':
        return
    else:
        
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#headlessui-popover-button-5').click()
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[id*='search-bar-id-']").send_keys(TRANSLATE_TO)
        sleep(3)
        try:
            driver.find_element(By.CSS_SELECTOR, 'button.hover\:bg-dark-8:nth-child(1)').click()
            print(TRANSLATE_TO+" selected...")
        except:
            current=driver.find_element(By.CSS_SELECTOR, 'span.overflow-hidden:nth-child(2)').get_attribute("innerHTML")
            print("Chosen language not found. Defaulting to "+current+".") 
    
    inp_box.clear()

def vid2sub(v):
    a = v[:v.rfind(".")]
    return a+"_TRANSLATED.srt"

def deepl(line):
    inp_box.send_keys(line)

    sleep(3)
    while True:
        try:
            out_box = driver.find_element(By.CSS_SELECTOR, ".last\:grow > div:nth-child(1) > p:nth-child(2) > span:nth-child(1)") 
            break
        except:
            sleep(1)

    out_box.click()
    tr=out_box.get_attribute("innerHTML")
    inp_box.clear()
    print(tr)
    return tr+"\n"

def translate(file, name, T):
    global TRANSLATE_TO

    TRANSLATE_TO=T
    with open(file, "r", encoding='utf-8') as f: lines=f.readlines()

    pick_lang(lines[2])
    
    for i in range(2,len(lines)-1,4):
        lines[i]=deepl(lines[i][:-3])

    with open(vid2sub(name), "wb") as f: f.write(''.join(lines).encode('utf8'))
