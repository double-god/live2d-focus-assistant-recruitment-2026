# 学习打卡小助手
# 记录每天的学习打卡，支持查看和统计

# 打卡数据，用列表存
records = []


def add_record():
    """添加一条打卡记录"""
    date = input("请输入日期（如 2026-09-27）： ")
    content = input("请输入学习内容： ")
    record = {"date": date, "content": content}
    records.append(record)
    print("打卡成功！")


def show_records():
    """显示所有打卡记录"""
    if not records:
        print("还没有打卡记录")
        return
    print("\n===== 打卡记录 =====")
    for i, record in enumerate(records, 1):
        print(f"{i}. {record['date']} - {record['content']}")
    print("====================\n")


def count_days():
    """统计打卡天数（去重）"""
    if not records:
        print("还没有打卡记录")
        return
    dates = set()
    for record in records:
        dates.add(record["date"])
    print(f"一共打卡 {len(dates)} 天")


def main():
    """主菜单循环"""
    while True:
        print("\n===== 学习打卡小助手 =====")
        print("1. 添加打卡")
        print("2. 查看记录")
        print("3. 统计天数")
        print("4. 退出")
        choice = input("请选择（1-4）： ")

        if choice == "1":
            add_record()
        elif choice == "2":
            show_records()
        elif choice == "3":
            count_days()
        elif choice == "4":
            print("👋 再见！")
            break
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main()