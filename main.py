from time import sleep
import os
import discord
import json
import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheetTrans = client.open("Discord Crypto").worksheet("Транзакции")

driver = webdriver.Chrome('chromedriver\chromedriver')
driver.get("https://discord.com/channels/793500828832235520/800044040728739860")
driver.find_element_by_name('email').send_keys("doronin_alex@yahoo.com")
driver.find_element_by_name('password').send_keys("crypto_bot")
sleep(3)
driver.find_element_by_name('password').send_keys(Keys.ENTER)
msg_xpath = '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div/div'

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    with open("price.txt", "r") as text:
        price = int(text.read())
    now = datetime.datetime.now()
    current_time = (now + datetime.timedelta(hours=3)).strftime("%d/%m/%y %H:%M")
    username = str(message.author)
    myid = "<@!882707904749244416>"
    # сообщение
    msg = message.content

    if msg.startswith("-trade "):
        value_trade = msg.split("-trade ")[1]
        value_trade_list = value_trade.split(" ")
        trade_type = value_trade_list[0]
        number_coin = int(value_trade_list[1])
        total_cost = price * number_coin
        if trade_type == "buy" or trade_type == "купить" or trade_type == "Buy" or trade_type == "Купить":
            driver.find_element_by_xpath(msg_xpath).send_keys(f"-remove-money {username} {total_cost}")
            driver.find_element_by_xpath(msg_xpath).send_keys(Keys.ENTER)
            sleep(3)
            driver.find_element_by_xpath(msg_xpath).send_keys(f"-add-money {myid} {total_cost}")
            driver.find_element_by_xpath(msg_xpath).send_keys(Keys.ENTER)
            with open("price.txt", "w") as text:
                text.write(price + number_coin)

        elif trade_type == "sell" or trade_type == "продать" or trade_type == "Sell" or trade_type == "Продать":
            driver.find_element_by_xpath(msg_xpath).send_keys(f"-with {total_cost}")
            driver.find_element_by_xpath(msg_xpath).send_keys(Keys.ENTER)
            sleep(3)
            driver.find_element_by_xpath(msg_xpath).send_keys(f"-give-money {username} {total_cost}")
            driver.find_element_by_xpath(msg_xpath).send_keys(Keys.ENTER)
            with open("price.txt", "w") as text:
                text.write(price - number_coin)

        insertTrans = [username, trade_type, price, number_coin, total_cost]
        sheetTrans.append_row(insertTrans)




client.run("ODg1MjE4MjcyNjc1NTI0NjA4.YTj1wg.uNvFOot_n3X1ESJ4H2z8MrkT2ZI")