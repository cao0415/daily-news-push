#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻资讯自动推送脚本（个性化定制版）
根据用户简历自动匹配推荐岗位
定时任务：每天早上8点执行
"""

import json
import urllib.request
import urllib.parse
import datetime
import os

# 尝试导入 requests，如果可用则优先使用
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# 从环境变量读取 sendkey（GitHub Actions 用），否则用默认值
sendkey = os.environ.get('SENDKEY', 'SCT328104TbVhbRlWRSj6lTJP7pRaAXMot')
today = datetime.datetime.now().strftime("%Y年%m月%d日")
weekday_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
weekday = weekday_list[datetime.datetime.now().weekday()]
text = f"📰 每日资讯 | {today} {weekday}"

# ============ 时政要闻 ============
politics_news = [
    {"title": "习近平外事活动", "desc": "近期重要外事活动及双边会谈成果", "hot": True},
    {"title": "京杭大运河水流贯通", "desc": "水利部宣布京杭大运河连续五年全线水流贯通", "hot": False},
    {"title": "十五五规划编制", "desc": "国家发改委启动十五五规划编制工作", "hot": True},
    {"title": "李强出席重要论坛", "desc": "国务院总理李强出席中国发展高层论坛年会", "hot": False},
    {"title": "人工智能+行动", "desc": "国务院印发AI与实体经济融合行动意见", "hot": True},
    {"title": "博鳌亚洲论坛", "desc": "2026年年会即将举办，主题聚焦亚洲发展", "hot": False},
    {"title": "国际交往", "desc": "中联部会见蒙古人民党代表团", "hot": False},
    {"title": "商务活动", "desc": "商务部会见外资高管，释放开放信号", "hot": False},
    {"title": "乡村振兴", "desc": "农业农村部部署2026年乡村振兴重点工作", "hot": False},
    {"title": "国防科技", "desc": "最新型装备研发取得新突破", "hot": False},
]

# ============ 科技新闻 ============
tech_news = [
    {"title": "AI产业发展", "desc": "中国AI企业超6000家，核心产业规模预计突破1.2万亿元", "hot": True},
    {"title": "国产大模型", "desc": "开源大模型全球累计下载量突破100亿次", "hot": False},
    {"title": "AI专利领先", "desc": "中国成为全球AI专利最大拥有国", "hot": False},
    {"title": "十五五AI规划", "desc": "国务院推动AI赋能千行百业", "hot": True},
    {"title": "巨头动态", "desc": "英伟达、字节、OpenAI密集发布技术突破", "hot": False},
    {"title": "面壁者计划", "desc": "国内AI团队启动破壁计划", "hot": False},
    {"title": "数字员工", "desc": "OpenClaw发布具备自主决策能力的AI产品", "hot": False},
    {"title": "本地模型", "desc": "边缘计算推动本地AI模型快速发展", "hot": False},
    {"title": "视频生成", "desc": "AI视频可控化技术取得突破", "hot": False},
    {"title": "应用落地", "desc": "生成式AI在各行业渗透率快速提升", "hot": False},
]

# ============ 全部企业招聘 ============
all_jobs = [
    {"name": "中车青岛四方机车", "industry": "轨道交通装备", "salary": "月薪30K+", "positions": "博士/硕士/本科", "url": "https://www.crrcgc.cc/", "tags": ["国企", "事业编", "博士30万安家费"], "keywords": ["设备", "工程师", "机械", "制造"]},
    {"name": "华能信息技术", "industry": "智能制造/AI", "salary": "月薪30K", "positions": "68个岗位", "url": "https://www.hnc.net.cn/", "tags": ["高薪", "AI"], "keywords": ["智能制造", "自动化"]},
    {"name": "海尔集团", "industry": "家电世界500强", "salary": "面议", "positions": "机械/自动化/设备等", "url": "https://www.haier.cn/", "tags": ["世界500强"], "keywords": ["设备", "机械", "制造", "自动化"]},
    {"name": "海信集团", "industry": "家电上市公司", "salary": "面议", "positions": "信动力计划", "url": "https://jobs.hisense.com/", "tags": ["上市公司", "股权激励"], "keywords": ["设备", "制造", "电子"]},
    {"name": "中车成型科技", "industry": "高端装备", "salary": "月薪20.7K", "positions": "38个岗位", "url": "https://www.crrcgc.cc/", "tags": ["研发", "复合材料"], "keywords": ["设备", "机械", "复合材料", "成型"]},
    {"name": "思锐智能", "industry": "半导体/芯片", "salary": "月薪16.2K", "positions": "21个岗位", "url": "https://www.srzt.com/", "tags": ["芯片", "集成电路"], "keywords": ["半导体", "设备", "SMT", "芯片"]},
    {"name": "雷沃重工", "industry": "工程机械", "salary": "月薪15.6K", "positions": "97个岗位", "url": "https://www.lovol.com/", "tags": ["农机", "机械"], "keywords": ["设备", "机械", "制造"]},
    {"name": "青岛电建三公司", "industry": "电力工程", "salary": "月薪15.1K", "positions": "31个岗位", "url": "https://www.sepcc3.com/", "tags": ["风电", "光伏"], "keywords": ["设备", "电气", "电力"]},
    {"name": "双瑞海洋", "industry": "环保工程", "salary": "月薪14.4K", "positions": "24个岗位", "url": "https://www.sunruitech.com/", "tags": ["海水淡化", "上市"], "keywords": ["设备", "工程"]},
    {"name": "渤星船舶科技", "industry": "船舶科技", "salary": "月薪13.3K", "positions": "9个岗位", "url": "https://www.bsship.com/", "tags": ["船舶", "海洋装备"], "keywords": ["设备", "制造"]},
    {"name": "上药国风药业", "industry": "医药", "salary": "月薪10.7K", "positions": "150个岗位", "url": "https://www.sphgf.com/", "tags": ["医药", "国企"], "keywords": ["设备", "制药设备"]},
    {"name": "双星集团", "industry": "轮胎/橡胶", "salary": "月薪10.3K", "positions": "59个岗位", "url": "https://www.double-star.com/", "tags": ["上市公司", "机器人"], "keywords": ["设备", "机械", "自动化"]},
    {"name": "招商局工业青岛", "industry": "船舶重工", "salary": "月薪10.1K", "positions": "船舶/重工", "url": "https://www.cmiic.com.cn/", "tags": ["央企", "船舶"], "keywords": ["设备", "重工", "制造"]},
    {"name": "澳柯玛", "industry": "家电/制冷", "salary": "面议", "positions": "技术/设备/制造", "url": "https://www.aucma.com.cn/", "tags": ["上市公司", "国企"], "keywords": ["设备", "制造"]},
    {"name": "青岛银行", "industry": "金融银行", "salary": "面议", "positions": "柜员/客户经理", "url": "https://www.qdbank.com/", "tags": ["上市银行", "国企"], "keywords": []},
    {"name": "赛轮集团", "industry": "轮胎", "salary": "面议", "positions": "生产/研发/设备", "url": "https://www.sailungroup.com/", "tags": ["上市公司", "海外"], "keywords": ["设备", "机械", "生产"]},
    {"name": "森麒麟", "industry": "轮胎", "salary": "面议", "positions": "技术/管理", "url": "https://www.netyre.com/", "tags": ["上市公司", "航空轮胎"], "keywords": ["设备", "技术"]},
    {"name": "山东省港口集团", "industry": "港口物流", "salary": "面议", "positions": "港务/物流/设备", "url": "https://www.sd-port.com/", "tags": ["国企", "世界级港口"], "keywords": ["设备", "机械"]},
    {"name": "青岛城投新能源", "industry": "新能源", "salary": "面议", "positions": "9个岗位", "url": "https://www.qdctne.com/", "tags": ["国企", "风电光伏"], "keywords": ["设备", "电气"]},
    {"name": "海发集团", "industry": "投资金融", "salary": "月薪17.7K", "positions": "30个岗位", "url": "https://www.qdgxjt.com/", "tags": ["国企", "投资"], "keywords": []},
    {"name": "兴航光电", "industry": "光电/半导体", "salary": "月薪17.6K", "positions": "25个岗位", "url": "https://www.qdgxjt.com/", "tags": ["研发", "光电"], "keywords": ["电子", "半导体", "光学"]},
    {"name": "鼎信通讯", "industry": "通信/芯片", "salary": "面议", "positions": "50+岗位", "url": "https://www.dingxin.com/", "tags": ["上市", "芯片", "通信"], "keywords": ["芯片", "电子", "工程师", "研发"]},
    {"name": "青岛光电半导体", "industry": "半导体/显示", "salary": "面议", "positions": "30+岗位", "url": "https://www.qdopto.com/", "tags": ["半导体", "显示面板"], "keywords": ["半导体", "电子", "设备", "调试"]},
    {"name": "歌尔微电子", "industry": "半导体/声学", "salary": "月薪20K+", "positions": "100+岗位", "url": "https://www.goertek.com/", "tags": ["上市", "半导体", "声学"], "keywords": ["半导体", "电子", "设备", "工程师"]},
    {"name": "青岛国信集团", "industry": "综合国企", "salary": "面议", "positions": "40+岗位", "url": "https://www.qdgxjt.com/", "tags": ["国企", "多产业"], "keywords": ["设备", "工程", "制造"]},
    {"name": "中石化青岛炼化", "industry": "石化/化工", "salary": "面议", "positions": "设备/技术", "url": "https://www.qlsh.com.cn/", "tags": ["央企", "石化"], "keywords": ["设备", "维护", "工程师"]},
    {"name": "崂山矿泉水", "industry": "饮品", "salary": "月薪7.8K", "positions": "6个岗位", "url": "https://www.lao-shan.com/", "tags": ["国企", "百年品牌"], "keywords": ["设备"]},
    {"name": "青岛旅游集团", "industry": "文旅", "salary": "月薪7.1K", "positions": "文旅/景区", "url": "https://www.qdtg.com/", "tags": ["国企", "旅游"], "keywords": []},
    {"name": "青岛航空", "industry": "航空货运", "salary": "月薪7.0K", "positions": "航空", "url": "https://www.qdairlines.com/", "tags": ["国企", "航空"], "keywords": []},
]

# ============ 用户简历画像（工程体系强化版）============
MY_PROFILE = {
    "name": "曹凤交",
    "position": "工业设备/系统工程师",
    "fields": ["半导体", "高端仪器", "工业检测系统"],
    "education": "南京农业大学（211），材料成型及控制工程，本科",
    "experience_years": "6年+",
    "companies": [
        "中国电子科技集团第55研究所（2018-2023）",
        "布鲁克北京（2023-2024）",
        "旭显未来（2023）",
        "明识智能科技（2025-至今）"
    ],
    "core_skills": [
        "设备全生命周期管理", "精度/稳定性/一致性工程", "系统集成",
        "FMEA/OCAP", "PM+PdM维护体系", "工程验证", "国产化替代",
        "半导体设备", "SMT设备", "XRD分析仪器", "激光拉曼检测",
        "光学/机械/电气/软件协同", "CAD/PRO/E/ANSYS",
        "安装调试", "性能验证", "技术文档", "英语可作为工作语言"
    ]
}

# 核心关键词（权重5）：直接对口的核心能力
CORE_KEYWORDS = [
    "设备", "半导体", "SMT", "XRD", "光学", "检测", "仪器", "拉曼",
    "系统集成", "工程师", "FMEA", "可靠性", "精度", "性能验证"
]

# 重要关键词（权重3）：相关经验和技术背景
IMPORTANT_KEYWORDS = [
    "机械", "制造", "电子", "自动化", "电气", "军工", "航天",
    "芯片", "集成电路", "调试", "安装", "技术支持", "维护",
    "工厂", "材料", "成型", "复合材料"
]

# 补充关键词（权重1）：通用技能
EXTRA_KEYWORDS = [
    "CAD", "PRO/E", "ANSYS", "维修", "生产", "研发", "技术"
]

def match_score(job):
    """多维度加权匹配岗位"""
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

    # 行业特别加分
    industry_bonus = {
        "半导体": 8, "芯片": 8, "集成电路": 8,
        "光电": 6, "光学": 6, "仪器": 6,
        "高端装备": 5, "工程机械": 4, "轨道交通装备": 4,
        "智能制造": 4, "AI": 3
    }
    for ind, bonus in industry_bonus.items():
        if ind in job["industry"]:
            score += bonus

    # 去重并返回结果
    match_reasons = list(dict.fromkeys(match_reasons))[:5]
    return score, match_reasons

def build_desp():
    """构建新闻资讯内容"""

    # ===== 今日要点速览 =====
    digest = (
        "• 博鳌亚洲论坛2026年年会即将举办\n"
        "• AI核心产业规模预计突破1.2万亿元\n"
        "• 油价进入9元时代，加满多花约80元\n"
        "• 山东省考面试进行中，多场考试即将到来"
    )

    # ===== 时政要闻 =====
    politics_lines = []
    for i, item in enumerate(politics_news):
        hot_tag = "🔥 " if item.get("hot") else ""
        politics_lines.append(f"`{i+1:02d}` {hot_tag}**{item['title']}**\n　　{item['desc']}")
    politics_str = "\n\n".join(politics_lines)

    # ===== 科技新闻 =====
    tech_lines = []
    for i, item in enumerate(tech_news):
        hot_tag = "🔥 " if item.get("hot") else ""
        tech_lines.append(f"`{i+1:02d}` {hot_tag}**{item['title']}**\n　　{item['desc']}")
    tech_str = "\n\n".join(tech_lines)

    # ===== 岗位匹配 =====
    scored_jobs = [(j, *match_score(j)) for j in all_jobs]
    scored_jobs.sort(key=lambda x: x[1], reverse=True)

    recommended = [(j, s, reasons) for j, s, reasons in scored_jobs if s >= 12]
    maybe = [(j, s, reasons) for j, s, reasons in scored_jobs if 5 <= s < 12]

    # 推荐岗位卡片
    rec_lines = []
    for j, s, reasons in recommended:
        tags = " · ".join(j['tags'][:3])
        match_pct = min(98, 65 + s * 2)
        reason_str = "、".join(reasons[:3]) if reasons else j['industry']
        rec_lines.append(
            f"✅ **[{j['name']}]({j['url']})**　`匹配{match_pct}%`\n"
            f"　　{j['industry']} | {j['salary']} | {j['positions']}\n"
            f"　　🎯 匹配原因：{reason_str}\n"
            f"　　📌 {tags}"
        )
    rec_str = "\n\n".join(rec_lines)

    # 备选岗位
    maybe_lines = []
    for j, s, reasons in maybe:
        reason_str = "、".join(reasons[:2]) if reasons else ""
        maybe_lines.append(
            f"🔹 **[{j['name']}]({j['url']})** `{j['salary']}` · {j['industry']}"
            + (f" · {reason_str}" if reason_str else "")
        )
    maybe_str = "\n".join(maybe_lines)

    # ===== 组装完整内容 =====
    desp = f"""# 📰 每日资讯简报
