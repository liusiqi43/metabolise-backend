#!/usr/local/bin/python
# coding: utf-8

from normalize import tokenize, singularize, unit_normalization
from pymongo import MongoClient

import random


def parse_item(n):
    qty, unit = unit_normalization(n['nf_serving_size_qty'],
                                   n['nf_serving_size_unit'])
    name, desc = n['item_name'], n['item_description'
                                   ] if 'item_description' in n else None
    tokens = [singularize(t) for t in tokenize(name, desc)]
    return qty, unit, tokens


def get_cal_data(client):
    nutrition = client.knowledge.nutrition
    projection = ['item_name', 'item_description', 'nf_serving_size_qty',
                  'nf_serving_size_unit', 'nf_calories']

    X_cal, Y_cal = [], []
    for n in nutrition.find(
        {'nf_calories': {'$gt': 0},
         'nf_serving_size_qty': {'$gt': 0}}, projection):
        qty, unit, tokens = parse_item(n)
        if unit not in tokens:
            tokens.append(unit)
        X_cal.append(' '.join(tokens))
        Y_cal.append(n['nf_calories'] / qty)
    data_cal = zip(X_cal, Y_cal)
    random.shuffle(data_cal)

    X_cal, Y_cal = zip(*data_cal)
    return X_cal, Y_cal


def get_unit_data(client):
    nutrition = client.knowledge.nutrition
    projection = ['item_name', 'item_description', 'nf_serving_size_qty',
                  'nf_serving_size_unit', 'nf_calories']

    X_unit, Y_unit = [], []
    for n in nutrition.find(
        {'nf_calories': {'$gt': 0},
         'nf_serving_size_qty': {'$gt': 0}}, projection):
        _, unit, tokens = parse_item(n)

        X_unit.append(' '.join(tokens))
        Y_unit.append(unit)

    data_unit = zip(X_unit, Y_unit)
    random.shuffle(data_unit)

    X_unit, Y_unit = zip(*data_unit)
    return X_unit, Y_unit


if __name__ == '__main__':
    client = MongoClient()

    X_cal, Y_cal = get_cal_data(client, set([]))
    print X_cal[:10]
    print Y_cal[:10]

    X_unit, Y_unit = get_unit_data(client, set([]))
    print X_unit[:10]
    print Y_unit[:10]
