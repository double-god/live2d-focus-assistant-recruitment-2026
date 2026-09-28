from src.presentation import format_session_summary


def test_active():
    session = {"task_text": "写代码", "status": "active", "duration_seconds": 1500, "remaining_seconds": 1200}
    result = format_session_summary(session)
    assert "进行中" in result
    assert "写代码" in result


def test_completed():
    session = {"task_text": "读论文", "status": "completed", "duration_seconds": 2700,
               "remaining_seconds": 0, "finished_at": "2026-09-28"}
    result = format_session_summary(session)
    assert "已完成" in result
    assert "2026-09-28" in result


def test_missing_fields():
    session = {"task_text": "调试"}
    result = format_session_summary(session)
    assert "调试" in result
    assert "未完成" in result


def test_original_not_modified():
    session = {"task_text": "写代码", "status": "active"}
    original = session.copy()
    format_session_summary(session)
    assert session == original


def test_special_chars():
    session = {"task_text": "含'引号'和\n换行", "status": "active"}
    result = format_session_summary(session)
    assert "含'引号'和\n换行" in result