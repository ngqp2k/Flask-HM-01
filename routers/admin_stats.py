from app import app, db
from flask import render_template, request, redirect, url_for
import datetime


import models as models

class StatsModel:
    def __init__(self, room_type, amount, rate, qty, no):
        self.no = no
        self.room_type = room_type
        self.amount = amount
        self.qty = qty
        self.rate = rate


@app.route('/test-stats', methods=['GET'])
def test_stats_page():

    labels_1 = ['Quý 1', 'Quý 2', 'Quý 3', 'Quý 4']
    labels_2 = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']

    # data_11 = [22000000, 15500000, 11000000, 45000000]
    # data_12 = [40000000, 35000000, 22000000, 66000000]
    # data_13 = [33000000, 22000000, 42000000, 59000000]
    data_2 = [22000000, 15500000, 11000000, 45000000, 22000000, 15500000, 11000000, 45000000, 22000000, 15500000, 11000000, 45000000]

    # get random number between 10 and 90
    import random
    data_11 = [random.randint(10, 90) * 1000000 for i in range(12)]
    data_12 = [random.randint(10, 90) * 1000000 for i in range(12)]
    data_13 = [random.randint(10, 90) * 1000000 for i in range(12)]

    data = [data_11, data_12, data_13]

    stats_models = []
    stats1 = StatsModel('Tiêu chuẩn', sum(data_11), 42, 80, 1)
    stats2 = StatsModel('Cao cấp', sum(data_12), 15, 15, 2)
    stats3 = StatsModel('Đặc biệt', sum(data_13), 3, 5, 3)
    stats_models.append(stats1)
    stats_models.append(stats2)
    stats_models.append(stats3)

    print(f'ngqp2k debug: {request.method}')

    room_types = [room_type.name for room_type in models.RoomType.query.all()]

    # if request.method == 'GET':
    #     stats_type = request.args.get('stats_type')

    #     stats_time = request.args.get('stats_time')

    #     # if stats_time is not None:
    #         # month = stats_time.split('-')[1]
    #         # year = stats_time.split('-')[0]

    #         # invoices = models.Invoice.query.filter_by(month=month, year=year).all()

    #         # print(f'ngqp2k debug: {stats_type} {month} {year} {type(stats_type)} {type(month)} {type(year)} ')

    #     if stats_type == '1':
    #         return render_template('stats-test.html', labels=labels_1, data11=data_11, data12=data_12, stats_type=stats_type)
    #     elif stats_type == '2':
    #         return render_template('stats-test.html', labels=labels_2, data=data_2, stats_type=stats_type)

    return render_template('stats-test.html'
                           , labels=labels_2
                           , data=data
                           , room_types=room_types
                           , stats_models=stats_models)


@app.route('/test-stats-1', methods=['GET', 'POST'])
def test_stats_1_page(num = 0):
    stats_models = []

    room_types = models.RoomType.query.all()

    idx = 1;
    for room_type in room_types:
        print(f'ngqp2k debug: {room_type.name}')
        stats_models.append(StatsModel(room_type.name, 0, 0, 0, idx))
        idx += 1

    if request.method == 'GET':
        stats_time = request.args.get('stats_time')

        if stats_time is None:
            stats_time = datetime.datetime.now().strftime("%Y-%m")

        month = stats_time.split('-')[1]
        invoices = models.Invoice.query.all()
        idx = 0
        for invoice in invoices:
            if (invoice.created_date.month == int(month)):
                idx += 1
                for stats in stats_models:
                    if invoice.booking_room.room.room_type.name == stats.room_type:
                        stats.amount += invoice.total_price
                        stats.qty += 1


    return render_template('stats-test-1.html'
                           , room_types=room_types
                           , stats_models=stats_models
                           , stats_time=stats_time)


