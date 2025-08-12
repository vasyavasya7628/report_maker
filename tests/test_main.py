import pytest
import json
import sys
from app import log_analyzer


def test_parse_args(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["log_analyzer.py", "--file", "file1", "file2", "--report", "average"],
    )
    args = log_analyzer.parse_args()
    assert args.file == ["file1", "file2"]
    assert args.report == ["average"]
    assert args.date is None

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "log_analyzer.py",
            "--file",
            "file.log",
            "--report",
            "average",
            "--date",
            "2023-01-01",
        ],
    )
    args = log_analyzer.parse_args()
    assert args.date == "2023-01-01"


def test_process_files(tmp_path, capsys):
    valid_file = tmp_path / "valid.log"
    valid_data = [
        '{"url": "/test", "response_time": 0.1, "@timestamp": "2023-01-01T12:00:00"}',
        '{"url": "/test", "response_time": 0.2, "@timestamp": "2023-01-01T12:01:00"}',
    ]
    valid_file.write_text("\n".join(valid_data))

    invalid_file = tmp_path / "invalid.log"
    invalid_file.write_text('invalid json data\n{"missing": "fields"}')

    records = log_analyzer.process_files([str(valid_file), str(invalid_file)])
    assert len(records) == 2
    assert records[0]["url"] == "/test"

    records = log_analyzer.process_files([str(valid_file)], date_filter="2023-01-01")
    assert len(records) == 2

    records = log_analyzer.process_files(["nonexistent.log"])
    captured = capsys.readouterr()
    assert "Файл не найден" in captured.out
    assert records == []


def test_create_stats():
    records = [
        {"url": "/test", "response_time": 0.1},
        {"url": "/test", "response_time": 0.2},
        {"url": "/other", "response_time": 0.3},
    ]

    stats = log_analyzer.create_stats(records, "average")
    assert "/test" in stats
    assert stats["/test"]["count"] == 2
    assert stats["/test"]["total_time"] == pytest.approx(0.3)
    assert stats["/other"]["count"] == 1

    with pytest.raises(ValueError):
        log_analyzer.create_stats([], "invalid_type")


def test_generate_average_report():
    stats = {
        "/test": {"count": 2, "total_time": 0.3},
        "/other": {"count": 1, "total_time": 0.4},
    }

    report = log_analyzer.generate_average_report(stats)
    assert "№" in report
    assert "url" in report
    assert "0.15" in report
    assert "0.4" in report


def test_generate_report():
    stats = {"/test": {"count": 1, "total_time": 0.1}}
    report = log_analyzer.generate_report(stats, "average")
    assert isinstance(report, str)

    with pytest.raises(ValueError):
        log_analyzer.generate_report(stats, "invalid_type")


def test_main_integration(tmp_path, capsys, monkeypatch):
    log_file = tmp_path / "test.log"
    data = [
        {"url": "/test", "response_time": 0.1, "@timestamp": "2023-01-01T12:00:00"},
        {"url": "/test", "response_time": 0.2, "@timestamp": "2023-01-01T12:01:00"},
    ]
    log_file.write_text("\n".join(json.dumps(item) for item in data))

    monkeypatch.setattr(
        sys, "argv", ["log_analyzer.py", "--file", str(log_file), "--report", "average"]
    )

    log_analyzer.main()

    captured = capsys.readouterr()
    assert "№" in captured.out
    assert "url" in captured.out
    assert "requests" in captured.out
    assert "0.15" in captured.out
