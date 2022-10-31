from StepnActions import StepnActions
from SneakerFind import SneakerFind


stepn_actions = StepnActions()
sneakers = stepn_actions.get_first_ten_sneakers(41)
print(len(sneakers))
print(sneakers)
# stepn_actions.get_shoe_list(104)
#
# find_sneaker_obj = SneakerFind(32)
#
#
#
# otd = 413766824
# order_id, price = find_sneaker_obj.find_sneakers_by_otd(otd,session_id)
# print(order_id)
# data = stepn_actions.get_order_inf(order_id)
# print(repr(data))
# {"code":0}