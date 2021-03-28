Установка сервиса на удаленном сервере:
1. Открыть терминал
2. Зайти на удаленный сервер путем команды:
    ssh <имя_удаленного_пользователя>@<IP_адрес_удаленного_сервера>
Ввести пароль удаленного пользователя в появившейся строке консоли
3. Установить git:
    sudo apt install git
4. Скачать проект сервиса с репозитория github, для этого ввести команду:
    git clone https://github.com/lizatish/YandexBackendSchool2021.git
Ввести логин и пароль от аккаунта github для успешного скачивания проекта.

Развертывание сервиса на удаленном сервере:
5. Установить docker:
     sudo apt-get update
     sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo \
      "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
6. Установить docker-compose
    sudo apt install docker-compose
7. Перейти в директорию проекта:
    cd YandexBackendSchool2021
8. Создать папку для хранения парамтеров запуска сервиса и базы данных и перейти в нее:
    mkdir env
    cd end
9. Создать файл конфигурации мастера:
    nano master.env
    В появивишемся окне ввести следующие параметры:
        FLASK_APP=store
        FLASK_RUN_HOST=0.0.0.0
        FLASK_RUN_PORT=8080
        FLASK_ENV=development
        DATABASE_URL=postgresql://postgres:postgres@database:5432/yandex_store
    Сохранить изменения путем последователного нажатия клавиш Ctrl+O, Ctrl+X
10. Создать файл конфигурации базы данных:
    nano database.env
    В появивишемся окне ввести следующие параметры:
        POSTGRES_HOST=database
        POSTGRES_PORT=5432
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=postgres
        POSTGRES_DB=yandex_store
    Сохранить изменения путем последователного нажатия клавиш Ctrl+O, Ctrl+X
12. Зайти в директорию проекта и собрать docker-образ:
    cd ..
    sudo docker-compose build
13. Запустить сервис:
    sudo docker-compose up

Примечания:
 - Для того, чтобы остановить сервис, необходимо нажать сочетание клавищ Ctrl+C
 - Для второго и последующего развертываний сервиса повторить пункты 7, 13.

