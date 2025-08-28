#!/usr/bin/python3
"""
name: okpt 签到
cron: 28 9 * * *
"""
import os

import requests
import re
import random
import time
import notify


def checkin():
    if os.getenv("OKPT_COOKIE"):
        cookie = os.getenv("OKPT_COOKIE")
    else:
        print("OKPT_COOKIE environment variable not set")
        return

    headers = {
        "upgrade-insecure-requests": "1",
        "dnt": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "cache-control": "no-cache",
        "cookie": cookie,
    }

    response = requests.get(
        f"https://www.okpt.net/attendance.php",
        headers=headers,
    )
    text = response.text
    if response.status_code == 200 and "签到成功" in text:
        # 已连续签到 <b>39</b> 天，本次签到获得 <b>3900</b> 个魔力值
        checkin_day = re.findall(r"已连续签到 <b>(\d+)</b> 天", text)
        magic_count = re.findall(r"本次签到获得 <b>(\d+)</b> 个魔力值", text)
        print(f"okpt 签到成功！连续签到: {checkin_day} 天, 获得魔力值: {magic_count}")
        notify.send('okpt 签到成功！', f'连续签到: {checkin_day} 天, 获得魔力值: {magic_count}')
    else:
        print(f"okpt 签到失败，状态码: {response.status_code}, 错误信息: {response.text}")
        notify.send('okpt 签到失败！', 'okpt 签到失败！')


def main():
    # 随机延迟 1-10 秒
    delay = random.randint(1, 10)
    print(f"等待 {delay} 秒后开始签到...")
    time.sleep(delay)
    checkin()


if __name__ == "__main__":
    main()
