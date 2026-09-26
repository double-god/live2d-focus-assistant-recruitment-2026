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



    def seconds_to_cn(seconds):
        """
        E03:将秒数转为中文时长字符串
        :param seconds:输入的秒，必须为非负整数
        :return:中文格式化后的时常
        """
        if isinstance(seconds,bool):
            raise TypeError("不允许布尔类型")
        if not isinstance(seconds,int):
            raise TypeError("输入必须是整数")
        if seconds < 0:
            raise ValueError("输入秒数不能为负")
        h,remain = divmod(seconds,3600)
        m,s = divmod(remain,60)
        parts = []
        if h > 0:
            parts.append(f"{h}小时")
        if m > 0:
            parts.append(f"{m}分钟")
        if s > 0:
            parts.append(f"{s}秒")
        if len(parts) == 0:
            return "0秒"
        return"".join(parts)    
