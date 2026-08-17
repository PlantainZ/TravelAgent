"""多智能体旅行规划系统"""

import json
from typing import Dict, Any, List
# jlq_rpc # =====================================

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
import asyncio

# jlq_crt # =====================================
# from hello_agents.tools import MCPTool
from tools.builtin.protocol_tools import MCPTool

from backend.app.models.schemas import TripRequest, TripPlan, DayPlan, Attraction, Meal, WeatherInfo, Location, Hotel
from backend.app.config import get_settings

from dotenv import load_dotenv
import os

load_dotenv()

# ============ Agent提示词 ============

ATTRACTION_AGENT_PROMPT = """你是景点搜索专家。你的任务是根据城市和用户偏好搜索合适的景点。

**重要提示:**
你必须使用工具来搜索景点!不要自己编造景点信息!

**工具调用格式:**
使用maps_text_search工具时,必须严格按照以下格式:
`[TOOL_CALL:amap_maps_text_search:keywords=景点关键词,city=城市名]`

**示例:**
用户: "搜索北京的历史文化景点"
你的回复: [TOOL_CALL:amap_maps_text_search:keywords=历史文化,city=北京]

用户: "搜索上海的公园"
你的回复: [TOOL_CALL:amap_maps_text_search:keywords=公园,city=上海]

**注意:**
1. 必须使用工具,不要直接回答
2. 格式必须完全正确,包括方括号和冒号
3. 参数用逗号分隔
"""

WEATHER_AGENT_PROMPT = """你是天气查询专家。你的任务是查询指定城市的天气信息。

**重要提示:**
你必须使用工具来查询天气!不要自己编造天气信息!

**工具调用格式:**
使用maps_weather工具时,必须严格按照以下格式:
`[TOOL_CALL:amap_maps_weather:city=城市名]`

**示例:**
用户: "查询北京天气"
你的回复: [TOOL_CALL:amap_maps_weather:city=北京]

用户: "上海的天气怎么样"
你的回复: [TOOL_CALL:amap_maps_weather:city=上海]

**注意:**
1. 必须使用工具,不要直接回答
2. 格式必须完全正确,包括方括号和冒号
"""

HOTEL_AGENT_PROMPT = """你是酒店推荐专家。你的任务是根据城市和景点位置推荐合适的酒店。

**重要提示:**
你必须使用工具来搜索酒店!不要自己编造酒店信息!

**工具调用格式:**
使用maps_text_search工具搜索酒店时,必须严格按照以下格式:
`[TOOL_CALL:amap_maps_text_search:keywords=酒店,city=城市名]`

**示例:**
用户: "搜索北京的酒店"
你的回复: [TOOL_CALL:amap_maps_text_search:keywords=酒店,city=北京]

**注意:**
1. 必须使用工具,不要直接回答
2. 格式必须完全正确,包括方括号和冒号
3. 关键词使用"酒店"或"宾馆"
"""

PLANNER_AGENT_PROMPT = """你是行程规划专家。你的任务是根据景点信息和天气信息,生成详细的旅行计划。

请严格按照以下JSON格式返回旅行计划:
```json
{
  "city": "城市名称",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "days": [
    {
      "date": "YYYY-MM-DD",
      "day_index": 0,
      "description": "第1天行程概述",
      "transportation": "交通方式",
      "accommodation": "住宿类型",
      "hotel": {
        "name": "酒店名称",
        "address": "酒店地址",
        "location": {"longitude": 116.397128, "latitude": 39.916527},
        "price_range": "300-500元",
        "rating": "4.5",
        "distance": "距离景点2公里",
        "type": "经济型酒店",
        "estimated_cost": 400
      },
      "attractions": [
        {
          "name": "景点名称",
          "address": "详细地址",
          "location": {"longitude": 116.397128, "latitude": 39.916527},
          "visit_duration": 120,
          "description": "景点详细描述",
          "category": "景点类别",
          "ticket_price": 60
        }
      ],
      "meals": [
        {"type": "breakfast", "name": "早餐推荐", "description": "早餐描述", "estimated_cost": 30},
        {"type": "lunch", "name": "午餐推荐", "description": "午餐描述", "estimated_cost": 50},
        {"type": "dinner", "name": "晚餐推荐", "description": "晚餐描述", "estimated_cost": 80}
      ]
    }
  ],
  "weather_info": [
    {
      "date": "YYYY-MM-DD",
      "day_weather": "晴",
      "night_weather": "多云",
      "day_temp": 25,
      "night_temp": 15,
      "wind_direction": "南风",
      "wind_power": "1-3级"
    }
  ],
  "overall_suggestions": "总体建议",
  "budget": {
    "total_attractions": 180,
    "total_hotels": 1200,
    "total_meals": 480,
    "total_transportation": 200,
    "total": 2060
  }
}
```

**重要提示:**
1. weather_info数组必须包含每一天的天气信息
2. 温度必须是纯数字(不要带°C等单位)
3. 每天安排2-3个景点
4. 考虑景点之间的距离和游览时间
5. 每天必须包含早中晚三餐
6. 提供实用的旅行建议
7. **必须包含预算信息**:
   - 景点门票价格(ticket_price)
   - 餐饮预估费用(estimated_cost)
   - 酒店预估费用(estimated_cost)
   - 预算汇总(budget)包含各项总费用
"""

