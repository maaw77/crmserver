# Сервис учета горюче-смазочных материалов
Микросервис, предоставляющий данные учета горюче-смазочных материалов в JSON-формате.
## Запуск
1. Установить docker 
2. В папке с проектом создать файл `.env`, содержащий параметры соединения с сервером PostgreSQL.<br>
Пример:
```text
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=************
HOST_DB=db
PORT_DB=5432
```
3. В папке с проектом выполнить команды
```commandline
docker build -t crmserver .
```
```commandline
docker run --network=crm_default --name=crmserver --rm -it -p 8080:8080 crmserver
```
## Описание API
Сервис доступен без авторизации пользователя.
### 1. Список конечных точек
Get-request: `http://localhost:8080/`.<br>
Response: 

- status code - 200; <br>
- body -
```json 
{"urls": ["/gsm_table", "/tank_table", 
          "/sheet_table", "/azs_table", 
          "/exchange_table", "/remains_table"]}
```
### 2. Таблица «Прием»
Get-request: `http://localhost:8080/gsm_table/{date}`, где date = _YYYY-MM-DD_.<br>
Response:<br> 
- status code - 200; <br>
- body - 
```json
        [{"dt_receiving": "2024-06-01", 
          "dt_crch": "", 
          "site": "SITE_1", 
          "income_kg": 26442.70, 
          "operator": "OPERATOR_1", 
          "provider": "PROVIDER_1", 
          "contractor": "CONTRACTOR_1", 
          "license_plate": "A902RUS", 
          "status": "Uploaded", 
          "been_changed": false}, 
         {"dt_receiving": "2024-06-01", 
          "dt_crch": "", 
          "site": "SITE_2", 
          "income_kg": 562.20, 
          "operator": "OPERATOR_2", 
          "provider": "PROVIDER_2", 
          "contractor": "CONTRACTOR_2", 
          "license_plate": "A342RUS", 
          "status": "Uploaded", 
          "been_changed": false},
          ...]
```
### 3. Таблица «Выдача в АТЗ»
Get-request: `http://localhost:8080/tank_table/{date}`, где date = _YYYY-MM-DD_.<br>
Response:<br> 
- status code - 200; <br>
- body - 
```json
        [{"dt_giveout": "2024-06-01", 
          "dt_crch": "", 
          "site": "SITE_1", 
          "onboard_num": "376 (К35456) АТЗ КАМАЗ 43118", 
          "dest_site": "SITE_2", 
          "given_kg": 3706.0, 
          "status": "Uploaded", 
          "been_changed": false}, 
         {"dt_giveout": "2024-06-01", 
         "dt_crch": "",
         "site": "SITE_3", 
         "onboard_num": "786(К124) АТЗ КАМАЗ 987", 
         "dest_site": "SITE_34", 
         "given_kg": 3706.0, 
         "status": "Uploaded", 
         "been_changed": false},
         ...]
```
### 4. Таблица «Выдача из АТЗ»
Get-request: `http://localhost:8080/sheet_table/{date}`, где date = _YYYY-MM-DD_.<br>
Response:<br> 
- status code - 200; <br>
- body - 
```json
        [{"dt_giveout":"2024-06-01",
          "dt_crch":"",
          "site":"SITE_0",
          "atz":"АТЗ — 90260",
          "give_site":"SITE_3",
          "given_litres":1805,
          "given_kg":1487.30,
          "status":"Uploaded",
          "been_changed":false}, 
         {"dt_giveout":"2024-06-01",
          "dt_crch":"2024-06-04",
          "site":"SITE_4",
          "atz":"АТЗ - 90260",
          "give_site":"SITE_9",
          "given_litres":4505,
          "given_kg":1487.30,
          "status":"Uploaded",
          "been_changed":false},
          ...]
```
### 5. Таблица «Выдача из ТРК»
Get-request: `http://localhost:8080/azs_table/{date}`, где date = _YYYY-MM-DD_.<br>
Response:<br> 
- status code - 200; <br>
- body - 
```json
        [{"dt_giveout": "2024-06-01", 
          "dt_crch": "", 
          "site": "SITE_2", 
          "storekeeper": "SROEKEEPER_88", 
          "counter_azs_bd": 0.0, 
          "counter_azs_ed": 170.0, 
          "given_litres": 170.0, 
          "given_kg": 127.31, 
          "status": "Uploaded", 
          "been_changed": false},
         {"dt_giveout": "2024-06-01", 
          "dt_crch": "", 
          "site": "SITE_55", 
          "storekeeper": "SROEKEEPER_99", 
          "counter_azs_bd": 0.0, 
          "counter_azs_ed": 170.0, 
          "given_litres": 170.0, 
          "given_kg": 127.31, 
          "status": "Uploaded", 
          "been_changed": false},
          ...]
```
### 6. Таблица «Обмен между резервуарами»
Get-request: `http://localhost:8080/exchange_table/{date}`, где date = _YYYY-MM-DD_.<br>
Response:<br> 
- status code - 200; <br>
- body - 
```json
        [{"dt_change":"2024-06-01",
          "dt_crch":"",
          "site":"SITE_32",
          "operator":"OPERATOR_99",
          "tanker_in":"TANKER №8 ",
          "tanker_out":"TANKER №5)",
          "litres":26204,
          "been_changed":false,
          "status":"Uploaded"}, 
         {"dt_change":"2024-06-01",
         "dt_crch":"2024-06-02",
          "site":"SITE_5",
          "operator":"OPERATOR_32",
          "tanker_in":"TANKER №18 ",
          "tanker_out":"TANKER №15)",
          "litres":878756,
          "been_changed":false,
          "status":"Uploaded"},
          ...]
```
### 7. Таблица «Снятие остатков»
Get-request: `http://localhost:8080/remains_table/{date}`, где date = _YYYY-MM-DD_.<br>
Response:<br> 
- status code - 200; <br>
- body - 
```json
        [{"dt_inspection": "2024-06-01", 
          "site": "SITE_22", 
          "inspector": "INSPECTOR_33", 
          "tanker_num": "TANKER- 90038", 
          "remains_kg": 0.0, 
          "fuel_mark": "FUEL 95", 
          "status": "Uploaded"},
         {"dt_inspection": "2024-06-01",
          "site": "SITE_23", 
          "inspector": "INSPECTOR_1",
          "tanker_num": "TANKER- 97887", 
          "remains_kg": 183.0, 
          "fuel_mark": "FUEL 95", 
          "status": "Uploaded"},
          ...]
 ```
