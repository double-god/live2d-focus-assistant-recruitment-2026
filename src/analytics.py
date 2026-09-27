"""专注历史的统计与报告函数，保持无框架、易于单独复用。"""
from sqlite3 import Connection
from . import repositories


def _ended(connection):
    return [s for s in repositories.all_sessions(connection, include_archived=False) if s["status"] in {"completed", "abandoned"}]


def summary(connection):
    rows = _ended(connection)
    completed = [s for s in rows if s["status"] == "completed"]
    durations = [max(0, s["duration_seconds"] - s["remaining_seconds"]) for s in completed]
    return {"total_sessions": len(rows), "completed_sessions": len(completed),
            "abandoned_sessions": len(rows) - len(completed),
            "total_focus_seconds": sum(durations),
            "average_focus_seconds": round(sum(durations) / len(durations), 1) if durations else 0,
            "completion_rate": round(len(completed) / len(rows), 4) if rows else 0}


def daily_summary(connection, days=30):
    """兼容统计接口；按日期的完整聚合留作 M01。"""
    if days <= 0:
        return []
    return []


def time_buckets(connection):
    """兼容统计接口；时段边界与聚合留作 M02。"""
    return {"morning": 0, "afternoon": 0, "evening": 0, "night": 0}


def report(connection):
    # Baseline report intentionally exposes only the basic counters. Date-range
    # filtering, streaks and a readable text rendering are left for follow-up work.
    return summary(connection)


def analyze_focus_records(records):
    """
    分析专注记录，按时长统计为短、中、长三类。
    """
    
    # 1. 安全检查：如果列表是空的，直接返回全0结果
    if not records:
        return {"short": 0, "normal": 0, "long": 0}

    # 2. 初始化计数器
    result = {"short": 0, "normal": 0, "long": 0}

    # 3. 遍历每一条记录
    for record in records:
        # 获取计划时长和剩余时长，如果没有则默认为0
        duration = record.get("duration_seconds", 0)
        remaining = record.get("remaining_seconds", 0)

        # 计算实际专注时长
        actual_time = duration - remaining

        # 4. 异常处理：如果结果是负数，按题目要求视为0
        if actual_time < 0:
            actual_time = 0

        # 5. 条件分支：根据时长归类
        # 10分钟 = 600秒，30分钟 = 1800秒
        if actual_time < 600:
            result["short"] += 1      # 少于10分钟
        elif actual_time <= 1800:     # 10到30分钟之间 (包含30分钟)
            result["normal"] += 1
        else:                         # 超过30分钟
            result["long"] += 1

    # 6. 返回最终统计结果
    return result