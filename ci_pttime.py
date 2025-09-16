#!/usr/bin/python3
"""
name: pttime 签到
cron: 28 9 * * *
"""
import os
import requests
import re
import random
import time
import notify


def checkin():
    if os.getenv("PTTIME_COOKIE"):
        cookie = os.getenv("PTTIME_COOKIE")
    else:
        print("PTTIME_COOKIE environment variable not set")
        return

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "cookie": cookie
    }

    response = requests.get(
        "https://www.pttime.org/attendance.php",
        headers=headers,
    )
    text = response.text
    if response.status_code == 200 and "签到成功" in text:
        # 提取签到天数和获得的魔力值
        checkin_day = re.findall(r"已连续签到 <b>(\d+)</b> 天", text)
        magic_count = re.findall(r"本次签到获得 <b>(\d+)</b> 个魔力值", text)
        print(f"pttime 签到成功！连续签到: {checkin_day} 天, 获得魔力值: {magic_count}")
        notify.send('pttime 签到成功！', f'连续签到: {checkin_day} 天, 获得魔力值: {magic_count}')
    else:
        print(f"pttime 签到失败，状态码: {response.status_code}, 错误信息: {response.text}")
        notify.send('pttime 签到失败！', 'pttime 签到失败！')


def main():
    # 随机延迟 1-10 秒
    delay = random.randint(1, 10)
    print(f"等待 {delay} 秒后开始签到...")
    time.sleep(delay)
    checkin()


if __name__ == "__main__":
    main()
