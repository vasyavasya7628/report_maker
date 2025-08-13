# 🌟 report_maker


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub Stars](https://img.shields.io/github/stars/vasyavasya7628/report_maker?style=social)


## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/vasyavasya7628/report_maker.git

# Install dependencies
pip install -r requirements.txt

# Run the application
python .\app\log_analyzer.py --file example1.log --report average

# Run Tests
pytest --cov=mypackage

# Results
(.venv) PS D:\PythonProjects\report_maker> python .\app\log_analyzer.py --file example1.log --report average
  №  url                         requests    avg_resp_time
  0  /api/context/...                  21            0.043
  1  /api/homeworks/...                71            0.158
  2  /api/specializations/...           6            0.035
  3  /api/users/...                     1            0.072
  4  /api/challenges/...                1            0.056
(.venv) PS D:\PythonProjects\report_maker> python .\app\log_analyzer.py --file example2.log --report average
  №  url                         requests    avg_resp_time
  0  /api/homeworks/...             55241            0.093
  1  /api/context/...               43907            0.019
  2  /api/specializations/...        8329            0.052
  3  /api/users/...                  1446            0.066
  4  /api/challenges/...             1475            0.078

# Test results 
(.venv) PS D:\PythonProjects\report_maker> pytest --cov=app                                   
======================================================================================================== test session starts =========================================================================================================
platform win32 -- Python 3.12.10, pytest-8.4.1, pluggy-1.6.0 -- D:\PythonProjects\report_maker\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\PythonProjects\report_maker
configfile: pytest.ini
testpaths: tests
plugins: cov-6.2.1
collected 6 items                                                                                                                                                                                                                     

tests/test_main.py::test_parse_args PASSED                                                                                                                                                                                      [ 16%] 
tests/test_main.py::test_process_files PASSED                                                                                                                                                                                   [ 33%]
tests/test_main.py::test_create_stats PASSED                                                                                                                                                                                    [ 50%] 
tests/test_main.py::test_generate_average_report PASSED                                                                                                                                                                         [ 66%] 
tests/test_main.py::test_generate_report PASSED                                                                                                                                                                                 [ 83%] 
tests/test_main.py::test_main_integration PASSED                                                                                                                                                                                [100%]D:\PythonProjects\report_maker\.venv\Lib\site-packages\coverage\inorout.py:516: CoverageWarning: Module src was never imported. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported")


=========================================================================================================== tests coverage =========================================================================================================== 
__________________________________________________________________________________________ coverage: platform win32, python 3.12.10-final-0 __________________________________________________________________________________________ 

Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
app\log_analyzer.py      66      2    97%   58, 96
---------------------------------------------------
TOTAL                    66      2    97%
Required test coverage of 80.0% reached. Total coverage: 96.97%
========================================================================================================= 6 passed in 0.24s ==========================================================================================================
