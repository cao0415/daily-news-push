#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刘林洁 - 每日岗位推荐推送
根据简历画像：行政/人事/综合管理方向
定时任务：每天早上9点执行
"""

import json
import urllib.request
import datetime
import os

# 从环境变量读取 sendkey
sendkey = os.environ.get('SENDKEY_LIU', 'SCT328749Tq5FhB6vfacEnARlew7tLbOPx')
today = datetime.datetime.now().strftime("%Y年%m月%d日")
weekday_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
weekday = weekday_list[datetime.datetime.now().weekday()]
text = f"💼 每日岗位推荐 | {today} {weekday}"

# ============ 刘林洁简历画像 ============
MY_PROFILE = {
    "name": "刘林洁",
    "gender": "女",
    "birth": "1997.7",
    "political": "中共党员",
    "position": "行政/人事/综合管理",
    "location": "青岛",
    "address": "水清沟三小区（市北区乐安路）",
    "education": "鲁东大学，广播电视编导，本科（2017-2021）",
    "experience_years": "3年+",
    "companies": [
        "青岛大地新能源研究院（2021.6-2024.12）综合行政",
        "明识（青岛）智能科技有限公司（2025.4-至今）综合管理"
    ],
    "core_skills": [
        "人事招聘", "员工入职离职管理", "考勤门禁管理",
        "社保公积金操作", "薪资发放", "出纳财务",
        "行政统筹", "采购管理", "会议组织", "文档管理",
        "公众号运营", "团建策划", "项目申报协助",
        "英语四级", "计算机二级", "C1驾照"
    ],
    "preferences": {
        "work_schedule": "双休",
        "benefits": "五险一金",
        "location": "离家近，市北区水清沟附近优先"
    }
}

# 核心关键词（权重5）
CORE_KEYWORDS = [
    "人事", "行政", "HR", "招聘", "综合管理", "出纳", "财务",
    "社保", "公积金", "考勤", "文员", "助理", "前台"
]

# 重要关键词（权重3）
IMPORTANT_KEYWORDS = [
    "办公室", "文秘", "档案", "会议", "接待", "采购",
    "后勤", "运营", "党建", "工会", "企业文化"
]

# 补充关键词（权重1）
EXTRA_KEYWORDS = [
    "管理", "协调", "沟通", "文档", "表格", "统计"
]

# ============ 青岛地区行政人事岗位（标注福利和距离） ============
all_jobs = [
    # 市北区附近（水清沟周边）
    {"name": "青岛啤酒", "industry": "食品饮料/国企", "salary": "月薪6-10K", "positions": "行政/人事", "url": "https://www.tsingtao.com.cn/", "tags": ["国企", "双休", "五险一金", "市北近"], "keywords": ["行政", "人事", "综合管理"], "distance": "近", "welfare": ["双休", "五险一金"]},
    {"name": "青岛地铁集团", "industry": "轨道交通/国企", "salary": "月薪5-10K", "positions": "行政/综合", "url": "https://www.qd-metro.com/", "tags": ["国企", "双休", "五险一金", "稳定"], "keywords": ["行政", "综合", "文秘"], "distance": "中", "welfare": ["双休", "五险一金"]},
    {"name": "青岛银行", "industry": "金融/上市银行", "salary": "月薪5-8K", "positions": "行政/文秘", "url": "https://www.qdbank.com/", "tags": ["上市银行", "双休", "五险一金"], "keywords": ["行政", "文秘", "综合"], "distance": "中", "welfare": ["双休", "五险一金"]},
    {"name": "青岛出版集团", "industry": "文化传媒/国企", "salary": "月薪5-8K", "positions": "行政/编辑助理", "url": "http://www.qdpub.com/", "tags": ["国企", "双休", "市北近"], "keywords": ["行政", "文秘", "编辑"], "distance": "近", "welfare": ["双休", "五险一金"]},
    {"name": "青岛市北区政府", "industry": "政府机关", "salary": "事业编待遇", "positions": "行政/文员", "url": "http://www.qingdaoshibei.gov.cn/", "tags": ["事业编", "双休", "市北"], "keywords": ["行政", "文员"], "distance": "近", "welfare": ["双休", "五险一金"]},
    {"name": "青岛日报报业集团", "industry": "传媒/国企", "salary": "月薪5-8K", "positions": "行政/新媒体", "url": "http://www.qingdaonews.com/", "tags": ["国企", "双休", "市北近"], "keywords": ["行政", "新媒体", "运营"], "distance": "近", "welfare": ["双休", "五险一金"]},
    {"name": "青岛饮料集团", "industry": "食品饮料/国企", "salary": "月薪5-8K", "positions": "行政/综合", "url": "http://www.qdyljt.com/", "tags": ["国企", "双休", "市北近"], "keywords": ["行政", "综合"], "distance": "近", "welfare": ["双休", "五险一金"]},
    
    # 其他区域
    {"name": "海尔集团", "industry": "家电/世界500强", "salary": "面议", "positions": "行政/人事/综合", "url": "https://www.haier.cn/", "tags": ["世界500强", "大平台", "双休"], "keywords": ["人事", "行政", "综合管理"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "海信集团", "industry": "家电/上市公司", "salary": "面议", "positions": "HR/行政", "url": "https://jobs.hisense.com/", "tags": ["上市公司", "股权激励", "双休"], "keywords": ["人事", "HR", "行政"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "青岛港集团", "industry": "港口物流/国企", "salary": "面议", "positions": "行政/综合", "url": "https://www.qdport.com/", "tags": ["国企", "世界级港口", "双休"], "keywords": ["行政", "综合管理"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "青岛城投集团", "industry": "投资/国企", "salary": "月薪6-12K", "positions": "行政/人事", "url": "https://www.qdctjt.com/", "tags": ["国企", "大平台", "双休"], "keywords": ["行政", "人事", "综合管理"], "distance": "中", "welfare": ["双休", "五险一金"]},
    {"name": "青岛国信集团", "industry": "综合国企", "salary": "月薪6-10K", "positions": "行政/人事", "url": "https://www.qdgxjt.com/", "tags": ["国企", "多产业", "双休"], "keywords": ["行政", "人事", "综合管理"], "distance": "中", "welfare": ["双休", "五险一金"]},
    {"name": "中车青岛四方", "industry": "轨道交通/央企", "salary": "月薪5-9K", "positions": "行政/综合", "url": "https://www.crrcgc.cc/", "tags": ["央企", "事业编", "双休"], "keywords": ["行政", "综合", "文秘"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "青岛能源集团", "industry": "能源/国企", "salary": "月薪5-8K", "positions": "行政/人事", "url": "http://www.qdnyjt.com/", "tags": ["国企", "能源", "双休"], "keywords": ["行政", "人事"], "distance": "中", "welfare": ["双休", "五险一金"]},
    {"name": "青岛华通集团", "industry": "投资/国企", "salary": "月薪6-10K", "positions": "行政/综合", "url": "http://www.qdhtjt.com/", "tags": ["国企", "投资", "双休"], "keywords": ["行政", "综合"], "distance": "中", "welfare": ["双休", "五险一金"]},
    {"name": "青岛旅游集团", "industry": "文旅/国企", "salary": "月薪4-7K", "positions": "行政/综合", "url": "https://www.qdtg.com/", "tags": ["国企", "旅游", "双休"], "keywords": ["行政", "综合", "文秘"], "distance": "中", "welfare": ["双休", "五险一金"]},
    {"name": "青岛航空", "industry": "航空/国企", "salary": "月薪5-8K", "positions": "行政/人事", "url": "https://www.qdairlines.com/", "tags": ["国企", "航空", "双休"], "keywords": ["行政", "人事"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "澳柯玛集团", "industry": "家电/上市公司", "salary": "月薪5-8K", "positions": "行政/人事", "url": "https://www.aucma.com.cn/", "tags": ["上市公司", "国企", "双休"], "keywords": ["行政", "人事"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "双星集团", "industry": "轮胎/上市公司", "salary": "月薪5-8K", "positions": "行政/综合", "url": "https://www.double-star.com/", "tags": ["上市公司", "机器人", "双休"], "keywords": ["行政", "综合"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "赛轮集团", "industry": "轮胎/上市公司", "salary": "月薪5-9K", "positions": "行政/人事", "url": "https://www.sailungroup.com/", "tags": ["上市公司", "海外", "双休"], "keywords": ["行政", "人事"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "软控股份", "industry": "智能制造/上市公司", "salary": "月薪6-10K", "positions": "行政/HR", "url": "http://www.mesnac.com/", "tags": ["上市公司", "智能制造", "双休"], "keywords": ["行政", "HR", "人事"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "特锐德", "industry": "新能源/上市公司", "salary": "月薪6-10K", "positions": "行政/人事", "url": "http://www.tgood.cn/", "tags": ["上市公司", "新能源", "双休"], "keywords": ["行政", "人事"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "鼎信通讯", "industry": "通信/上市公司", "salary": "月薪6-10K", "positions": "行政/人事", "url": "https://www.dingxin.com/", "tags": ["上市公司", "通信", "双休"], "keywords": ["行政", "人事"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "歌尔股份", "industry": "电子/上市公司", "salary": "月薪6-12K", "positions": "行政/HR", "url": "https://www.goertek.com/", "tags": ["上市公司", "电子", "双休"], "keywords": ["行政", "HR", "人事"], "distance": "远", "welfare": ["双休", "五险一金"]},
    {"name": "青岛高新区管委会", "industry": "政府机关", "salary": "事业编待遇", "positions": "行政/文秘", "url": "http://www.qdgxq.gov.cn/", "tags": ["事业编", "政府", "双休"], "keywords": ["行政", "文秘", "综合"], "distance": "远", "welfare": ["双休", "五险一金"]},
]

def match_score(job):
    """多维度加权匹配岗位（含距离和福利偏好）"""
    score = 0
    match_reasons = []
    job_keywords = set(job.get("keywords", []))
    job_text = job["name"] + job["industry"] + " ".join(job["tags"])

    # 核心技能匹配
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

    # 国企/上市公司加分
    if "国企" in job["tags"]:
        score += 3
        match_reasons.append("国企")
    if "上市公司" in job["tags"]:
        score += 2
        match_reasons.append("上市公司")

    # 距离加分（市北区水清沟附近优先）
    distance = job.get("distance", "中")
    if distance == "近":
        score += 5
        match_reasons.append("📍市北近")
    elif distance == "中":
        score += 2
        match_reasons.append("📍距离适中")

    # 福利加分（双休+五险一金）
    welfare = job.get("welfare", [])
    if "双休" in welfare:
        score += 2
        match_reasons.append("双休")
    if "五险一金" in welfare:
        score += 2
        match_reasons.append("五险一金")

    match_reasons = list(dict.fromkeys(match_reasons))[:5]
    return score, match_reasons

def build_desp():
    """构建岗位推荐内容"""

    # ===== 岗位匹配 =====
    scored_jobs = [(j, *match_score(j)) for j in all_jobs]
    scored_jobs.sort(key=lambda x: x[1], reverse=True)

    recommended = [(j, s, reasons) for j, s, reasons in scored_jobs if s >= 10]
    maybe = [(j, s, reasons) for j, s, reasons in scored_jobs if 5 <= s < 10]

    # 推荐岗位卡片
    rec_lines = []
    for j, s, reasons in recommended[:8]:  # 最多显示8个
        tags = " · ".join(j['tags'][:3])
        match_pct = min(98, 60 + s * 2)
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
    for j, s, reasons in maybe[:5]:  # 最多显示5个
        reason_str = "、".join(reasons[:2]) if reasons else ""
        maybe_lines.append(
            f"🔹 **[{j['name']}]({j['url']})** `{j['salary']}` · {j['industry']}"
            + (f" · {reason_str}" if reason_str else "")
        )
    maybe_str = "\n".join(maybe_lines)

    # ===== 组装完整内容 =====
    desp = f"""# 💼 每日岗位推荐

