import utils
from utils import *

# stable
property_tax_rate = 1.0/100 * 1
income_tax_rate = 1.0/100 * 4
interest_rate = 1.0/100 * 4.5
yr_insurance = 800


# configurable
loan_yrs = 30
house_price = 700000
hoa = 500
down_payment = 120000
potential_rent = 3000
yr_increase = 0.01 * 25

house = myHouse(house_price, hoa, property_tax_rate, yr_insurance)
loan = myLoan(house_price-down_payment, interest_rate, loan_yrs)
investment = myInvestment(income_tax_rate, house, loan)

# simulation
events_pay_extra = {24: 10000, 60: 20000}
events_rent_it_out = {(61, 120): 3000, (121, 180): 3300}


investment.simulate(24)

print "In Total:"
print investment.see_my_costs()
print investment.see_my_assessment_deposits()
print investment.see_my_earnings()
print "my cash balance is: ", investment.see_my_earnings() - investment.see_my_costs()
print "my assessment deposits so far is: ", investment.see_my_assessment_deposits()


print "\nFor each month:"
for n in range(0, 24):
    print "\nmonth = ", n
    print "my cash balance for this month is: ", investment.see_my_earnings(n) - investment.see_my_costs(n)
    print "my assessment deposits this month is: ", investment.see_my_assessment_deposits(n)


# rent_incomes = {}
# deposits = {}
# costs = {}
#
# for n in range(1, loan_yrs*12+1):
#     ## making payments
#     if loan.get_remaining_principal() > 0:
#         ## a regular payment
#         loan.make_a_regular_payment(n)
#         ## pay extra payment
#         if n in events_pay_extra:
#             amount = events_pay_extra[n]
#             loan.make_extra_payment(amount, n)
#
#     ## get rental payment
#     for k, rent in events_rent_it_out.items():
#         if k[0] <= n <= k[1]:
#             house.set_current_rent(rent)
#             if n in rent_incomes:
#                 rent_incomes[n] += rent
#             else:
#                 rent_incomes[n] = rent
#
#     print "\n", n, "th month:"
#     if n in loan.get_timeline_table():
#         deposits[n] = loan.get_timeline_table()[n]["this_principal_payment"]
#         costs[n] = loan.get_timeline_table()[n]["this_interest_payment"] + house.get_monthly_cost()
#     else:
#         deposits[n]=0
#         costs[n] = house.get_monthly_cost()
#     rent_incomes[n] = house.get_current_rent()
#
#     print "this month:"
#     print "    deposite=",deposits[n], "cost=",costs[n], "income=",rent_incomes[n], "net flow=",rent_incomes[n]-costs[n]
#     print "    total_net_flow=", sum(rent_incomes.values())-sum(costs.values()), "total_deposit=", sum(deposits.values())