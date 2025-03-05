import subprocess
import os
import sys
import json


def run_student_code(code_file, input_data, timeout=5):
    """
    Запускает код ученика и возвращает stdout.
    :param code_file: Путь к файлу с кодом ученика.
    :param input_data: Входные данные для программы (опционально).
    :param timeout: Время ожидания выполнения программы (в секундах).
    :return: Вывод программы (stdout).
    """
    try:
        result = subprocess.run(
            ["python", code_file],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            return f"Ошибка выполнения: {result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Ошибка: время выполнения программы истекло."
    except Exception as e:
        return f"Ошибка: {str(e)}"


def check_solution(test_cases, code_file):
    """
    Проверяет решение ученика на нескольких тестовых случаях.
    :param test_cases: Список тестовых случаев.
    :param code_file: Путь к файлу с кодом ученика.
    :return: Результаты проверки.
    """
    results = {"passed": 0, "failed": 0, "errors": 0, "details": []}

    for i, test_case in enumerate(test_cases, 1):
        input_data = test_case.get("input", "")
        expected_output = test_case.get("output", "")
        description = test_case.get("description", f"Тест {i}")

        student_output = run_student_code(code_file, input_data)

        if "Ошибка" in student_output:
            results["errors"] += 1
            results["details"].append(
                {
                    "test": description,
                    "status": "error",
                    "expected": expected_output,
                    "received": student_output,
                }
            )
        elif student_output.strip() == expected_output.strip():
            results["passed"] += 1
            results["details"].append(
                {
                    "test": description,
                    "status": "passed",
                    "expected": expected_output,
                    "received": student_output,
                }
            )
        else:
            results["failed"] += 1
            results["details"].append(
                {
                    "test": description,
                    "status": "failed",
                    "expected": expected_output,
                    "received": student_output,
                }
            )

    return results


def save_results(results, output_file="results.json"):
    """
    Сохраняет результаты проверки в JSON-файл.
    :param results: Результаты проверки.
    :param output_file: Имя файла для сохранения.
    """
    output_file = os.path.join("..", "_cache", output_file)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def main():
    test_cases = [
        {
            "input": "5\n3",
            "output": "8\n",
            "description": "Проверка сложения двух чисел",
        },
        {
            "input": "10\n-2",
            "output": "8\n",
            "description": "Проверка сложения с отрицательным числом",
        },
    ]

    code_file = "student_code.py"
    results = check_solution(test_cases, code_file)
    save_results(results)

    print(f"Пройдено тестов: {results['passed']}")
    print(f"Не пройдено тестов: {results['failed']}")
    print(f"Ошибок: {results['errors']}")
    for detail in results["details"]:
        print(f"\nТест: {detail['test']}")
        print(f"Статус: {detail['status']}")
        print(f"Ожидалось: {detail['expected']!r}")
        print(f"Получено: {detail['received']!r}")


if __name__ == "__main__":
    main()
