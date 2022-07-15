# PARSER BOT + WEB INTERFACE
VERSION 1.0.0

 * [`Demon`](./demon/README.md) - **Working with data**
 * [`Interface`](./interface/README.md) - **Single-page interface**

> [`Task`](https://kanalservis.notion.site/kanalservis/Python-82f517c516d041b8aca227f0a44ed1f1) 
> [`Sheet`](https://docs.google.com/spreadsheets/d/13k0ORwAXAQ4LwaUGfReXmJ7x0SsXpHussJQZ-abm6lI/edit#gid=0)

## Setup:
> ```shell
> # SSH
> git clone git@github.com:xristxgod/TRON-GETEWAY.git
> # HTTPS
> git clone https://github.com/xristxgod/TRON-GETEWAY.git
> ```

## Settings in .env file:
> `TELEGRAM_TOKEN` - Telegram bot token. Can be obtained here: [`@BotFather`](https://t.me/BotFather)
>
> `TELEGRAM_ADMIN_IDS` - Telegram admin chat ids. Example: 1415125,41241551 . Can be obtained here: [`@BotFather`](https://t.me/username_to_id_bot)
> 
> `DATABASE_URL` - Database url. From the database inside the container. Example: postgresql://root:root@sql_database:5432/orders_parser
> 
> `MONGODB_URL` - NoSQL Database url. From the database inside the container. Example: mongodb://root:root@nosql_database:27017
> 
> `SPREADSHEET_ID` - To work with google sheets api. The data is located inside the URL of the page with the sheet. Example: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/...`
> 
> `PAGE_NAME` - The name of the sheet. Located in the lower left corner. Example: `test_page`
> 
> `SHEET_ID` - ID of the sheet. The data is located inside the URL of the page with the sheet. `https://docs.google.com/.../edit#gid={SHEET_ID}`

## How to run:
> ```shell
> # Docker
> # Run
> docker-compose -f bot-docker-compose.yml up --build
> # Stop
> docker-compose -f bot-docker-compose.yml stop
> ```

### Screenshot of the work:
![image](https://user-images.githubusercontent.com/84931791/179219125-fd7369d3-86b9-4157-bcaf-39b6e7b2ff46.png)
