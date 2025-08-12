import argparse
import json
from tabulate import tabulate

REPORT_GENERATORS = {}


def report_generator(report_type):
    def decorator(func):
        REPORT_GENERATORS[report_type] = func
        return func

    return decorator


@report_generator("average")
def generate_average_report(stats):
    table_data = []
    for i, (url, data) in enumerate(stats.items()):
        count = data["count"]
        avg_time = data["total_time"] / count
        # Форматируем до 3 знаков после запятой
        table_data.append([i, url, count, f"{avg_time:.3f}"])

    headers = ["№", "url", "requests", "avg_resp_time"]
    return tabulate(table_data, headers=headers, tablefmt="plain")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", nargs="+", required=True, help="Пути к лог-файлам")
    parser.add_argument(
        "--report",
        nargs="+",
        required=True,
        choices=["average"],
    )
    parser.add_argument("--date")
    return parser.parse_args()


def process_files(files, date_filter=None):
    records = []
    for file_path in files:
        try:
            with open(file_path, "r") as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        if not all(
                            key in record
                            for key in ["url", "response_time", "@timestamp"]
                        ):
                            continue
                        if date_filter and not record["@timestamp"].startswith(
                            date_filter
                        ):
                            continue
                        records.append(record)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            print(f"Файл не найден {file_path}")
    return records


def create_stats(records, stat_type):
    stats = {}
    if stat_type == "average":
        for record in records:
            url = record["url"]
            if url not in stats:
                stats[url] = {"count": 0, "total_time": 0.0}
            stats[url]["count"] += 1
            stats[url]["total_time"] += record["response_time"]
        return stats
    raise ValueError(f"Неподдерживаемый тип статистики: {stat_type}")


def generate_report(stats, report_type):
    if report_type not in REPORT_GENERATORS:
        raise ValueError(f"Неподдерживаемый тип отчёта: !{report_type}")
    return REPORT_GENERATORS[report_type](stats)


def main():
    args = parse_args()
    records = process_files(args.file, args.date)
    for report_type in args.report:
        stats = create_stats(records, report_type)
        report_table = generate_report(stats, report_type)
        print(report_table)


if __name__ == "__main__":
    main()
