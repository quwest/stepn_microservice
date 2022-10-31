from flask import Flask, request
from flask_restful import Resource, Api
from DB import DB
from werkzeug.exceptions import default_exceptions, Aborter

from SneakerFind import SneakerFind
from Exceptions import IncorrectArgument, IncorrectId, InauthorizedAccount
from StepnActions import StepnActions

app = Flask(__name__)
api = Api(app)
default_exceptions[203] = IncorrectArgument
default_exceptions[205] = IncorrectId
abort = Aborter()
stepn_actions_obj = StepnActions()

class GetTenSneakers(Resource):
    accepted_request_args = ['project']
    db = DB()
    ids = db.get_all_ids()

    def get(self):
        for arg in request.args:
            if arg not in self.accepted_request_args:
                return abort(203)

        project_id = request.args.get('project')
        try:
            project_id = int(project_id)
        except:
            return 'incorrect project'
        if project_id not in self.ids:
            print(project_id)
            return abort(205)
        sneakers = stepn_actions_obj.get_first_ten_sneakers(project_id)

        return sneakers

class GetAccInf(Resource):
    accepted_request_args = ['chain']
    accepted_chains = ['bnb','BNB','sol','SOL','eth','ETH']

    def get(self):
        for arg in request.args:
            if arg not in self.accepted_request_args:
                return abort(203)


        chain = request.args.get('chain')
        if chain not in self.accepted_chains:
            return 'incorrect chain'
        if chain in ['SOL', 'sol']:
            chain = 103
        if chain in ['BNB', 'bnb']:
            chain = 104
        if chain in ['ETH', 'eth']:
            chain = 101

        sneakers_info = stepn_actions_obj.get_shoe_list(chain)
        acc_info = stepn_actions_obj.get_acc_inf(chain)

        return [acc_info, sneakers_info]

class GetSneakersInfo(Resource):
    accepted_request_args = ['project', 'otd']
    db = DB()
    ids = db.get_all_ids()

    def get(self):
        for arg in request.args:
            if arg not in self.accepted_request_args:
                return abort(203)

        project_id = request.args.get('project')
        try:
            project_id = int(project_id)
        except:
            return 'incorrect project'
        if project_id not in self.ids:
            return abort(205)

        otd = request.args.get('otd')
        try:
            otd = int(otd)
        except:
            return 'incorrect otd'


        find_sneaker_obj = SneakerFind(project_id)
        while True:
            try:
                order_id, _ = find_sneaker_obj.find_sneakers_by_otd(otd, stepn_actions_obj.sessionID)
            except InauthorizedAccount:
                stepn_actions_obj.log_in()
            else:
                break
        order_inf = stepn_actions_obj.get_order_inf(order_id)

        return order_inf

class BuySneaker(Resource):
    accepted_request_args = ['project', 'otd']
    db = DB()
    ids = db.get_all_ids()

    def get(self):
        for arg in request.args:
            if arg not in self.accepted_request_args:
                return abort(203)

        project_id = request.args.get('project')
        try:
            project_id = int(project_id)
        except:
            return 'incorrect project'
        if project_id not in self.ids:
            return abort(205)

        otd = request.args.get('otd')
        try:
            otd = int(otd)
        except:
            return 'incorrect otd'

        find_sneaker_obj = SneakerFind(project_id)
        while True:
            try:
                order_id, price = find_sneaker_obj.find_sneakers_by_otd(otd, stepn_actions_obj.sessionID)
            except InauthorizedAccount:
                stepn_actions_obj.log_in()
            except Exception as e:
                print(e)
                return "stepn doesn't have this order"
            else:
                break

        message = stepn_actions_obj.buy_sneaker(order_id, price)

        return message

class CheckSold(Resource):
    accepted_request_args = ['otd']

    def get(self):
        for arg in request.args:
            if arg not in self.accepted_request_args:
                return abort(203)

        otd = request.args.get('otd')
        try:
            otd = int(otd)
        except:
            return 'incorrect otd'

        is_sold = stepn_actions_obj.check_sold(otd)

        if is_sold:
            return 'sold'
        else:
            return 'not sold'



api.add_resource(GetTenSneakers, '/LastSneakers', endpoint='lastsneakers')
api.add_resource(GetAccInf, '/AccInfo', endpoint='accinfo')
api.add_resource(GetSneakersInfo, '/SneakersInfo', endpoint='sneakersinfo')
api.add_resource(BuySneaker, '/BuySneakers', endpoint='buysneakers')
api.add_resource(CheckSold, '/CheckSold', endpoint='check_sold')

if __name__ == '__main__':
    app.run(debug=True)