#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日资讯推送脚本（精简版 - 无需API Key）
使用免费公开数据源，无需注册申请
"""

import json
import urllib.request
import datetime
import os
import calendar

# 配置
SENDKEY = os.environ.get('SENDKEY', 'SCT328104TbVhbRlWRSj6lTJP7pRaAXMot')
today = datetime.datetime.now()
today_str = today.strftime("%Y年%m月%d日")
weekday_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
weekday = weekday_list[today.weekday()]
text = f"📰 每日简报 | {today_str} {weekday}"

# ============ 免费数据源 ============

def fetch_weather():
    """获取青岛天气 - Open-Meteo完全免费"""
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=36.0671&longitude=120.3826&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Asia/Shanghai&forecast_days=4"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            weather_codes = {
                0: "☀️ 晴", 1: "🌤️ 晴", 2: "⛅ 多云", 3: "☁️ 阴",
                45: "🌫️ 雾", 48: "🌫️ 雾凇",
                51: "🌦️ 毛毛雨", 53: "🌧️ 中雨", 55: "🌧️ 大雨",
                61: "🌧️ 小雨", 63: "🌧️ 中雨", 65: "🌧️ 大雨",
                71: "🌨️ 小雪", 73: "🌨️ 中雪", 75: "🌨️ 大雪",
                95: "⛈️ 雷雨", 96: "⛈️ 雷伴冰雹", 99: "⛈️ 雷伴冰雹"
            }
            
            current = data.get('current', {})
            daily = data.get('daily', {})
            
            weather_code = current.get('weather_code', 0)
            
            # 构建4天预报
            forecast = []
            daily_codes = daily.get('weather_code', [])
            daily_max = daily.get('temperature_2m_max', [])
            daily_min = daily.get('temperature_2m_min', [])
            
            day_names = ["今天", "明天", "后天", "大后天"]
            for i in range(min(4, len(daily_codes))):
                code = daily_codes[i] if i < len(daily_codes) else 0
                temp_max = daily_max[i] if i < len(daily_max) else '--'
                temp_min = daily_min[i] if i < len(daily_min) else '--'
                forecast.append({
                    "day": day_names[i],
                    "icon": weather_codes.get(code, "☁️")[0],
                    "weather": weather_codes.get(code, "多云")[2:],
                    "temp": f"{temp_min}°~{temp_max}°"
                })
            
            return {
                "current_temp": current.get('temperature_2m', '--'),
                "current_weather": weather_codes.get(weather_code, "☁️ 多云"),
                "humidity": current.get('relative_humidity_2m', '--'),
                "wind": current.get('wind_speed_10m', '--'),
                "forecast": forecast
            }
    except Exception as e:
        return None


def get_github_trending():
    """GitHub热门项目 - 无需API Key"""
    try:
        # 获取最近一周的热门仓库
        url = "https://api.github.com/search/repositories?q=created:>2025-03-20&sort=stars&order=desc&per_page=5"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('items', [])[:5]
            return [{
                "title": item.get('name', ''),
                "desc": item.get('description', '无描述')[:40] + '...' if item.get('description') else '热门开源项目',
                "stars": item.get('stargazers_count', 0),
                "url": item.get('html_url', '')
            } for item in items]
    except:
        return []


def get_daily_quote():
    """每日一句 - 使用本地轮换"""
    quotes = [
        ("种一棵树最好的时间是十年前，其次是现在。", "非洲谚语"),
        ("不积跬步，无以至千里。", "荀子"),
        ("业精于勤，荒于嬉。", "韩愈"),
        ("千里之行，始于足下。", "老子"),
        ("宝剑锋从磨砺出，梅花香自苦寒来。", "古诗"),
        ("天道酬勤。", "古语"),
        ("路漫漫其修远兮，吾将上下而求索。", "屈原"),
        ("博学之，审问之，慎思之，明辨之，笃行之。", "《中庸》"),
        ("工欲善其事，必先利其器。", "《论语》"),
        ("学而不思则罔，思而不学则殆。", "《论语》"),
    ]
    # 根据日期轮换
    index = today.timetuple().tm_yday % len(quotes)
    return quotes[index]


def get_job_hunting_tips():
    """求职小贴士 - 根据日期轮换"""
    tips = [
        "📄 简历优化：突出量化成果，用数字说话",
        "🎯 面试准备：研究公司业务，准备3个有深度的问题",
        "💼 职业规划：明确短期目标（1年）和长期目标（5年）",
        "🤝 人脉拓展：LinkedIn更新状态，主动联系行业前辈",
        "📚 技能提升：每天花30分钟学习行业新技术",
        "📝 面试复盘：记录每次面试问题，持续改进",
        "🎁 薪资谈判：了解市场行情，自信表达期望",
        "🔍 职位搜索：设置多个关键词组合，扩大搜索范围",
        "💪 心态调整：求职是双向选择，保持自信",
        "📧 跟进技巧：面试后24小时内发送感谢邮件",
    ]
    index = today.timetuple().tm_yday % len(tips)
    return tips[index]


def get_this_day_in_history():
    """历史上的今天"""
    month = today.month
    day = today.day
    
    # 简化版历史事件（可以扩展）
    events = {
        (3, 27): "1968年 - 人类首次绕月飞行返回地球",
        (3, 28): "1979年 - 美国三里岛核电站事故",
        (3, 29): "1974年 -  NASA发现首个太阳系外行星证据",
        (3, 30): "1981年 - 里根总统遇刺受伤",
        (3, 31): "1999年 - 中国恢复对澳门行使主权筹备工作完成",
        (4, 1): "2001年 - 中美撞机事件",
        (4, 2): "1982年 - 阿根廷出兵攻占福克兰群岛",
    }
    
    return events.get((month, day), None)


# ============ 企业招聘数据 ============
all_jobs = [
    {"name": "中车青岛四方机车", "industry": "轨道交通装备", "salary": "月薪30K+", "positions": "博士/硕士/本科", "url": "https://www.crrcgc.cc/", "tags": ["国企", "事业编", "博士30万安家费"], "keywords": ["设备", "工程师", "机械", "制造"]},
    {"name": "海尔集团", "industry": "家电世界500强", "salary": "面议", "positions": "机械/自动化/设备等", "url": "https://www.haier.cn/", "tags": ["世界500强"], "keywords": ["设备", "机械", "制造", "自动化"]},
    {"name": "海信集团", "industry": "家电上市公司", "salary": "面议", "positions": "信动力计划", "url": "https://jobs.hisense.com/", "tags": ["上市公司", "股权激励"], "keywords": ["设备", "制造", "电子"]},
    {"name": "思锐智能", "industry": "半导体/芯片", "salary": "月薪16.2K", "positions": "21个岗位", "url": "https://www.srzt.com/", "tags": ["芯片", "集成电路"], "keywords": ["半导体", "设备", "SMT", "芯片"]},
    {"name": "歌尔微电子", "industry": "半导体/声学", "salary": "月薪20K+", "positions": "100+岗位", "url": "https://www.goertek.com/", "tags": ["上市", "半导体", "声学"], "keywords": ["半导体", "电子", "设备", "工程师"]},
    {"name": "鼎信通讯", "industry": "通信/芯片", "salary": "面议", "positions": "50+岗位", "url": "https://www.dingxin.com/", "tags": ["上市", "芯片", "通信"], "keywords": ["芯片", "电子", "工程师", "研发"]},
    {"name": "青岛光电半导体", "industry": "半导体/显示", "salary": "面议", "positions": "30+岗位", "url": "https://www.qdopto.com/", "tags": ["半导体", "显示面板"], "keywords": ["半导体", "电子", "设备", "调试"]},
    {"name": "兴航光电", "industry": "光电/半导体", "salary": "月薪17.6K", "positions": "25个岗位", "url": "https://www.qdgxjt.com/", "tags": ["研发", "光电"], "keywords": ["电子", "半导体", "光学"]},
    {"name": "中车成型科技", "industry": "高端装备", "salary": "月薪20.7K", "positions": "38个岗位", "url": "https://www.crrcgc.cc/", "tags": ["研发", "复合材料"], "keywords": ["设备", "机械", "复合材料", "成型"]},
    {"name": "雷沃重工", "industry": "工程机械", "salary": "月薪15.6K", "positions": "97个岗位", "url": "https://www.lovol.com/", "tags": ["农机", "机械"], "keywords": ["设备", "机械", "制造"]},
    {"name": "青岛电建三公司", "industry": "电力工程", "salary": "月薪15.1K", "positions": "31个岗位", "url": "https://www.sepcc3.com/", "tags": ["风电", "光伏"], "keywords": ["设备", "电气", "电力"]},
    {"name": "双瑞海洋", "industry": "环保工程", "salary": "月薪14.4K", "positions": "24个岗位", "url": "https://www.sunruitech.com/", "tags": ["海水淡化", "上市"], "keywords": ["设备", "工程"]},
    {"name": "双星集团", "industry": "轮胎/橡胶", "salary": "月薪10.3K", "positions": "59个岗位", "url": "https://www.double-star.com/", "tags": ["上市公司", "机器人"], "keywords": ["设备", "机械", "自动化"]},
    {"name": "招商局工业青岛", "industry": "船舶重工", "salary": "月薪10.1K", "positions": "船舶/重工", "url": "https://www.cmiic.com.cn/", "tags": ["央企", "船舶"], "keywords": ["设备", "重工", "制造"]},
    {"name": "中石化青岛炼化", "industry": "石化/化工", "salary": "面议", "positions": "设备/技术", "url": "https://www.qlsh.com.cn/", "tags": ["央企", "石化"], "keywords": ["设备", "维护", "工程师"]},
]

CORE_KEYWORDS = ["设备", "半导体", "SMT", "XRD", "光学", "检测", "仪器", "拉曼", "系统集成", "工程师", "FMEA", "可靠性", "精度", "性能验证"]
IMPORTANT_KEYWORDS = ["机械", "制造", "电子", "自动化", "电气", "军工", "航天", "芯片", "集成电路", "调试", "安装", "技术支持", "维护", "工厂", "材料", "成型", "复合材料"]
EXTRA_KEYWORDS = ["CAD", "PRO/E", "ANSYS", "维修", "生产", "研发", "技术"]


def match_score(job):
    """岗位匹配评分"""
    score = 0
    match_reasons = []
    job_keywords = set(job.get("keywords", []))
    job_text = job["name"] + job["industry"] + " ".join(job["tags"])

    for kw in CORE_KEYWORDS:
        if kw in job_keywords:
            score += 5
            match_reasons.append(kw)
        elif kw in job_text:
            score += 2

    for kw in IMPORTANT_KEYWORDS:
        if kw in job_keywords:
            score += 3
            match_reasons.append(kw)
        elif kw in job_text:
            score += 1

    for kw in EXTRA_KEYWORDS:
        if kw in job_keywords:
            score += 1
            match_reasons.append(kw)

    industry_bonus = {"半导体": 8, "芯片": 8, "集成电路": 8, "光电": 6, "光学": 6, "仪器": 6, "高端装备": 5, "工程机械": 4, "智能制造": 4}
    for ind, bonus in industry_bonus.items():
        if ind in job["industry"]:
            score += bonus

    match_reasons = list(dict.fromkeys(match_reasons))[:3]
    return score, match_reasons


def build_desp():
    """构建推送内容"""
    
    # 获取数据
    weather = fetch_weather()
    github_trending = get_github_trending()
    quote, quote_author = get_daily_quote()
    job_tip = get_job_hunting_tips()
    history_event = get_this_day_in_history()
    
    # 构建天气字符串
    if weather:
        weather_table = "| 日期 | 天气 | 温度 |\n|:----:|:----:|:----:|\n"
        for day in weather['forecast']:
            weather_table += f"| {day['day']} | {day['icon']} {day['weather']} | {day['temp']} |\n"
        weather_str = f"""
