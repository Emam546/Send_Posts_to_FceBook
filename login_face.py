from types import FunctionType
from selenium import webdriver
import time
from constants import FaceBook_pattern
import os
def login_drive(driver:webdriver.Chrome,email,password):
    driver.get("https://www.facebook.com/")
    # login
    driver.find_element_by_xpath("//input[@id='email']").send_keys(email)
    driver.find_element_by_xpath("//input[@id='pass']").send_keys(password)
    driver.find_element_by_xpath("//button[@name='login']").click()

def post2groups(driver:webdriver.Chrome,groups:list,message:str,save_posts):
    newgroups=[]
    for i,group in enumerate(groups):
        try:
            groupCode=FaceBook_pattern.sub(r"\5",group)
            print(f"loading {i} group page {group}")
            tries=0
            while tries<3:
                try:
                    driver.get(group)
                    print("finding the clicking page element to page")
                    clickingBox=driver.find_element_by_xpath("//div[@class='oajrlxb2 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x i1ao9s8h esuyzwwr f1sip0of abiwlrkh p8dawk7l lzcic4wl bp9cbjyn b3i9ofy5 orhb3f3m czkt41v7 fmqxjp7s emzo65vh j83agx80 btwxx1t3 buofh1pr jifvfom9 l9j0dhe7 idiwt2bm kbf60n1y cxgpxx05 d1544ag0 sj5x9vvc tw6a2znq']")
                    break
                except Exception as e:
                    if tries==2:print(e)
                    pass
                tries+=1
            else:
                print(f"FAILED OT GET TO {group}")
                continue
            #clickingBox=driver.find_element_by_xpath("//div[@data-pagelet='GroupInlineComposer']").find_elements_by_xpath("//div[@role='button']")[0]
            tries=0
            while tries<7:
                try:
                    clickingBox.click()
                    break
                except:pass
                tries+=1
            else:
                continue
            tries=0
            while tries<6:
                try:
                    post_button = driver.find_element_by_xpath("//div[@aria-label='نشر' or @aria-label='Post']")
                    
                    post_box=driver.find_element_by_xpath("//div[@aria-label='إنشاء منشور عام...' or @aria-label='Create a public post…' or @aria-label='Write something...']")
                    post_box.send_keys(message)

                    print("Clicking on the Post button")
                    post_button.click()
                    newgroups.append(group)
                    save_posts(group)
                    print("succeed in posting")
                    break
                except Exception as e:
                    if tries==5:print(e)
                tries+=1
            else:
                continue
        
            time.sleep(20)
            print("finding first post")
            posts=driver.find_elements_by_xpath("//div[@data-pagelet='GroupFeed']/div")
            
            if len(posts)<=1:
                print("there is no posts sended")
                continue
            firstPost=posts[-2]
            #putting the message here to check if hte post completely loaded or not
            buttontoclick=firstPost.find_element_by_xpath("//div[@aria-label='الإجراءات التي يمكن اتخاذها لهذا المنشور' or @aria-label='Actions for this post']")
            
            tries=0
            while tries<10:
                try:
                    y=int(firstPost.location["y"])-100
                    driver.execute_script(f"window.scrollTo(0,{y})", firstPost)
                    time.sleep(1)
                    _img_in=0
                    while True:
                        filename=f"{groupCode}_({_img_in}).png"
                        file=os.path.join(".\\Images",filename)
                        if os.path.exists(file):
                            _img_in+=1
                            continue
                        driver.save_screenshot(file)
                        break
                    print(f"Screenshot saved in {file}")
                    break
                except Exception as e:
                    if tries==9:print(e)
                    pass
                tries+=1
            else:
                continue
                
            tries=0
            while tries<10:
                try:
                    buttontoclick.click()
                    print("Clicking on the options menu button")
                    break
                except:
                    pass
                tries+=1
            else:
                print("FAILED ON GETTING THE POST")
                continue
            clickednoposting_button=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[8]')

            tries=0
            while tries<4:
                try:
                    clickednoposting_button.click()
                    print("Removing Comments process succeed")
                    break
                except:pass
                tries+=1
            
        except Exception as e:
            print(e)
            print("FAILED IN COMPLETE PROCESS")
    return newgroups
def get_groups_posts(driver:webdriver.Chrome):
    print("Getting groups")
    tries=0
    while tries<3:
        try:
            driver.get("https://web.facebook.com/groups/feed")
            driver.find_element_by_xpath(f"//div[@role='separator']/following-sibling::div/following-sibling::div[1]/a")
            break
        except Exception as e:
            print(e)
            pass
        tries+=1
    else:
        print("ERROR IN GETTING ON THE GROUPS PAGE")
        return
    while True:
        try:
            driver.maximize_window()
            break
        except Exception as e:
            print(e)

    i = 0
    result=[]
    try:
        while True:
            #groups = driver.find_elements_by_xpath("//div[@role='separator']/following-sibling::div/following-sibling::div/a/div/div[2]/div/div/div/div[1]/span/span/span")
            groups = driver.find_elements_by_xpath("//div[@role='separator']/following-sibling::div/following-sibling::div/a")
            driver.execute_script("arguments[0].scrollIntoView(true);", groups[i])
            result.append(groups[i].get_attribute("href"))
            if (i==len(groups)-1):
                try:
                    driver.find_element_by_xpath(f"//div[@role='separator']/following-sibling::div/following-sibling::div[{len(groups)+2}]/a")
                except:
                    break
                    
            i+=1
    except Exception as e:
        print(e)
    if not len(result):
        print("some problem went wrong in getting groups")
    print(f"Finished in Scraping groups with length of {len(result)}")
    return result
    
    