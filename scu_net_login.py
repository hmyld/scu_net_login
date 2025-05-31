from playwright.sync_api import sync_playwright
import time
url="http://192.168.2.135"
def usr_ipt():
    username = input("请输入账号：")
    password = input("请输入密码：")
    save_condition = input("是否保存密码? (y/n)")
    if save_condition.lower() == 'y':
        with open('account.txt', 'w') as f:
            f.write(f"{username}\n{password}")
        print("账号密码已保存，稍后你可以在同一目录中account.txt中修改")
    return username, password
def load_account():
    try:
        with open('account.txt', 'r') as f:
            username = f.readline().strip()
            password = f.readline().strip()
        return username, password
    except FileNotFoundError:
        return None, None
def logout(page):
    try:
        logout_button = page.wait_for_selector('div#toLogOut')
        logout_button.click()
    except Exception as e:
        print(f"等待或点击按钮时出错: {e}")
    try:
        sure_button = page.wait_for_selector('a#sure')
        sure_button.click()
    except Exception as e:
        print(f"等待或点击按钮时出错: {e}")
def login():
    username,password=load_account()
    if not username and not password:
        username,password=usr_ipt()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        )
        page = context.new_page()
        page.goto(url)
        try:
            page.wait_for_selector('span:text("您已成功连接校园网!")')
            temp=input("您已经连接到校园网了，想退出吗? (y/n)")
            if temp=='y':
                logout(page)
            exit(1)
        except Exception as e:
            pass        
        time.sleep(1)
        page.keyboard.press('Tab')
        page.keyboard.type(password)
        page.keyboard.press('Tab')
        page.keyboard.press('Enter')
        page.keyboard.type(username)
        page.keyboard.press('Enter')
        time.sleep(1)
        page.keyboard.press('Tab')
        page.keyboard.press('Tab')
        page.keyboard.press('Tab')
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Space")
        time.sleep(1)
        page.keyboard.press('Tab')
        page.keyboard.press('Tab')
        page.keyboard.press('Tab')
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Space")
        time.sleep(1)
        page.keyboard.press('Tab')
        page.keyboard.press('Tab')
        page.keyboard.press('Tab')
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Space")
        try:
            page.wait_for_selector('span:text("您已成功连接校园网!")')
            print("连接成功!")
            exit(0)
        except Exception as e:
            print("校园网+三种运营商连接全部失败，请检查网络连接状况，账号密码是否正确以及是否有套餐余额！") 
            exit(2)
        browser.close()

if __name__ == "__main__":
    login()