**🌡️ 当前天气**
青岛：{weather['current_weather']} {weather['current_temp']}°C | 湿度 {weather['humidity']}% | 风速 {weather['wind']}km/h

**📅 未来4天预报**

{weather_table}
"""
    else:
        weather_str = "> 天气数据获取失败"
    
    # 构建GitHub热榜
    if github_trending:
        github_str = "\n".join([f"`{i+1}` ⭐ **[{item['title']}]({item['url']})** · {item['stars']} stars\n　　{item['desc']}" for i, item in enumerate(github_trending)])
    else:
        github_str = "> GitHub数据获取失败"
    
    # 历史上的今天
    history_str = f"\n> 📜 历史上的今天：{history_event}\n" if history_event else ""
    
    # 岗位匹配
    scored_jobs = [(j, *match_score(j)) for j in all_jobs]
    scored_jobs.sort(key=lambda x: x[1], reverse=True)
    recommended = [(j, s, reasons) for j, s, reasons in scored_jobs if s >= 10][:5]
    
    rec_lines = []
    for j, s, reasons in recommended:
        tags = " · ".join(j['tags'][:2])
        match_pct = min(95, 60 + s * 2)
        reason_str = "、".join(reasons[:2]) if reasons else j['industry']
        rec_lines.append(
            f"✅ **[{j['name']}]({j['url']})** `匹配{match_pct}%`\n"
            f"　　{j['industry']} | {j['salary']} | 📌 {tags}\n"
            f"　　🎯 {reason_str}"
        )
    rec_str = "\n\n".join(rec_lines)
    
    # 组装内容
    desp = f"""# 📰 每日简报
