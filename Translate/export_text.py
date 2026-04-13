import json
import csv
import os
from tqdm import tqdm

# Параметры
input_file = "hoshishiro_03.book"
output_csv = os.path.join(os.path.expanduser("~"), "Desktop", "dialogues.csv")  # на рабочий стол

# Проверка существования входного файла
if not os.path.exists(input_file):
    print(f"Ошибка: файл {input_file} не найден!")
    exit()

print("Загрузка JSON...")
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Получаем importGridList
import_grid_list = data.get("importGridList", {})
if not import_grid_list:
    print("Ошибка: нет importGridList")
    exit()

grid_array = import_grid_list.get("Array", [])
if not grid_array:
    print("Ошибка: importGridList.Array пуст")
    exit()

print(f"Найдено grid-секций: {len(grid_array)}")

# Открываем CSV на запись (с разделителем табуляция)
with open(output_csv, "w", encoding="utf-8-sig", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["rowIndex", "character", "japanese", "chinese", "russian", "voice", "command"])

    total_processed = 0
    for grid_idx, grid in enumerate(tqdm(grid_array, desc="Обработка grid-секций")):
        rows_obj = grid.get("rows", {})
        rows_array = rows_obj.get("Array", [])
        if not rows_array:
            continue

        for row in rows_array:
            strings_obj = row.get("strings", {})
            strings = strings_obj.get("Array", [])
            # Дополняем до 14 элементов (индекс 12)
            while len(strings) < 14:
                strings.append("")

            japanese = strings[8] if len(strings) > 8 else ""
            if not japanese.strip():
                continue

            row_index = row.get("rowIndex", "")
            character = strings[1] if len(strings) > 1 else ""
            chinese = strings[12] if len(strings) > 12 else ""
            voice = strings[10] if len(strings) > 10 else ""
            command = strings[0] if len(strings) > 0 else ""

            writer.writerow([row_index, character, japanese, chinese, "", voice, command])
            total_processed += 1

print(f"Обработано строк с текстом: {total_processed}")
print(f"Экспорт завершён. CSV сохранён в {output_csv}")