**{today} {weekday}**

> 📋 **今日要点**
{digest}

---
# 📡 全国资讯

## 🏛️ 时政要闻

{politics_str}

> 📌 来源：新华网 · 人民网 · 央视新闻

---

## 💻 科技前沿

{tech_str}

> 📌 来源：36氪 · 极客公园 · 科技日报

---
# 🏙️ 青岛生活

## ⛽ 今日油价

| 项目 | 价格 | 变动 |
|:----:|:----:|:----:|
| 92号汽油 | 约9.03元/升 | ↑1.73元 |
| 95号汽油 | 约9.68元/升 | ↑1.84元 |
| 0号柴油 | 约8.75元/升 | ↑1.76元 |

> 📌 3月23日24时调价 | 💡 加满50L多花约80元

---

## 📚 山东公务员 / 事业编

**2026年山东省考**　招录8332人 | 省属583人 | 公安955人

**近期招聘** 835+岗位更新中

🔗 [山东省考公告](http://www.shandong.gov.cn/art/2025/11/5/art_94237_10357496.html)
🔗 [事业编统考](https://sd.offcn.com/html/2026/01/583960.html)
🔗 [最新招聘汇总](https://sd.huatu.com/)

---

## 📺 青岛本地新闻

**🔷 政务**　青岛市召开2026年重点工作部署会议；多个区市发布民生实事清单

**🔷 经济**　青岛一季度经济运行稳中向好；多个重点项目集中开工

**🔷 民生**　新一批便民设施投入使用；城区多条道路优化改造完成

> 📌 来源：青岛日报 · 青岛政务网

---

## 🌤️ 青岛天气（未来3天）

| 日期 | 天气 | 温度 | 风力 | 穿衣 |
|:----:|:----:|:----:|:----:|:----:|
| 今日 | 🌥️ 多云转晴 | 7° ~ 12° | 3-4级 | 厚外套 |
| 明日 | ⛅ 晴转多云 | 8° ~ 14° | 3-4级 | 外套 |
| 后日 | 🌥️ 多云 | 9° ~ 13° | 4-5级 | 防风 |

> 📌 来源：中国天气网

---

## 🚇 出行路况

🚇 **地铁**　1/2/3/8号线正常运营，早晚高峰拥挤

🛣️ **高速**　胶州湾大桥/环湾大道/青银高速正常

⚠️ **拥堵**　早高峰 7:30-9:00 香港中路 · 晚高峰 17:30-19:00 胶州路/辽宁路

> 📌 来源：青岛交警

---

## 💡 民生公告

**💧 停水**　暂无计划　　**⚡ 停电**　暂无计划

> 📌 来源：青岛水务 · 国网青岛供电

---

## 🎭 周末文化活动

| 类型 | 活动 | 地点 |
|:----:|:----:|:----:|
| 🖼️ 展览 | 青岛国际当代艺术展 | 崂山美术馆 |
| 🎵 演出 | 青岛交响乐团音乐会 | 青岛大剧院 |
| 🎬 电影 | 多部新片热映中 | 各大影院 |
| 📚 讲座 | 名家读书分享会 | 青岛市图书馆 |

> 📌 来源：青岛文化云

---

## 📱 科技新品

- 📱 多款旗舰新机即将发布，折叠屏持续热销
- 💻 新一代轻薄本/平板集中上市
- 🚗 多款新能源车型密集发布，智能驾驶升级
- 🎮 新一代AR/VR设备看点十足

> 📌 来源：科技日报 · 爱范儿

---
# 📋 求职考试

## 📅 考试日历

| 考试 | 时间 | 状态 |
|:--------|:----:|:----:|
| 山东省考面试 | 3-4月 | 🔸进行中 |
| 研究生复试 | 3-4月 | 🔸进行中 |
| 事业单位统考 | 3月 | ✅已结束 |
| 教师资格证 | 5月中旬 | 📖备考 |
| 初级会计 | 5月中旬 | 📖备考 |
| 英语四六级 | 6月中旬 | 📖备考 |
| 法考客观题 | 9月中旬 | 📖备考 |
| 国考笔试 | 11月底 | 📖备考 |

> 📌 来源：山东人事考试网

---

## 💼 为你推荐（系统/设备工程师）

> 🎯 根据你的简历（6年+经验 | 半导体·高端仪器·工业检测 | CETC55所+布鲁克+明识智能）智能匹配
> 📋 核心能力：设备全生命周期管理 · 精度/稳定性工程 · 系统集成 · FMEA/OCAP · PM+PdM维护体系

**✅ 高度匹配**

{rec_str}

**🔸 可以关注**

{maybe_str}

🔗 更多：[智联招聘](https://www.zhaopin.com/qingdao/) · [BOSS直聘](https://www.zhipin.com/qingdao/)

---

> ⏰ {today} {weekday} ｜ 每日早上8:00自动推送
> 💬 如需调整推荐方向请回复"""

    return desp


def send_push(text, desp):
    """发送推送消息到Server酱（支持系统代理和直连）"""
    data = {
        "text": text,
        "desp": desp
    }

    url = f"https://sctapi.ftqq.com/{sendkey}.send"

    # 方法1: 使用 requests 直连（不使用代理）
    if HAS_REQUESTS:
        try:
            response = requests.post(url, json=data, timeout=30)
            if response.status_code == 200:
                print(f"推送成功: {response.text}")
                return True
        except Exception as e:
            print(f"requests 直连失败: {e}")

        # 方法2: 使用 requests + 系统代理
        try:
            proxies = urllib.request.getproxies()
            response = requests.post(url, json=data, proxies=proxies, timeout=30)
            if response.status_code == 200:
                print(f"推送成功: {response.text}")
                return True
        except Exception as e:
            print(f"requests 代理失败: {e}")

    # 方法3: 使用 urllib 直连
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = response.read().decode('utf-8')
            print(f"推送成功: {result}")
            return True
    except Exception as e:
        print(f"urllib 直连失败: {e}")

    # 方法4: 使用 urllib + 系统代理
    try:
        proxies = urllib.request.getproxies()
        proxy_handler = urllib.request.ProxyHandler(proxies)
        opener = urllib.request.build_opener(proxy_handler)
        with opener.open(req, timeout=30) as response:
            result = response.read().decode('utf-8')
            print(f"推送成功: {result}")
            return True
    except Exception as e:
        print(f"urllib 代理失败: {e}")

    return False


if __name__ == "__main__":
    desp = build_desp()
    send_push(text, desp)
