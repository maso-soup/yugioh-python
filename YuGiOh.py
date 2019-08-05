#Project for cataloging my YuGiOh card collection and getting accurate and live pricing on it
#Thanks to http://yugiohprices.com/ for the pricing and https://yugiohprices.docs.apiary.io/#reference for the API which made this whole thing a million times easier
#Created by mason@masonjon.es

import requests
import json
import csv
from datetime import date

input=open("YuGiOh Card Input List.txt", "r")
if input.mode == 'r':
    listOfCards = input.readlines()

today = date.today()
outputFile = 'Inventory as of %s.csv' % today

with open(outputFile, 'a') as output:
    row = ["CardID", "Occurences", "Name", "Card Type", "Property", "Family", "Type", "Set Name", "Print Tag", "Rarity", "Average Price", "High Price", "Low Price", "Current Shift", "7 Day Shift", "30 Day Shift", "6 Month Shift", "Year Shift", "Last Updated"]
    writer = csv.writer(output)
    writer.writerow(row)

    for card in listOfCards:


        row = []
        cardSplit = card.split(',')
        cardID = cardSplit[0]
        cardOccurences = cardSplit[1].rstrip()

        url = "https://yugiohprices.com/api/price_for_print_tag/"+cardID

        response = requests.get(url)
        cardDetail = json.loads(response.text)

        #Add in total price with occurences
        #cardID is first
        occurences = cardOccurences
        name = cardDetail["data"]["name"]
        card_type = cardDetail["data"]["card_type"]
        property = cardDetail["data"]["property"]
        family = cardDetail["data"]["family"]
        type = cardDetail["data"]["type"]
        set_name = cardDetail["data"]["price_data"]["name"]
        print_tag = cardDetail["data"]["price_data"]["print_tag"]
        rarity = cardDetail["data"]["price_data"]["rarity"]
        average_price = cardDetail["data"]["price_data"]["price_data"]["data"]["prices"]["average"]
        high_price = cardDetail["data"]["price_data"]["price_data"]["data"]["prices"]["high"]
        low_price = cardDetail["data"]["price_data"]["price_data"]["data"]["prices"]["low"]
        #format the decimals for shift
        current_shift = cardDetail["data"]["price_data"]["price_data"]["data"]["prices"]["shift"]
        shift_7 = cardDetail["data"]["price_data"]["price_data"]["data"]["prices"]["shift_7"]
        shift_30 = cardDetail["data"]["price_data"]["price_data"]["data"]["prices"]["shift_30"]
        shift_180 = cardDetail["data"]["price_data"]["price_data"]["data"]["prices"]["shift_180"]
        shift_365 = cardDetail["data"]["price_data"]["price_data"]["data"]["prices"]["shift_365"]
        updated_at = cardDetail["data"]["price_data"]["price_data"]["data"]["prices"]["updated_at"]

        row = [cardID, occurences, name, card_type, property, family, type, set_name, print_tag, rarity, average_price, high_price, low_price, current_shift, shift_7, shift_30, shift_180, shift_365, updated_at]

        writer.writerow(row)

#Try writing last row with formula for sum of occurences and total price

output.close()