# ✅✅✅ 关键：在所有函数/类定义之前，显式初始化为 None
# _trip_planner_agent = None
# _checkpointer = None
# _init_lock = asyncio.ock()


class MultiAgentTripPlanner:
    """多智能体旅行规划系统"""

    def __init__(self, llm, checkpointer):
        """初始化多智能体系统"""
        print("🔄 开始初始化多智能体旅行规划系统...")

        settings = get_settings()
        self.llm = llm
        self.checkpointer = checkpointer

        self.provider = settings.openai_base_url
        self.model = settings.openai_model

    async def initialize(self):
        # 创建共享的MCP工具(只创建一次)
        print("  - 创建共享MCP工具...")
        self.mcp_client = MultiServerMCPClient(
            {
                "amap": {
                    "url": "https://mcp.amap.com/sse?key=f5345c390cff8a23d5c42a395b765779",
                    "transport": "sse",
                },
            }
        )
        tools = await self.mcp_client.get_tools()

        # 创建景点搜索Agent
        print("  - 创建景点搜索Agent...")
        self.attraction_agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=ATTRACTION_AGENT_PROMPT,
            checkpointer=self.checkpointer,
        )

        print("  - 创建天气搜索Agent...")
        self.weather_agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=WEATHER_AGENT_PROMPT,
            checkpointer=self.checkpointer,
        )

        print("  - 创建酒店搜索Agent...")
        self.hotel_agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=HOTEL_AGENT_PROMPT,
            checkpointer=self.checkpointer,
        )

        print("  - 创建行程生成Agent...")
        self.planner_agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=PLANNER_AGENT_PROMPT,
            checkpointer=self.checkpointer,
        )

        print(f"✅ 多智能体系统初始化成功")
        print(f"   景点搜索Agent: {len(tools)} 个工具")  # ✅ 直接用 tools
        for t in tools:
            print(f"     🔧 {t.name}: {t.description[:50]}")



    # 修改为并行Agent结构...
    async def plan_trip(self, request: TripRequest) -> TripPlan:
        """
        使用多智能体协作生成旅行计划

        Args:
            request: 旅行请求

        Returns:
            旅行计划
        """
        try:
            print(f"\n{'=' * 60}")
            print(f"🚀 开始多智能体协作规划旅行...")
            print(f"目的地: {request.city} | 天数: {request.travel_days}天")
            print(f"{'=' * 60}\n")

            # ==========================================
            # 🔥 核心优化：前3个Agent并行执行
            # ==========================================
            print("⚡ 并行执行: 景点搜索 / 天气查询 / 酒店推荐...")

            attraction_query = self._build_attraction_query(request)
            weather_query = f"请查询{request.city}的天气信息"
            hotel_query = f"请搜索{request.city}的{request.accommodation}酒店"

            # 定义三个异步任务
            attraction_task = self.attraction_agent.ainvoke(
                {"messages": [{"role": "user", "content": attraction_query}]},
                config={"configurable": {"thread_id": f"trip_{request.city}_attractions"}}
            )
            weather_task = self.weather_agent.ainvoke(
                {"messages": [{"role": "user", "content": weather_query}]},
                config={"configurable": {"thread_id": f"trip_{request.city}_weather"}}
            )
            hotel_task = self.hotel_agent.ainvoke(
                {"messages": [{"role": "user", "content": hotel_query}]},
                config={"configurable": {"thread_id": f"trip_{request.city}_hotels"}}
            )

            # 并发等待所有任务完成
            results = await asyncio.gather(
                attraction_task, weather_task, hotel_task,
                return_exceptions=True  # ⚠️ 防止单个失败导致全部崩溃
            )

            # 安全提取结果
            attraction_response = self._safe_extract(results[0], "景点搜索")
            weather_response = self._safe_extract(results[1], "天气查询")
            hotel_response = self._safe_extract(results[2], "酒店推荐")

            print(f"✅ 并行任务完成!")
            print(f"  📍 景点: {attraction_response[:100]}...")
            print(f"  🌤️  天气: {weather_response[:100]}...")
            print(f"  🏨 酒店: {hotel_response[:100]}...\n")

            # ==========================================
            # 步骤4: 串行执行（必须等待前面结果）
            # ==========================================
            print("📋 步骤4: 整合信息生成行程计划...")
            planner_query = self._build_planner_query(
                request, attraction_response, weather_response, hotel_response
            )
            result = await self.planner_agent.ainvoke(
                {"messages": [{"role": "user", "content": planner_query}]},
                config={"configurable": {"thread_id": f"trip_{request.city}_plan"}}
            )
            planner_response = result["messages"][-1].content

            trip_plan = self._parse_response(planner_response, request)

            print(f"{'=' * 60}")
            print(f"✅ 旅行计划生成完成!")
            print(f"{'=' * 60}\n")
            return trip_plan

        except Exception as e:
            print(f"❌ 生成旅行计划失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._create_fallback_plan(request)

    def _safe_extract(self, result, task_name: str) -> str:
        """安全地从gather结果中提取内容，处理异常"""
        if isinstance(result, Exception):
            print(f"⚠️ {task_name}失败: {result}")
            return f"{task_name}暂时无法获取信息"
        try:
            return result["messages"][-1].content
        except (KeyError, IndexError, TypeError) as e:
            print(f"⚠️ {task_name}结果解析失败: {e}")
            return f"{task_name}结果格式异常"





    def _build_attraction_query(self, request: TripRequest) -> str:
        """构建景点搜索查询 - 直接包含工具调用"""
        keywords = []
        if request.preferences:
            # 只取第一个偏好作为关键词
            keywords = request.preferences[0]
        else:
            keywords = "景点"

        # 直接返回工具调用格式
        query = f"请使用amap_maps_text_search工具搜索{request.city}的{keywords}相关景点。\n[TOOL_CALL:amap_maps_text_search:keywords={keywords},city={request.city}]"
        return query

    def _build_planner_query(self, request: TripRequest, attractions: str, weather: str, hotels: str = "") -> str:
        """构建行程规划查询"""
        query = f"""请根据以下信息生成{request.city}的{request.travel_days}天旅行计划:

                    **基本信息:**
                    - 城市: {request.city}
                    - 日期: {request.start_date} 至 {request.end_date}
                    - 天数: {request.travel_days}天
                    - 交通方式: {request.transportation}
                    - 住宿: {request.accommodation}
                    - 偏好: {', '.join(request.preferences) if request.preferences else '无'}

                    **景点信息:**
                    {attractions}

                    **天气信息:**
                    {weather}

                    **酒店信息:**
                    {hotels}

                    **要求:**
                    1. 每天安排2-3个景点
                    2. 每天必须包含早中晚三餐
                    3. 每天推荐一个具体的酒店(从酒店信息中选择)
                    3. 考虑景点之间的距离和交通方式
                    4. 返回完整的JSON格式数据
                    5. 景点的经纬度坐标要真实准确
                    """
        if request.free_text_input:
            query += f"\n**额外要求:** {request.free_text_input}"

        return query

    def _parse_response(self, response: str, request: TripRequest) -> TripPlan:
        """
        解析Agent响应

        Args:
            response: Agent响应文本
            request: 原始请求

        Returns:
            旅行计划
        """
        try:
            # 尝试从响应中提取JSON
            # 查找JSON代码块
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response and "}" in response:
                # 直接查找JSON对象
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                raise ValueError("响应中未找到JSON数据")

            # 解析JSON
            data = json.loads(json_str)

            # 转换为TripPlan对象
            trip_plan = TripPlan(**data)

            return trip_plan

        except Exception as e:
            print(f"⚠️  解析响应失败: {str(e)}")
            print(f"   将使用备用方案生成计划")
            return self._create_fallback_plan(request)

    def _create_fallback_plan(self, request: TripRequest) -> TripPlan:
        """创建备用计划(当Agent失败时)"""
        from datetime import datetime, timedelta

        # 解析日期
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")

        # 创建每日行程
        days = []
        for i in range(request.travel_days):
            current_date = start_date + timedelta(days=i)

            day_plan = DayPlan(
                date=current_date.strftime("%Y-%m-%d"),
                day_index=i,
                description=f"第{i + 1}天行程",
                transportation=request.transportation,
                accommodation=request.accommodation,
                attractions=[
                    Attraction(
                        name=f"{request.city}景点{j + 1}",
                        address=f"{request.city}市",
                        location=Location(longitude=116.4 + i * 0.01 + j * 0.005, latitude=39.9 + i * 0.01 + j * 0.005),
                        visit_duration=120,
                        description=f"这是{request.city}的著名景点",
                        category="景点"
                    )
                    for j in range(2)
                ],
                meals=[
                    Meal(type="breakfast", name=f"第{i + 1}天早餐", description="当地特色早餐"),
                    Meal(type="lunch", name=f"第{i + 1}天午餐", description="午餐推荐"),
                    Meal(type="dinner", name=f"第{i + 1}天晚餐", description="晚餐推荐")
                ]
            )
            days.append(day_plan)

        return TripPlan(
            city=request.city,
            start_date=request.start_date,
            end_date=request.end_date,
            days=days,
            weather_info=[],
            overall_suggestions=f"这是为您规划的{request.city}{request.travel_days}日游行程,建议提前查看各景点的开放时间。"
        )


# ===================================================================
# 🔧 内部基础设施：同步执行异步代码的唯一通道
# ===================================================================
def _run_sync(coro_func, *args, **kwargs):
    """
    在同步上下文中安全执行协程。
    - 线程池 / 主线程脚本：asyncio.run() ✅
    - 已有 running loop（如 Jupyter）：nest_asyncio 兜底
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Jupyter / 某些特殊环境
        import nest_asyncio
        nest_asyncio.apply()
        return loop.run_until_complete(coro_func(*args, **kwargs))
    else:
        # FastAPI def 路由（线程池）/ 普通脚本 ← 主要路径
        return asyncio.run(coro_func(*args, **kwargs))


async def _create_planner() -> MultiAgentTripPlanner:
    """创建一个完整的 planner 实例（含 MCP 连接）"""
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL_ID"),
        base_url=os.getenv("LLM_BASE_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        temperature=0.7,
    )
    checkpointer = InMemorySaver()
    planner = MultiAgentTripPlanner(llm=llm, checkpointer=checkpointer)
    await planner.initialize()
    return planner


# ===================================================================
# 🎯 对外公开 API（全部同步）
# ===================================================================

def get_agent_info() -> dict:
    """
    获取 Agent 元信息（健康检查专用）

    Returns:
        {
            "agent_name": str,
            "tools_count": int,
            "model": str,
            "provider": str,
        }
    """
    async def _inner():
        planner = await _create_planner()
        agent = planner.attraction_agent
        info = {
            "agent_name": agent.name,
            "tools_count": len(agent.tools),
            "model": planner.model,
            "provider": planner.provider,
        }
        return info

    return _run_sync(_inner)


def generate_plan(request) -> "TripPlan":
    """
    生成旅行计划（行程规划专用）

    Args:
        request: TripRequest 对象

    Returns:
        TripPlan 对象
    """
    async def _inner():
        planner = await _create_planner()
        return await planner.plan_trip(request)

    return _run_sync(_inner)


def chat(query: str, thread_id: str = "default") -> str:
    """
    与景点搜索 Agent 自由对话（可选扩展）

    Args:
        query: 用户问题
        thread_id: 会话ID

    Returns:
        Agent 回复文本
    """
    async def _inner():
        planner = await _create_planner()
        result = await planner.attraction_agent.ainvoke(
            {"messages": [{"role": "user", "content": query}]},
            config={"configurable": {"thread_id": thread_id}},
        )
        return result["messages"][-1].content

    return _run_sync(_inner)