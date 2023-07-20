call .\venv\Scripts\activate.bat

python manage.py makemigrations authapp && ^
python manage.py makemigrations mainapp && ^
python manage.py makemigrations cartapp && ^
python manage.py makemigrations && ^
python manage.py migrate

deactivate