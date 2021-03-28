## Установка сервиса на удаленном сервере

1. Открыть терминал
2. Зайти на удаленный сервер путем команды:
   ```bash
   ssh <имя_удаленного_пользователя>@<IP_адрес_удаленного_сервера>
      ```
   Ввести пароль удаленного пользователя в появившейся строке консоли
3. Установить git:
   ```bash
   sudo apt install git
   ```
4. Скачать проект сервиса с репозитория github, для этого ввести команду:
   ```bash
   git clone https://github.com/lizatish/YandexBackendSchool2021.git
   ```
   Ввести логин и пароль от аккаунта github для успешного скачивания проекта.

## Развертывание сервиса на удаленном сервере

5. Установить docker:
     ```bash
    sudo apt-get update
   
    sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
   
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o
    /usr/share/keyrings/docker-archive-keyring.gpg
   
    echo \ 
   "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   
    sudo apt-get update 
    sudo apt-get install docker-ce docker-ce-cli containerd.io    
    ```

6. Установить docker-compose:
   ```bash
   sudo apt install docker-compose
   ```
7. Перейти в директорию проекта:
   ```bash
    cd YandexBackendSchool2021
    ```
8. Создать директорию для хранения параметров запуска сервиса и базы данных и перейти в нее:
    ```bash   
    mkdir env cd end
    ```
9. Создать файл конфигурации мастера:
   ```bash   
   nano master.env 
   ```
   В появивишемся окне ввести следующие параметры:
   ```python
    FLASK_APP=store 
    FLASK_RUN_HOST=0.0.0.0
    FLASK_RUN_PORT=8080
    FLASK_ENV=development
    DATABASE_URL=postgresql://postgres:postgres@database:5432/yandex_store 
   ```
   Сохранить изменения путем последователного нажатия клавиш Ctrl+O, Ctrl+X
10. Создать файл конфигурации базы данных:
     ```bash  
    nano database.env
    ```
     В появивишемся окне ввести следующие параметры:
     ```python
    POSTGRES_HOST=database
    POSTGRES_PORT=5432
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=yandex_store
    ```
    Сохранить изменения путем последователного нажатия клавиш Ctrl+O, Ctrl+X
12. Зайти в директорию проекта и собрать docker-образ:
    ```bash 
    cd .. sudo docker-compose build
    ```
13. Запустить сервис:
    ```bash  
    sudo docker-compose up
    ```

### Примечания:

- После перезапуска компьютера сервис будет работать в фоновом режиме на порту 8080, повторный запуск не требуется.

