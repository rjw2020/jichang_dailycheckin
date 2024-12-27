import json
import os
import requests

# server酱
domain = 'https://ikuuu.one'
SCKEY = os.environ.get('SCKEY')
login_url = f'{domain}/auth/login'
check_url = f'{domain}/user/checkin'
info_url = f'{domain}/user/profile'


def work(email, passwd):
    session = requests.session()
    header = {
        'origin': domain,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    data = {
        'email': email,
        'passwd': passwd
    }
    content = ''
    try:
        print(f'{email} 进行登录...')
        response = json.loads(session.post(url=login_url, headers=header, data=data).text)
        print(response['msg'])
        # 获取账号名称
        info_html = session.get(url=info_url, headers=header).text
        # 进行签到
        result = json.loads(session.post(url=check_url, headers=header).text)
        print(result['msg'])
        content = result['msg']
    except:
        content = '签到失败'
        print(content)
    finally:
        # 进行推送
        print(f'sckey = {SCKEY}')
        if SCKEY:
            push_url = 'https://sctapi.ftqq.com/{}.send?title=ikuuu自动签到任务提示&desp={}'.format(SCKEY, content)
            requests.post(url=push_url)
            print('推送成功')
        print("===================================================")


def main():
    # 配置用户名（一般是邮箱）
    email = os.environ.get("EMAIL")
    # 配置用户名对应的密码 和上面的email对应上
    passwd = os.environ.get("PASSWD")
    if email and passwd:
        email = email.split(",")
        passwd = passwd.split(",")
        for a, b in zip(email, passwd):
            work(a, b)


if __name__ == '__main__':
    main()
