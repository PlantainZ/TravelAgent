"""高德地图MCP服务封装"""

from typing import List, Dict, Any, Optional
import json
import asyncio
from typing import Dict, Any, Optional, List
import re

import aiohttp

# jlq_crt # =====================================
# from hello_agents.tools import MCPTool
from tools.builtin.protocol_tools import MCPTool
# MCPTool已可以被替代！加油替换
# ===============================================

from backend.app.config import get_settings
from langchain_mcp_adapters.client import MultiServerMCPClient
from backend.app.models.schemas import Location, POIInfo, WeatherInfo

# 全局MCP工具实例
_amap_mcp_tool = None


class AmapService:
    """高德地图 MCP 服务封装 - 完整12个功能"""

    def __init__(self):
        settings = get_settings()

        if not settings.amap_api_key:
            raise ValueError("请在.env中设置AMAP_API_KEY")

        self._client = MultiServerMCPClient({
            "amap": {
                "url": f"https://mcp.amap.com/sse?key={settings.amap_api_key}",
                "transport": "sse",
            },
        })
        self._tool_map: Dict[str, Any] = {}

    async def initialize(self):
        if not self._tool_map:
            tools = await self._client.get_tools()
            self._tool_map = {t.name: t for t in tools}
        return self._tool_map

    async def list_tools(self):
        tool_map = await self.initialize()
        print(f"共 {len(tool_map)} 个工具:")
        for name, t in tool_map.items():
            desc = (t.description or "")[:80]
            print(f"  • {name}: {desc}")

    async def inspect_tool(self, tool_name: str):
        """🔍 打印工具的实际参数 schema"""
        if not self._tool_map:
            await self.initialize()
        tool = self._tool_map.get(tool_name)
        if not tool:
            print(f"❌ 工具 '{tool_name}' 不存在")
            return

        print(f"\n🔍 Tool: {tool_name}")
        print(f"   Description: {(tool.description or '')[:120]}")

        schema = None
        args_schema = getattr(tool, "args_schema", None)
        if isinstance(args_schema, dict):
            schema = args_schema
        elif hasattr(args_schema, "model_json_schema"):
            schema = args_schema.model_json_schema()
        elif hasattr(args_schema, "schema"):
            schema = args_schema.schema()

        if schema is None:
            input_schema = getattr(tool, "input_schema", None)
            if isinstance(input_schema, dict):
                schema = input_schema

        if schema:
            print(f"   Args Schema:\n{json.dumps(schema, ensure_ascii=False, indent=4)}")
        else:
            print("   ⚠️ 无法获取参数 schema")

    async def _invoke(self, tool_name: str, params: dict) -> Any:
        if not self._tool_map:
            await self.initialize()
        tool = self._tool_map.get(tool_name)
        if not tool:
            available = ", ".join(sorted(self._tool_map.keys()))
            raise ValueError(f"未找到工具 '{tool_name}'，可用: {available}")
        return await tool.ainvoke(params)

    # ──────────────────────────────────────────────
    # 1. 地理编码 maps_geo
    #    Input: address(必填), city(可选)
    # ──────────────────────────────────────────────
    async def geocode(self, address: str, city: Optional[str] = None) -> Any:
        params: Dict[str, str] = {"address": address}
        if city:
            params["city"] = city
        return await self._invoke("maps_geo", params)

    # ──────────────────────────────────────────────
    # 2. 反向地理编码 maps_regeocode
    #    Input: location(必填)
    # ──────────────────────────────────────────────
    async def regeocode(self, location: str) -> Any:
        return await self._invoke("maps_regeocode", {"location": location})

    # ──────────────────────────────────────────────
    # 3. IP定位 maps_ip_location
    #    Input: ip(必填)
    # ──────────────────────────────────────────────
    async def ip_location(self, ip: str) -> Any:
        return await self._invoke("maps_ip_location", {"ip": ip})

    # ──────────────────────────────────────────────
    # 4. 天气查询 maps_weather
    #    Input: city(必填, 城市名称或adcode)
    # ──────────────────────────────────────────────
    async def weather(self, city: str) -> Any:
        return await self._invoke("maps_weather", {"city": city})

    # ──────────────────────────────────────────────
    # 5. 骑行路径规划 maps_direction_bicycling
    #    Input: origin(必填), destination(必填)
    # ──────────────────────────────────────────────
    async def plan_bicycling(self, origin: str, destination: str) -> Any:
        return await self._invoke(
            "maps_direction_bicycling",
            {"origin": origin, "destination": destination},
        )

    # ──────────────────────────────────────────────
    # 6. 步行路径规划 maps_direction_walking
    #    Input: origin(必填), destination(必填)
    # ──────────────────────────────────────────────
    async def plan_walking(self, origin: str, destination: str) -> Any:
        return await self._invoke(
            "maps_direction_walking",
            {"origin": origin, "destination": destination},
        )

    # ──────────────────────────────────────────────
    # 7. 驾车路径规划 maps_direction_driving
    #    Input: origin(必填), destination(必填)
    # ──────────────────────────────────────────────
    async def plan_driving(self, origin: str, destination: str) -> Any:
        return await self._invoke(
            "maps_direction_driving",
            {"origin": origin, "destination": destination},
        )

    # ──────────────────────────────────────────────
    # 8. 公共交通规划 maps_direction_transit_integrated
    #    Input: origin, destination, city, cityd (全部必填)
    # ──────────────────────────────────────────────
    async def plan_transit(
        self, origin: str, destination: str, city: str, cityd: str
    ) -> Any:
        return await self._invoke(
            "maps_direction_transit_integrated",
            {
                "origin": origin,
                "destination": destination,
                "city": city,
                "cityd": cityd,
            },
        )

    # ──────────────────────────────────────────────
    # 9. 距离测量 maps_distance
    #    Input: origins(必填,多坐标用|分隔), destination(必填), type(可选:0直线/1驾车/3步行)
    # ──────────────────────────────────────────────
    async def measure_distance(
        self, origins: str, destination: str, type_: Optional[str] = None
    ) -> Any:
        params: Dict[str, str] = {"origins": origins, "destination": destination}
        if type_ is not None:
            params["type"] = type_
        return await self._invoke("maps_distance", params)

    # ──────────────────────────────────────────────
    # 10. 关键字搜索 maps_text_search
    #     Input: keywords(必填), city(可选), citylimit(可选,bool)
    # ──────────────────────────────────────────────
    async def text_search(
        self,
        keywords: str,
        city: Optional[str] = None,
        citylimit: Optional[bool] = None,
    ) -> Any:

        params = {
            "key": get_settings().amap_api_key,
            "keywords": keywords,
            "city": city,
            "citylimit": str(citylimit).lower(),
            "output": "JSON",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://restapi.amap.com/v3/place/text", params=params
            ) as resp:
                # ✅ 直接用 .json() 解析，不要手动包装
                data = await resp.json()

        # ✅ 检查高德 API 返回状态
        if data.get("status") != "1":
            raise Exception(f"高德API错误: {data.get('info', '未知错误')}")

        # ✅ 直接提取 pois 数组并返回
        pois = data.get("pois", [])

        # ✅ 数据清洗 & 格式转换
        cleaned_pois = []
        for poi in pois:
            # 1. 处理 location: "lng,lat" 字符串 → Location 对象
            location_str = poi.get("location", "")
            lng, lat = None, None
            if isinstance(location_str, str) and "," in location_str:
                parts = location_str.split(",")
                if len(parts) == 2:
                    lng, lat = float(parts[0]), float(parts[1])

            # 2. 处理 tel: [] → "" 或 None
            tel = poi.get("tel")
            if not isinstance(tel, str):
                tel = ""

            cleaned_pois.append({
                "name": poi.get("name", ""),
                "address": poi.get("address", ""),
                "location": {"longitude": lng, "latitude": lat} if lng and lat else None,
                "tel": tel,
                "type": poi.get("type", ""),
                "id": poi.get("id", ""),
                # ... 其他你需要的字段 ...
            })

        return cleaned_pois

    # ──────────────────────────────────────────────
    # 11. 周边搜索 maps_around_search
    #     Input: keywords(必填), location(必填), radius(可选)
    # ──────────────────────────────────────────────
    async def around_search(
        self, keywords: str, location: str, radius: Optional[str] = None
    ) -> Any:
        params: Dict[str, str] = {"keywords": keywords, "location": location}
        if radius is not None:
            params["radius"] = radius
        return await self._invoke("maps_around_search", params)

    # ──────────────────────────────────────────────
    # 12. POI详情 maps_search_detail
    #     Input: id(必填)
    # ──────────────────────────────────────────────
    async def search_detail(self, id: str) -> Any:
        return await self._invoke("maps_search_detail", {"id": id})

    # ──────────────────────────────────────────────
    # 🎁 附加: 行程地图展示 maps_schema_personal_map
    # ──────────────────────────────────────────────
    async def personal_map(self, org_name: str, line_list: List[Dict]) -> Any:
        return await self._invoke(
            "maps_schema_personal_map",
            {"orgName": org_name, "lineList": line_list},
        )

    # ──────────────────────────────────────────────
    # 🎁 附加: 导航唤醒 maps_schema_navi
    # ──────────────────────────────────────────────
    async def schema_navi(self, lon: str, lat: str) -> Any:
        return await self._invoke("maps_schema_navi", {"lon": lon, "lat": lat})

    # ──────────────────────────────────────────────
    # 🎁 附加: 打车唤醒 maps_schema_take_taxi
    # ──────────────────────────────────────────────
    async def schema_take_taxi(
        self,
        dlon: str,
        dlat: str,
        dname: str,
        slon: Optional[str] = None,
        slat: Optional[str] = None,
        sname: Optional[str] = None,
    ) -> Any:
        params: Dict[str, str] = {"dlon": dlon, "dlat": dlat, "dname": dname}
        if slon is not None:
            params["slon"] = slon
        if slat is not None:
            params["slat"] = slat
        if sname is not None:
            params["sname"] = sname
        return await self._invoke("maps_schema_take_taxi", params)