**{today_str} {weekday}**

{history_str}
---
## 🌤️ 青岛天气

{weather_str}

> 📌 数据来源：Open-Meteo 实时数据

---
## 💡 每日一句

> "{quote}"
> 
> —— {quote_author}

---
## 💼 求职小贴士

{job_tip}

---
## 🔥 GitHub 热门项目

{github_str}

> 📌 数据来源：GitHub API

---
## 🎯 岗位推荐（系统/设备工程师）

> 根据你的简历智能匹配 | 6年+经验 | 半导体·高端仪器·工业检测

{rec_str}

🔗 更多：[智联招聘](https://www.zhaopin.com/qingdao/) · [BOSS直聘](https://www.zhipin.com/qingdao/)

---

> ⏰ {today_str} {weekday} ｜ 每日早上8:00推送
> 💬 无需API Key，数据每日自动更新
"""

    return desp


def send_push(text, desp):
    """发送推送"""
    data = {"text": text, "desp": desp}
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = response.read().decode('utf-8')
            print(f"推送成功: {result}")
            return True
    except Exception as e:
        print(f"推送失败: {e}")
        return False


if __name__ == "__main__":
    print(f"=== 开始执行每日推送 {today_str} {weekday} ===")
    desp = build_desp()
    send_push(text, desp)
    print("=== 执行完成 ===")
