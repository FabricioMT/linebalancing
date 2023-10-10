set original_dir=%cd%\
set venv_root_dir="%original_dir%venv"

call pip install virtualenv

call virtualenv venv

cd %venv_root_dir%

call %venv_root_dir%\Scripts\activate.bat

cd %original_dir%

call pip install -r requirements.txt

call python.exe -m pip install --upgrade pip
call pip freeze
pause
