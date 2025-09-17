#!/usr/bin/python3
"""
name: 龙湖天街签到
cron: 28 9 * * *
"""
import json
import os
import random
import time

import requests

import notify


def checkin(token):
    url = "https://gw2c-hw-open.longfor.com/lmarketing-task-api-mvc-prod/openapi/task/v1/signature/clock"

    payload = "{\"activity_no\":\"11111111111686241863606037740000\"}"
    headers = {
        'Host': 'gw2c-hw-open.longfor.com',
        'X-LF-DXRisk-Source': '5',
        'X-LF-Bu-Code': 'C20400',
        'X-LF-DXRisk-Captcha-Token': 'undefined',
        'X-GAIA-API-KEY': 'c06753f1-3e68-437d-b592-b94656ea5517',
        'X-LF-UserToken': token,
        'X-LF-Channel': 'C2',
        'Accept': 'application/json, text/plain, */*',
        'X-LF-DXRisk-Token': '68c7c171f8dX2pszpUwnm2bwnksHHtCWIsyD1Ca1',
        'token': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541022) XWEB/16467',
        'Origin': 'https://longzhu.longfor.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://longzhu.longfor.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'acw_tc=ac11000117580027548446323e59edaab0f4b04f639b943430db002bad3318',
        'Content-Type': 'application/json;charset=UTF-8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        try:
            resp_json = response.json()
            code = resp_json.get("code")
            message = resp_json.get("message", "")
            data = resp_json.get("data", {})

            if code == "0000":
                is_popup = data.get("is_popup", 0)
                if is_popup == 1:
                    # 签到成功
                    reward_info = data.get("reward_info", [])
                    if reward_info:
                        reward_num = reward_info[0].get("reward_num", 0)
                        print(f"龙湖天街签到成功！获得了 {reward_num} 个成长值")
                        notify.send('龙湖天街签到成功！', f'获得了 {reward_num} 个成长值')
                    else:
                        print("龙湖天街签到成功！")
                        notify.send('龙湖天街签到成功！', '龙湖天街签到成功！')
                else:
                    # 今天已经签过到了
                    print("龙湖天街今天已经签过到了")
                    notify.send('龙湖天街签到', '今天已经签过到了')
            elif code == "801001":
                # 登录已过期
                print(f"龙湖天街签到失败：{message}")
                notify.send('龙湖天街签到失败！', f'登录已过期：{message}')
            else:
                # 其他错误
                print(f"龙湖天街签到失败，错误代码: {code}, 错误信息: {message}")
                notify.send('龙湖天街签到失败！', f'错误代码: {code}, 错误信息: {message}')
        except json.JSONDecodeError:
            print(f"龙湖天街签到失败，响应解析错误: {response.text}")
            notify.send('龙湖天街签到失败！', '响应解析错误')
    else:
        print(f"龙湖天街签到失败，状态码: {response.status_code}, 错误信息: {response.text}")
        notify.send('龙湖天街签到失败！', f'状态码: {response.status_code}')


def main():
    if os.getenv("LONGFOR_TOKEN"):
        token = os.getenv("LONGFOR_TOKEN")
    else:
        print("LONGFOR_TOKEN environment variable not set")
        return
    # 随机延迟 1-10 秒
    delay = random.randint(1, 10)
    print(f"等待 {delay} 秒后开始签到...")
    time.sleep(delay)
    checkin(token)


if __name__ == "__main__":
    main()
