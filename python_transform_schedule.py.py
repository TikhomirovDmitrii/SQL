import pandas as pd
from datetime import datetime, timedelta

# Исходная витрина (таблица 1)
data = {
    "tab_num": [15123, 16234, 17345, 17345, 18456, 19567],
    "start_date": ["2020-09-02", "2020-09-20", "2020-09-28", "2020-10-26", "2020-09-02", "2020-09-02"],
    "finish_date": ["9999-12-31", "2020-10-30", "2020-10-25", "2020-12-31", "9999-12-31", "2020-12-31"],
    "wday_type01": [0, 0, 1, 1, 2, 3],
    "wday_type02": [0, 0, 0, 1, 2, 3],
    "wday_type03": [0, 1, 0, 1, 2, 3],
    "wday_type04": [0, 1, 0, 1, 2, 3],
    "wday_type05": [0, 0, 0, 1, 2, 3],
    "wplace_type": [0, 2, 2, 1, 3, 4],
    "end_da": ["2020-10-31", None, None, None, "2020-09-30", None]
}

df = pd.DataFrame(data)
df["start_date"] = pd.to_datetime(df["start_date"])
df["finish_date"] = pd.to_datetime(df["finish_date"])
df["end_da"] = pd.to_datetime(df["end_da"])

# Замена finish_date на end_da, если оно не пусто
df["finish_date"] = df.apply(lambda row: row["end_da"] if pd.notnull(row["end_da"]) else row["finish_date"], axis=1)

# Целевой диапазон дат
start_date = datetime(2020, 9, 1)
end_date = datetime(2020, 12, 31)


def generate_schedule(row):
    schedule = []
    current_date = start_date

    while current_date <= end_date:
        if row["start_date"] <= current_date <= row["finish_date"]:
            weekday = current_date.weekday()  # Понедельник - 0, воскресенье - 6

            if weekday >= 5:  # Сб или вс
                to_be_at_office = None
            else:
                flag = row[f"wday_type0{weekday + 1}"]

                if row["wplace_type"] in [3, 4]:
                    # Логика для wplace_type 3 и 4
                    week_number = (current_date - row["start_date"]).days // 7
                    if row["wplace_type"] == 3:  # Неделя через неделю
                        to_be_at_office = 1 if week_number % 2 else 0
                    elif row["wplace_type"] == 4:  # Две недели через две
                        to_be_at_office = 1 if (week_number // 2) % 2 else 0
                else:
                    to_be_at_office = 1 if flag == 0 else 0
        else:
            to_be_at_office = None

        schedule.append({
            "tab_num": row["tab_num"],
            "ymd_date": current_date,
            "to_be_at_office": to_be_at_office
        })
        current_date += timedelta(days=1)
    return schedule


# Преобразование данных
schedules = df.apply(generate_schedule, axis=1)
result = pd.DataFrame([entry for schedule in schedules for entry in schedule])

print(result.head())