# ────────────────────────────────────────────────────────
# MCP Content 解包 + 坐标提取（通用工具函数）
# ────────────────────────────────────────────────────────

_COORD_PATTERN = re.compile(r"(\d{2,3}\.\d+)\s*,\s*(\d{2,3}\.\d+)")


def unwrap_mcp_content(raw: Any) -> Any:
    """
    将 MCP 工具返回的 Content 列表解包为实际数据。
    格式: [{'type': 'text', 'text': '<json-string>', 'id': '...'}]
    """
    if isinstance(raw, list) and len(raw) > 0:
        first = raw[0]
        if isinstance(first, dict) and "text" in first:
            try:
                return json.loads(first["text"])
            except (json.JSONDecodeError, TypeError):
                return first["text"]
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return raw
    return raw


def extract_location(geo_result: Any) -> str:
    """从 maps_geo 返回值中提取 'lng,lat'"""
    data = unwrap_mcp_content(geo_result)
    if isinstance(data, dict):
        results = data.get("results", [])
        if isinstance(results, list) and len(results) > 0:
            loc = results[0].get("location", "")
            if loc:
                return str(loc).strip()
        loc = data.get("location", "")
        if loc:
            return str(loc).strip()
    match = _COORD_PATTERN.search(str(data))
    if match:
        lng, lat = match.group(1), match.group(2)
        if 73 <= float(lng) <= 136 and 3 <= float(lat) <= 54:
            return f"{lng},{lat}"
    print(f"  ⚠️ 坐标提取失败，原始值: {repr(geo_result)}")
    return ""



# 创建全局服务实例
_amap_service = None

def get_amap_service() -> AmapService:
    """获取高德地图服务实例(单例模式)"""
    global _amap_service

    if _amap_service is None:
        _amap_service = AmapService()
    
    return _amap_service