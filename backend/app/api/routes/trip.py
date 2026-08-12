"""旅行规划API路由"""
import asyncio
from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import (
    TripRequest,
    TripPlanResponse,
    ErrorResponse
) # 从schemas中引入了一些数据类。。。

# jlq # 文件替换 ...
# from backend.app.agents.trip_planner_agent_original import get_trip_planner_agent
from backend.app.agents.trip_planner_agent import generate_plan,get_agent_info

router = APIRouter(prefix="/trip", tags=["旅行规划"])


@router.post(
    "/plan",
    response_model=TripPlanResponse,
    summary="生成旅行计划",
    description="根据用户输入的旅行需求,生成详细的旅行计划"
)
def plan_trip(request: TripRequest):
    """
    生成旅行计划

    Args:
        request: 旅行请求参数

    Returns:
        旅行计划响应
    """
    try:
        print(f"\n{'='*60}")
        print(f"📥 收到旅行规划请求:")
        print(f"   城市: {request.city}")
        print(f"   日期: {request.start_date} - {request.end_date}")
        print(f"   天数: {request.travel_days}")
        print(f"{'='*60}\n")

        # 获取Agent实例
        print("🔄 获取多智能体系统实例...")
        # agent = get_trip_planner_agent()

        # 生成旅行计划
        print("🚀 开始生成旅行计划...")
        # trip_plan = agent.plan_trip(request)
        trip_plan = generate_plan(request)

        print("✅ 旅行计划生成成功,准备返回响应\n")

        return TripPlanResponse(
            success=True,
            message="旅行计划生成成功",
            data=trip_plan
        )

    except Exception as e:
        print(f"❌ 生成旅行计划失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"生成旅行计划失败: {str(e)}"
        )


@router.get(
    "/health",
    summary="健康检查",
    description="检查旅行规划服务是否正常"
)
def health_check():                           # ← 同步 def
    """健康检查"""
    try:
        info = get_agent_info()                # ← 一行搞定

        return {
            "status": "healthy",
            "service": "trip-planner",
            **info,                            # 展开 agent_name, tools_count 等
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"服务不可用: {str(e)}",
        )
