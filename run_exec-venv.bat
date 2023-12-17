set original_dir=%cd%\
set venv_root_dir="%original_dir%venv"

cd %venv_root_dir%

call %venv_root_dir%\Scripts\activate.bat

cd %original_dir%&cls

call python linebalancing.py GUNTHER.IN2 3

pause