> 🎯 为 **刘林洁** 定制推荐（行政/人事/综合管理方向）
> 📋 简历画像：鲁东大学·广播电视编导 | 3年+综合行政经验 | 中共党员 | 英语四级·计算机二级·C1驾照
> 💡 核心能力：人事招聘·社保公积金·行政统筹·财务出纳·公众号运营·项目申报
> 🏠 工作偏好：**双休** · **五险一金** · **离家近**（水清沟三小区/市北区乐安路）

---

## ⭐ 高度匹配岗位（近+双休+五险一金）

{rec_str}

---

## 🔸 可以关注

{maybe_str}

---

## 📚 求职资源

🔗 [智联招聘-青岛行政](https://www.zhaopin.com/qingdao/) · [BOSS直聘-青岛人事](https://www.zhipin.com/qingdao/) · [前程无忧](https://www.51job.com/qingdao/)

🔗 [青岛人才网](http://rc.qingdao.gov.cn/) · [山东人事考试网](http://www.rsks.sd.gov.cn/)

---

> ⏰ {today} {weekday} ｜ 每日早上9:00自动推送
> 💬 如需调整推荐方向请联系"""

    return desp

def send_push(text, desp):
    """发送推送消息到Server酱"""
    data = {
        "text": text,
        "desp": desp
    }

    json_data = json.dumps(data).encode('utf-8')

    url = f"https://sctapi.ftqq.com/{sendkey}.send"
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={
            'Content-Type': 'application/json; charset=utf-8'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print(f"推送成功: {result}")
            return True
    except Exception as e:
        print(f"推送失败: {e}")
        return False

if __name__ == "__main__":
    desp = build_desp()
    send_push(text, desp)
