"""会话记录展示层：将单条会话字典格式化为可读文本。"""

STATUS_MAP = {
    "active": "进行中",
    "paused": "已暂停",
    "completed": "已完成",
    "abandoned": "已放弃",
}


def format_session_summary(session):
    """将一条会话记录格式化为单行可读中文文本。

    参数 session 为字典，不会被修改。
    """
    task = session.get("task_text", "未知任务")
    status = session.get("status", "unknown")
    duration = session.get("duration_seconds", 0)
    remaining = session.get("remaining_seconds", 0)
    finished = session.get("finished_at") or "未完成"
    last_started = session.get("last_started_at") or "未开始"

    status_text = STATUS_MAP.get(status, status)

    return (
        f"任务：{task} | 状态：{status_text} | "
        f"计划时长：{duration}秒 | 剩余时长：{remaining}秒 | "
        f"最后开始：{last_started} | 完成时间：{finished}"
    )