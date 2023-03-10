from flask import Flask, jsonify
import requests
import math
import time, datetime
from datetime import datetime
import os
from pathlib import Path

app = Flask(__name__)

detailed_receipts = []
identified_receipts = {"receipts": []}


########################################
### ROUTES
########################################


@app.route('/json_test')
def endpoint():
    # return jsonify({"retailer": "Walgreens","purchaseDate": "2022-01-02","purchaseTime": "08:13","total": "2.65","items": [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"},{"shortDescription": "Dasani", "price": "1.40"}]})
    return jsonify({
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {
                "shortDescription": "Gatorade",
                "price": "2.25"
            }, {
                "shortDescription": "Gatorade",
                "price": "2.25"
            }, {
                "shortDescription": "Gatorade",
                "price": "2.25"
            }, {
                "shortDescription": "Gatorade",
                "price": "2.25"
            }
        ],
        "total": "9.00"
    })


@app.route('/receipts/process')
def receipt_processing():
    function_receipts, json_item = process_receipts()
    print(type(detailed_receipts))
    print(detailed_receipts)

    return json_item


@app.route('/receipts/<string:x>/points', methods=['GET'])
def get_points(x):
    global detailed_receipts
    for item in detailed_receipts:
        if item[0] == {'id': x}:
            ############################
            # LOCAL VARIABLES
            ############################
            dict_1 = item[1]
            retailer = dict_1['retailer']
            total = dict_1['total']
            receipt_items = dict_1['items']
            purch_date = dict_1['purchaseDate']
            purch_time = dict_1['purchaseTime']

            name_points = 0
            totals_points = 0
            mult_twofive = 0
            item_count = 0
            descrip_points = 0
            date_points = 0
            time_points = 0
            grand_total = 0

            ############################
            # Determine total possible
            # points
            ############################

            # points for alphanumeric
            #####
            print(retailer)
            name_points = alnum_counter(retailer)
            print("name points: " + str(name_points) + "\n")

            # points for round dollar amount
            #####
            if float(total).is_integer():
                totals_points = 50
            print("total points: " + str(totals_points) + "\n")

            # multiple of 0.25
            #####
            if float(total) % 0.25 == 0:
                mult_twofive = 25
            print("points for 0.25 multiplicity: " + str(mult_twofive) + "\n")

            # points for every two items
            #####
            item_count = math.floor(len(receipt_items) / 2) * 5
            print("Item pair points: " + str(item_count) + "\n")

            # points for short description formula
            #####
            descrip_points = short_descrip_points(receipt_items)
            print("description points: " + str(descrip_points) + "\n")

            # purchase date odd points
            #####
            even_odd = purch_date[8:]
            result = int(even_odd[0] + even_odd[1])
            if result % 2 != 0:
                date_points = 6
            print("purchase date points: " + str(date_points) + "\n")

            # time in range points
            #####
            receipt_time = datetime.strptime(purch_time, '%H:%M').time()
            # receipt_time = purch_time.time()
            if time_in_range(receipt_time):
                time_points = 10
            print("time points: " + str(time_points) + "\n")

        grand_total = sum(
            [name_points, totals_points, mult_twofive, item_count, descrip_points, date_points, time_points])

    return jsonify({"points": grand_total})


########################################
### APP FUNCTIONS
########################################


def process_receipts():
    global identified_receipts
    global detailed_receipts

    baseurl = "http://127.0.0.1:5000/"
    request = requests.get(baseurl + "json_test").json()

    print(type(request))
    serial = serial_maker()
    json_item = {'id': serial}

    vari = detailed_receipts
    # request['id']=serial
    vari.append(tuple((json_item, request)))
    print(vari)

    identified_receipts['receipts'].append(request)

    print(identified_receipts)

    return vari, json_item


def alnum_counter(str):
    alnum_points = 0
    for item in str:
        if item.isalnum():
            alnum_points += 1
    return alnum_points


def short_descrip_points(a_list):
    point_total = 0
    count = 0
    descrip_list = [sub['shortDescription'] for sub in a_list]
    price_list = [sub['price'] for sub in a_list]

    for descrip in descrip_list:
        descrip = descrip.strip()
        str_count = len(descrip)
        if str_count % 3 == 0:
            price = float(price_list[count])
            points = math.ceil(price * 0.2)
            point_total += points
        count += 1
    return point_total


def time_in_range(time):
    result = False
    start = datetime.strptime('14:00', '%H:%M').time()
    end = datetime.strptime('16:00', '%H:%M').time()
    if start <= time <= end:
        result = True
    return result


import secrets


def serial_maker():
    seg_1 = secrets.token_hex(4)
    seg_2 = secrets.token_hex(2)
    seg_3 = secrets.token_hex(2)
    seg_4 = secrets.token_hex(2)
    seg_5 = secrets.token_hex(6)

    serial_output = seg_1 + "-" + seg_2 + "-" + seg_3 + "-" + seg_4 + "-" + seg_5
    return serial_output


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
