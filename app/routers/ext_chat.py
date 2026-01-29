import json
import asyncio
import time
import httpx
from typing import List, Optional
from fastapi import APIRouter, Header, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import logging
import os
from logging.handlers import RotatingFileHandler

from utils import random_chunk_split

# 创建日志目录
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置 logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 配置日志文件处理器
file_handler = RotatingFileHandler(
    os.path.join(log_dir, "ext_chat.log"),
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
    encoding="utf-8"
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

router = APIRouter(prefix="/knowledgeService", tags=["mock-chat"])

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    stream: bool = False
    agentId: str
    messages: List[Message]


@router.post("/extChatApi/v3/chat")
async def chat_completions(
    request: ChatRequest,
    raw_request: Request,
    app_id: Optional[str] = Header(None, alias="appId"),
    app_key: Optional[str] = Header(None, alias="appKey")
):
    body = await raw_request.body()
    logger.info(f"app_id: {app_id}, app_key: {app_key}, request: {body.decode('utf-8')}")
    async def event_generator():
        # 模拟响应内容片段
        content = '''
<div/>
<title> { "title": "五年以上变压器数量", "desc":"变电一所统计分析" } </title>

<ordermanager>{"sql":{"count":1,"data":[{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203},{"province_code":9,"total_count":4203}],"status":"success","type":"query"}}</ordermanager>

<ordermanager >{"sql":{"count":1,"data":[{ "province_code_1": 9, "total_count_1": 4203, "test_1": 1, "province_code_2": 12, "total_count_2": 3150, "test_2": 2, "province_code_3": 5, "total_count_3": 2789, "test_3": 3, "province_code_4": 18, "total_count_4": 5620, "test_4": 4, "province_code_5": 21, "total_count_5": 1987, "test_5": 5, "province_code_6": 7, "total_count_6": 4432, "test_6": 6, "province_code_7": 15, "total_count_7": 3675, "test_7": 7, "province_code_8": 3, "total_count_8": 1540, "test_8": 8, "province_code_9": 27, "total_count_9": 6891, "test_9": 9, "province_code_10": 11, "total_count_10": 2345, "test_10": 10}],"status":"success","type":"query"}}</ordermanager>

**饼图 - Pie Chart**

<chart> { "type": "pie", "data": [ { "category": "火锅", "value": 22 }, { "category": "自助餐", "value": 12 }, { "category": "小吃快餐", "value": 8 }, { "category": "西餐", "value": 6 }, { "category": "其它", "value": 44 } ], "title": "餐饮业营收额占比" } </chart>

**词云图 - WordCloud Chart.**


<chart>{ "type": "word-cloud", "data": [ { "text": "环境", "value": 20 }, { "text": "保护", "value": 15 }, { "text": "可持续发展", "value": 10 } ] }</chart>

**组织架构图 - Organization Chart.**


<chart>{ "type": "organization-chart", "data": { "name": "Alice Johnson", "description": "Chief Technology Officer", "children": [ { "name": "Bob Smith", "description": "Senior Software Engineer", "children": [ { "name": "Charlie Brown", "description": "Software Engineer" }, { "name": "Diana White", "description": "Software Engineer" } ] }, { "name": "Eve Black", "description": "IT Support Department Head", "children": [ { "name": "Frank Green", "description": "IT Support Specialist" }, { "name": "Grace Blue", "description": "IT Support Specialist" } ] } ] } }</chart>

**柱形图 - Column Chart**


<chart>{ "type": "column", "data": [ { "category": "2015 年", "value": 80 }, { "category": "2016 年", "value": 140 }, { "category": "2017 年", "value": 220 } ], "title": "海底捞公司外卖收入", "axisXTitle": "年份", "axisYTitle": "金额 （百万元）" }</chart>

**直方图 - Histogram Chart**


<chart>{ "type": "histogram", "data": [78, 88, 60, 100, 95], "binNumber": 5, "title": "成绩分布" }</chart>

**折线图 - Line Chart**


<chart>{ "type": "line", "data": [ { "time": "2015 年", "value": 1700 }, { "time": "2016 年", "value": 1500 }, { "time": "2017 年", "value": 1200 } ], "title": "出生人口变化", "axisXTitle": "年份", "axisYTitle": "出生人口（万人）" }</chart>

**鱼骨图 - Fishbone Diagram**


<chart>{ "type": "fishbone-diagram", "data": { "name": "产品销量下降", "children": [ { "name": "市场推广", "children": [{ "name": "广告投入减少" }, { "name": "促销活动不足" }] }, { "name": "产品质量", "children": [{ "name": "产品缺陷" }, { "name": "品质不稳定" }] }, { "name": "客户服务", "children": [{ "name": "响应速度慢" }, { "name": "服务态度差" }] }, { "name": "价格策略", "children": [{ "name": "定价过高" }, { "name": "竞争对手降价" }] } ] } }</chart>

**小提琴图 - Violin Chart**


<chart>{ "type": "violin", "data": [ { "category": "班级A", "value": 15 }, { "category": "班级A", "value": 18 }, { "category": "班级A", "value": 22 }, { "category": "班级A", "value": 27 }, { "category": "班级A", "value": 35 }, { "category": "班级B", "value": 10 }, { "category": "班级B", "value": 14 }, { "category": "班级B", "value": 19 }, { "category": "班级B", "value": 23 }, { "category": "班级B", "value": 30 } ], "title": "成绩分布" }</chart>

**箱线图 - Boxplot**


<chart>{ "type": "boxplot", "data": [ { "category": "班级A", "value": 15 }, { "category": "班级A", "value": 18 }, { "category": "班级A", "value": 22 }, { "category": "班级A", "value": 27 }, { "category": "班级A", "value": 35 }, { "category": "班级B", "value": 10 }, { "category": "班级B", "value": 14 }, { "category": "班级B", "value": 19 }, { "category": "班级B", "value": 23 }, { "category": "班级B", "value": 30 } ], "title": "成绩分布" }</chart>

**韦恩图 - Venn Chart**


<chart> { "type": "venn", "data": [ { "sets": ["A"], "value": 20, "label": "集合A" }, { "sets": ["B"], "value": 15, "label": "集合B" }, { "sets": ["A", "B"], "value": 5, "label": "交集AB" } ], "title": "集合交集示例" } </chart>

**网络图 - Network Graph**


<chart>{ "type": "network-graph", "data": { "nodes": [ { "name": "哈利·波特" }, { "name": "赫敏·格兰杰" }, { "name": "罗恩·韦斯莱" }, { "name": "伏地魔" } ], "edges": [ { "source": "哈利·波特", "target": "赫敏·格兰杰", "name": "朋友" }, { "source": "哈利·波特", "target": "罗恩·韦斯莱", "name": "朋友" }, { "source": "哈利·波特", "target": "伏地魔", "name": "敌人" }, { "source": "伏地魔", "target": "哈利·波特", "name": "试图杀死" } ] } }</chart>

**条形图 - Bar Chart**


<chart>{ "type": "bar", "data": [ { "category": "2015 年", "value": 80 }, { "category": "2016 年", "value": 140 }, { "category": "2017 年", "value": 220 } ], "title": "海底捞公司外卖收入", "axisXTitle": "年份", "axisYTitle": "金额 （百万元）" }</chart>

**思维导图 - Mind Map**


<chart>{ "type": "mind-map", "data": { "name": "项目计划", "children": [ { "name": "研究阶段", "children": [{ "name": "市场调研" }, { "name": "技术可行性分析" }] }, { "name": "设计阶段", "children": [{ "name": "产品功能确定" }, { "name": "UI 设计" }] }, { "name": "开发阶段", "children": [{ "name": "编写代码" }, { "name": "单元测试" }] }, { "id": "测试阶段", "children": [{ "name": "功能测试" }, { "name": "性能测试" }] } ] } }</chart>

**水波图 - Liquid Chart**


<chart>{ "type": "liquid", "percent": 0.75, "title": "任务完成度" }</chart>

**双轴图 - DualAxes Chart**


<chart>{ "type": "dual-axes", "categories": ["2018", "2019", "2020", "2021", "2022"], "title": "2018-2022销售额与利润率", "axisXTitle": "年份", "series": [ { "type": "column", "data": [91.9, 99.1, 101.6, 114.4, 121], "axisYTitle": "销售额" }, { "type": "line", "data": [0.055, 0.06, 0.062, 0.07, 0.075], "axisYTitle": "利润率" } ] }</chart>

**数据文本 - Vis Text**


<chart><vis-text type="time_desc">2023 年 1 月 1 日</vis-text>，<vis-text type="metric_name">支付宝交易量</vis-text>为<vis-text type="metric_value">100 万</vis-text>，环比上涨<vis-text type="delta_value_pos">3000<vis-text>，同比去年上涨<vis-text type="radio_value_pos">10%<vis-text></chart>

**桑基图 - Sankey Chart**


<chart>{ "type": "sankey", "data": [ { "source": "煤炭", "target": "发电厂", "value": 120 }, { "source": "天然气", "target": "发电厂", "value": 80 }, { "source": "发电厂", "target": "工业", "value": 100 }, { "source": "发电厂", "target": "居民", "value": 60 }, { "source": "发电厂", "target": "商业", "value": 40 } ], "nodeAlign": "justify", "title": "能源流动关系" }}</chart>

**散点图 - Scatter Chart**


<chart>{ "type": "scatter", "data": [ { "x": 10, "y": 15 }, { "x": 20, "y": 25 }, { "x": 30, "y": 35 }, { "x": 40, "y": 45 } ] }</chart>


**瀑布图 - Waterfall Chart**


<chart>{ "type": "waterfall", "data": [ { "category": "期初利润", "value": 100 }, { "category": "销售收入", "value": 80 }, { "category": "运营成本", "value": -50 }, { "category": "税费", "value": -20 }, { "category": "总计", "isTotal": true } ] }</chart>

**面积图 - Area Chart**


<chart>{ "type": "area", "data": [ { "time": "1 月", "value": 23.895 }, { "time": "2 月", "value": 23.695 }, { "time": "3 月", "value": 23.655 } ], "title": "1月到3月股票价格的变化", "axisXTitle": "月份", "axisYTitle": "价格" }</chart>

**漏斗图 - FunnelChart**


<chart>{ "type": "funnel", "data": [ { "category": "访问", "value": 1000 }, { "category": "咨询", "value": 600 }, { "category": "下单", "value": 300 }, { "category": "成交", "value": 120 } ], "title": "销售漏斗" }</chart>

**流程图 - Flow Diagram**


<chart>{ "type": "flow-diagram", "data": { "nodes": [ { "name": "访问注册页面" }, { "name": "填写并提交注册表单" }, { "name": "验证用户信息" }, { "name": "创建新用户账户" }, { "name": "提示修改错误信息" }, { "name": "发送验证邮件" }, { "name": "点击验证链接" }, { "name": "注册成功，跳转到登录页面" } ], "edges": [ { "source": "访问注册页面", "target": "填写并提交注册表单" }, { "source": "填写并提交注册表单", "target": "验证用户信息" }, { "source": "验证用户信息", "target": "创建新用户账户", "name": "信息无误" }, { "source": "验证用户信息", "target": "提示修改错误信息", "name": "信息有误" }, { "source": "创建新用户账户", "target": "发送验证邮件" }, { "source": "发送验证邮件", "target": "点击验证链接" }, { "source": "点击验证链接", "target": "注册成功，跳转到登录页面" } ] } }</chart>

**雷达图 - Radar Chart**


<chart>{ "type": "radar", "data": [ { "name": "沟通能力", "value": 2 }, { "name": "协作能力", "value": 3 }, { "name": "领导能力", "value": 2 }, { "name": "学习能力", "value": 5 }, { "name": "创新能力", "value": 6 }, { "name": "技术能力", "value": 9 } ] }</chart>

**矩阵树图 -Treemap Chart**


<chart>{ "type": "treemap", "data": [ { "name": "A", "value": 100, "children": [ { "name": "A1", "value": 40 }, { "name": "A2", "value": 30 }, { "name": "A3", "value": 30 } ] }, { "name": "B", "value": 80, "children": [ { "name": "B1", "value": 50 }, { "name": "B2", "value": 30 } ] } ] }</chart>






<think>
基于用户提供的业务需求，我们需要创建一个完整的销售管理系统示例，该系统需要展示如何从AI模型返回的数据中动态获取和展示信息。这个示例将展示XMarkdown如何：
1. 从模型返回的JSON数据中解析业务信息
2. 使用小写组件标签（如salesdashboard）
3. 处理动态数据渲染
4. 实现复杂的业务场景和交互需求
通过这种方式，用户可以清楚地看到XMarkdown不仅支持简单的文本渲染，还能处理动态数据驱动的复杂业务场景。
</think>

### 📊 动态销售仪表板

<salesdashboard>{"sales":[{"name":"销售量","value":52000,"color":"#3b82f6"},{"name":"总量","value":38000,"color":"#8b5cf6"}],"totalSales":141000,"totalOrders":487,"newCustomers":94}</salesdashboard>


## 订单数据分析报告（变电一所 — 油浸式变压器）

### 一、总体情况概述
本数据共包含 **5 条订单记录**，客户均为“变电一所”，产品类型统一为“油浸式变压器”，时间跨度为 **2015 年至 2019 年**，地区均为 **北京**，具有较强的集中性和可比性。

---

### 二、订单金额分析
| 订单号 | 金额（元） | 状态 |
|--------|------------|------|
| TR001  | 10000      | 已完成 |
| TR002  | 8000       | 已完成 |
| TR003  | 6300       | 已完成 |
| TR004  | 10000      | 处理中 |
| TR005  | 40000      | 已完成 |

- 总订单金额：**¥74,300**
- 已完成订单金额：**¥64,300**
- 最大单笔金额：**¥40,000（2015年）**
- 最小单笔金额：**¥6,300（2016年）**
- 平均订单金额：约 **¥14,860**

分析可见：
- 2015 年存在一笔大额采购，拉高整体金额水平；
- 2016–2018 年订单金额趋于中低水平；
- 2019 年金额回升，但仍处于处理中状态。

---

### 三、时间趋势分析
按时间顺序排列：

| 年份 | 订单数量 | 金额合计 |
|------|----------|----------|
| 2015 | 1        | 40000    |
| 2016 | 1        | 6300     |
| 2017 | 1        | 8000     |
| 2018 | 1        | 10000    |
| 2019 | 1        | 10000    |

趋势特点：
- 每年均有订单，说明合作关系较为稳定；
- 2015 年为采购高峰期；
- 2016 年后采购规模明显缩小；
- 近几年维持在 8000–10000 元区间，表现为常规补充采购。

---

### 四、订单状态分析
| 状态   | 数量 | 占比 |
|--------|------|------|
| 已完成 | 4    | 80%  |
| 处理中 | 1    | 20%  |

- 已完成率较高（80%），说明履约情况良好；
- 仅有一笔 2019 年订单仍在处理中，需重点跟进，防止影响客户满意度。

---

### 五、客户与区域特征分析
- 客户：全部来自 **变电一所**
- 地区：全部为 **北京**

说明：
- 该数据反映的是单一核心客户的采购情况；
- 客户集中度高，存在一定依赖风险；
- 尚未体现跨区域或多客户拓展能力。

---

### 六、综合评价与建议

#### 1. 综合评价
- 客户关系稳定，连续多年保持合作；
- 订单完成率高，履约能力较强；
- 采购规模呈“高峰后趋稳”特征；
- 客户和地区结构较为单一。

#### 2. 优化建议
- 持续跟进未完成订单，缩短处理周期；
- 深挖客户需求，争取恢复大额订单规模；
- 拓展新客户与新区域，降低集中风险；
- 分析2015年大额订单背景，复制成功经验。

---

### 七、结论
该订单数据表明，变电一所与供应方保持了长期稳定合作关系，但近年来采购规模趋于保守。未来应在保持现有客户稳定性的基础上，加强业务拓展与客户结构优化，以提升整体经营稳定性和增长潜力。


'''
        chunks = random_chunk_split(content, 100, 200)
        timestamp = int(time.time() * 1000)
        base_id = str(timestamp)
        
        current_content = ""
        for i, chunk in enumerate(chunks):
            current_content += chunk
            # 每次生成新的时间戳模拟真实感，或者保持一致，看用户示例似乎时间戳在变
            # 示例: 1768536414436 -> 1768536414538 -> ...
            current_timestamp = int(time.time() * 1000)
            
            data = {
                "created": current_timestamp,
                "model": "",
                "id": str(current_timestamp),
                "choices": [
                    {
                        "finish_reason": None,
                        "delta": {
                            "role": "assistant",
                            "content": current_content
                        }
                    }
                ],
                "object": "chat.completion.chunk"
            }
            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
            await asyncio.sleep(0.3) # 模拟处理延迟

        # 发送结束标记
        yield "data: [DONE]\n\n"
    print("输出")
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/extChatApi/v3/chat/real")
async def chat_completions_real(
    request: ChatRequest,
    raw_request: Request,
    app_id: Optional[str] = Header(None, alias="appId"),
    app_key: Optional[str] = Header(None, alias="appKey")
):
    body = await raw_request.body()
    logger.info(f"Real Chat - app_id: {app_id}, app_key: {app_key}, request: {body.decode('utf-8')}")

    # Coze Configuration
    COZE_API_TOKEN = "pat_b9214c6c6d5f00473130b4e6f38fb7eca18d242caa7eee352178a398c80977ad"
    COZE_BOT_ID = "7598459664958750720"
    
    # COZE_BOT_ID = "7597694170307756032"
    COZE_BASE_URL = "http://192.168.124.8:18888"

    # Extract user query
    query = '''
[
    { "类别": "火锅", "营收额占比(%)": 22 },
    { "类别": "自助餐", "营收额占比(%)": 12 },
    { "类别": "小吃快餐", "营收额占比(%)": 8 },
    { "类别": "西餐", "营收额占比(%)": 6 },
    { "类别": "其它", "营收额占比(%)": 44 }
  ]
'''
    for msg in reversed(request.messages):
        if msg.role == "user":
            query = msg.content
            break

    async def event_generator():
        url = f"{COZE_BASE_URL}/v3/chat"
        headers = {
            "Authorization": f"Bearer {COZE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "bot_id": COZE_BOT_ID,
            "user_id": "user_default",
            "stream": True,
            "auto_save_history": True,
            "additional_messages": [
                {
                    "role": "user",
                    "content": query,
                    "content_type": "text"
                }
            ]
        }

        current_content = ""
        
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", url, headers=headers, json=payload, timeout=120.0) as response:
                    if response.status_code != 200:
                        error_msg = f"Coze API Error: {response.status_code}"
                        yield f"data: {json.dumps({'error': error_msg}, ensure_ascii=False)}\n\n"
                        return

                    event_type = None
                    async for line in response.aiter_lines():
                        line = line.strip()
                        if not line:
                            continue
                        
                        logger.info(f"Coze Stream Line: {line}")
                        
                        if line.startswith("event:"):
                            event_type = line[6:].strip()
                        elif line.startswith("data:"):
                            data_str = line[5:].strip()
                            
                            if event_type == "conversation.message.delta":
                                try:
                                    data = json.loads(data_str)
                                    content = data.get("content", "")
                                    if content:
                                        current_content += content
                                        
                                        current_timestamp = int(time.time() * 1000)
                                        resp_data = {
                                            "created": current_timestamp,
                                            "model": "coze-bot",
                                            "id": str(current_timestamp),
                                            "choices": [
                                                {
                                                    "finish_reason": None,
                                                    "delta": {
                                                        "role": "assistant",
                                                        "content": current_content
                                                    }
                                                }
                                            ],
                                            "object": "chat.completion.chunk"
                                        }
                                        yield f"data: {json.dumps(resp_data, ensure_ascii=False)}\n\n"
                                except json.JSONDecodeError:
                                    continue
                            elif event_type == "error":
                                logger.error(f"Coze Error Event: {data_str}")
                                try:
                                    data = json.loads(data_str)
                                    error_msg = data.get("msg", "Unknown Coze Error")
                                    yield f"data: {json.dumps({'error': error_msg}, ensure_ascii=False)}\n\n"
                                except:
                                    yield f"data: {json.dumps({'error': data_str}, ensure_ascii=False)}\n\n"
            except Exception as e:
                logger.error(f"Stream error: {e}")
                yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
