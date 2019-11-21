#Project for cataloging my YuGiOh card collection and getting accurate pricing on it
#Thanks to http://yugiohprices.com/ for the pricing and https://yugiohprices.docs.apiary.io/#reference for the API which made this whole thing a million times easier
#Created by mason@masonjon.es

import requests
import json
import csv
import sys
import argparse, os
from datetime import date

BASE_URL = 'https://yugiohprices.com/api/price_for_print_tag'
WRITE = 'w'
APPEND = 'a'

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
# CURRENT_DIR = os.getcwd()
DEFAULT_INPUT_DIR = os.path.join(CURRENT_DIR, "input_files")
DEFAULT_OUTPUT_DIR = os.path.join(CURRENT_DIR, "output_files")
DEFAULT_OUTPUT = 'Inventory as of %s.csv'


class YuGiUtils():
    def __init__(self):
        pass

    # Returns a list of all files within a directory
    def get_all_files(self, input_files):
        if os.path.isfile(input_files):
            all_files = [input_files]
        else:
            all_files = [os.path.join(input_files, f) for f in os.listdir(input_files)
                         if os.path.isfile(os.path.join(input_files, f))]
        return all_files

    # Returns a list of all cards within a file/directory
    def get_cards(self, input_files):
        all_files = self.get_all_files(input_files)
        listOfCards = list()
        for f in all_files:
            with open(f, "r") as infile:
                listOfCards += infile.readlines()
        return listOfCards

    def parse_card(self, input_files, output_file, out_type):
        listOfCards = self.get_cards(input_files)
        l = len(listOfCards)

        # If no output_file, use default format
        if output_file is None:
            today = date.today()
            output_file = os.path.join(DEFAULT_OUTPUT_DIR, DEFAULT_OUTPUT % today)

        with open(output_file, out_type, newline='') as output:
            fieldnames = ["CardID", "Occurrences", "Name", "Card Type", "Property", "Family", "Type", "Set Name",
                          "Print Tag", "Rarity", "Average Price", "Low Price", "Total Average Price", "Total Low Price",
                          "7 Day Shift", "30 Day Shift", "6 Month Shift", "Year Shift"]
            d_writer = csv.DictWriter(output, fieldnames=fieldnames)

            if out_type is WRITE:
                d_writer.writeheader()

            i = 1
            for card in listOfCards:
                curr_row = dict()

                cardSplit = card.split(',')
                curr_row["CardID"] = cardSplit[0]
                curr_row["Occurrences"] = int(cardSplit[1].rstrip())
                cardDetail = self.get_card_details(curr_row["CardID"])

                data = cardDetail["data"]
                curr_row["Name"] = data["name"]
                curr_row["Card Type"] = data["card_type"]
                curr_row["Property"] = data["property"]
                curr_row["Family"] = data["family"]
                curr_row["Type"] = data["type"]

                price_data = data["price_data"]
                curr_row["Set Name"] = price_data["name"]
                curr_row["Print Tag"] = price_data["print_tag"]
                curr_row["Rarity"] = price_data["rarity"]

                prices = price_data["price_data"]["data"]["prices"]
                curr_row["Average Price"] = prices["average"]
                curr_row["Low Price"] = prices["low"]
                curr_row["Total Average Price"] = round(curr_row["Occurrences"]  * curr_row["Average Price"], 2)
                curr_row["Total Low Price"] = round(curr_row["Occurrences"]  * curr_row["Low Price"], 2)
                curr_row["7 Day Shift"] = round(prices["shift_7"], 2)
                curr_row["30 Day Shift"] = round(prices["shift_30"], 2)
                curr_row["6 Month Shift"] = round(prices["shift_180"], 2)
                curr_row["Year Shift"] = round(prices["shift_365"], 2)

                d_writer.writerow(curr_row)

                sys.stdout.write("\r%d out of %d" % (i, l))
                sys.stdout.flush()
                i = i + 1
        sys.stdout.write("\nComplete!")

    def get_card_details(self, card_id):
        url = BASE_URL + "/" + card_id
        response = requests.get(url)
        return json.loads(response.text)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input_files", default=DEFAULT_INPUT_DIR, help="Input file or directory")
    parser.add_argument("-o", "--output", dest="output_file", default=None, help="Output file")
    parser.add_argument("-w", "--write", dest="write", action="store_true", help="Write over output file")
    parser.add_argument("-a", "--append", dest="append", action="store_true", help="Append to output file")
    args = parser.parse_args()

    if args.write and not args.append:
        out_type = WRITE
    elif args.append and not args.write:
        out_type = APPEND
    else:  # default output write type
        out_type = APPEND

    yugi_utils = YuGiUtils()
    yugi_utils.parse_card(input_files=args.input_files, output_file=args.output_file, out_type=out_type)


if __name__ == '__main__':
    run()

# Ex. write to file
    #  python YuGiOh.py -w
# Ex. append to file
    #  python YuGiOh.py -a
