import os
import re
import argparse
import json
import csv
from collections import Counter


parser = argparse.ArgumentParser(description="Анализ логов Android с группировкой ошибок")
parser.add_argument("--input", type=str, required=True, help="Файл или папка с логами")
parser.add_argument("--errors", type=str, default="output/errors_filtered.txt", help="Файл для всех ошибок")
parser.add_argument("--report", type=str, default="output/report.txt", help="Текстовый отчёт")
parser.add_argument("--json", type=str, default="output/report.json", help="JSON отчёт")
parser.add_argument("--csv", type=str, default="output/report.csv", help="CSV отчёт")
parser.add_argument("--level", type=str, default="E,W", help="Уровни логов для фильтрации (E,W,I)")
parser.add_argument("--top", type=int, default=10, help="Показывать топ-N ошибок")
args = parser.parse_args()


os.makedirs("output", exist_ok=True)
levels = args.level.split(",")
error_pattern = re.compile(rf"({'|'.join(levels)})/.+")


logs = []

if os.path.isdir(args.input):
    files = [os.path.join(args.input, f) for f in os.listdir(args.input) if f.endswith(".txt")]
else:
    files = [args.input]

if not files:
    print("Нет файлов для обработки!")
    exit(1)

for file in files:
    print(f"Читаем {file} ...")
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        logs.extend(f.readlines())

print(f"Всего строк логов: {len(logs)}")


def normalize_error(line):
    line = line.strip()

    line = re.sub(r"^\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}\s+", "", line)

    line = re.sub(r"\([0-9]+\)", "", line)
    line = re.sub(r"#\d+", "", line)
    line = re.sub(r"\{.*?\}", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()

errors_raw = [line for line in logs if error_pattern.search(line)]
errors_normalized = [normalize_error(line) for line in errors_raw]

print(f"Найдено ошибок/варнингов: {len(errors_raw)}")
print(f"После нормализации уникальных ошибок: {len(set(errors_normalized))}")


with open(args.errors, "w", encoding="utf-8") as f:
    for line in errors_raw:
        f.write(line)

print(f"Файл со всеми ошибками: {args.errors}")


counter = Counter(errors_normalized)
top_errors = counter.most_common(args.top)


with open(args.report, "w", encoding="utf-8") as f:
    for line, count in top_errors:
        f.write(f"{line}: {count} раз\n")
print(f"Топ {args.top} ошибок сохранён в {args.report}")


json_list = [{"error": line, "count": count} for line, count in top_errors]
with open(args.json, "w", encoding="utf-8") as f:
    json.dump(json_list, f, ensure_ascii=False, indent=4)
print(f"JSON отчёт: {args.json}")


with open(args.csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["error", "count"])
    writer.writeheader()
    writer.writerows(json_list)
print(f"CSV отчёт: {args.csv}")

print("Готово! Самые частые ошибки выделены.")