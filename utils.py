def get_monthly_payment(interest_rate, principal, durantion_yrs):
    N = durantion_yrs*12
    R = interest_rate*1.0/12
    pymt = principal * (R/(1-(1 + R)**(-N)))
    return pymt

class myLoan(object):
    def __init__(self, principal, interest_rate, duration_yrs):
        self._inital_principal = principal
        self._inital_interest_rate = interest_rate

        self._remaining_principal = principal
        self._remaining_n_payments = duration_yrs * 12
        self._current_interest_rate = interest_rate
        self._current_monthly_pymt = self.get_monthly_payment(self._current_interest_rate, self._remaining_principal, duration_yrs*12)

        self._timeline_table = self._create_timeline_table()


    def get_monthly_payment(self, interest_rate, principal, n_payments):
        N = n_payments
        R = interest_rate * 1.0 / 12
        pymt = principal * (R / (1 - (1 + R) ** (-N)))
        return pymt

    def _create_timeline_table(self):
        return {0: {"remaining_principal": self._remaining_principal,
                    "this_interest_payment": 0,
                    "this_principal_payment": 0,
                    "all_interest_paid": 0,
                    "all_principal_paid": 0,
                    "remaining_n_payments": self._remaining_n_payments}}

    def _add_month_timeline(self, nth_month, remaining_principal, this_interest_payment,
                           this_principal_payment, all_interest_paid, all_principal_paid):
        self._timeline_table[nth_month] = {
            "remaining_principal": remaining_principal,
            "this_interest_payment": this_interest_payment,
            "this_principal_payment": this_principal_payment,
            "all_interest_paid": all_interest_paid,
            "all_principal_paid": all_principal_paid,
            "remaining_n_payments": self._timeline_table[nth_month-1]["remaining_n_payments"]-1
        }
        return

    def _alter_month_timeline(self, nth_month, key, val, option=""):
        if option == "":
            return
        elif option == "replace":
            self._timeline_table[nth_month][key] = val
        elif option == "add":
            self._timeline_table[nth_month][key] += val
        elif option == "subtract":
            self._timeline_table[nth_month][key] -= val
        return

    def make_a_regular_payment(self, nth_month):
        interest_paid = self._remaining_principal*self._current_interest_rate/12
        principal_paid = min([self._remaining_principal, self._current_monthly_pymt - interest_paid])
        self._add_month_timeline(nth_month,
                                remaining_principal=self._remaining_principal-principal_paid,
                                this_interest_payment=interest_paid,
                                this_principal_payment=principal_paid,
                                all_interest_paid=self._timeline_table[nth_month-1]["all_interest_paid"]+interest_paid,
                                all_principal_paid=self._timeline_table[nth_month-1]["all_principal_paid"]+principal_paid)
        self._remaining_principal -= principal_paid

    def make_extra_payment(self, nth_month, amount):
        self._remaining_principal -= amount
        self._alter_month_timeline(nth_month, key="remaining_principal", val=self._remaining_principal, option="replace")
        self._alter_month_timeline(nth_month, key="this_principal_payment", val=amount, option="add")
        self._alter_month_timeline(nth_month, key="all_principal_paid", val=amount, option="add")

    def refinance(self, rate, remaining_payments):
        self._current_interest_rate = rate
        self._remaining_n_payments = remaining_payments
        self._current_monthly_pymt = self.get_monthly_payment(self._current_interest_rate, self._remaining_principal, self._remaining_n_payments)
        return

    def get_timeline_table(self):
        return self._timeline_table

    def get_remaining_principal(self):
        return self._remaining_principal

    def get_this_month_interest_payment(self, nth_month):
        return self.get_timeline_table()[nth_month]["this_interest_payment"]

    def get_this_month_principal_payment(self, nth_month):
        return self.get_timeline_table()[nth_month]["this_principal_payment"]

class myHouse(object):
    def __init__(self, house_price, hoa, tax_rate, yr_insurance):
        self._initial_house_price = house_price
        self._hoa = hoa
        self._tax_rate = tax_rate
        self._yr_insurance = yr_insurance

        self._current_house_price = house_price
        self._current_rent_income = 0

    def set_current_house_price(self, price):
        self._current_house_price = price

    def set_current_rent(self, rent):
        self._current_rent_income = rent

    def get_current_rent(self):
        return self._current_rent_income

    def get_monthly_cost(self):
        if self._current_rent_income == 0:
            return self._hoa + self._tax_rate*self._initial_house_price*1.0/12 + self._yr_insurance*1.0/12
        else:
            return self._hoa + self._tax_rate * self._initial_house_price * 1.0 / 12

class myInvestment(object):
    def __init__(self, income_tax_rate, myhouse, myloan):
        self._income_tax_rate = income_tax_rate
        self._house = myhouse
        self._loan = myloan
        self._assessment_deposits = {0: self._loan._inital_principal}
        self._costs = {0: 0.0}
        self._earnings = {0: 0.0}

    def update_nth_month(self, nth_month, extra_principal_payment=0, rent=0):
        # make payment
        self._loan.make_a_regular_payment(nth_month)
        if extra_principal_payment > 0:
            self._loan.make_extra_payment(nth_month, extra_principal_payment)

        # receive rent income
        if rent > 0 and rent != self._house.get_current_rent:
            self._house.set_current_rent(rent)

        self._costs[nth_month] = self._house.get_monthly_cost() + self._loan.get_this_month_interest_payment(nth_month)
        self._earnings[nth_month] = self._house.get_current_rent() + self._loan.get_this_month_interest_payment(nth_month) * self._income_tax_rate

        self._assessment_deposits[nth_month] = self._loan.get_this_month_principal_payment(nth_month)

    def simulate(self, for_n_months, extra_principal_pays={}):
        current_month = self._get_current_month()

        for i in range(current_month+1, for_n_months+1):
            self.update_nth_month(i, extra_principal_payment= extra_principal_pays[i] if i in extra_principal_pays else 0, rent = self._house.get_current_rent)
        return

    def refinance(self):
        return

    def _get_current_month(self):
        return max(self._assessment_deposits.keys())

    def see_my_assessment_deposits(self, nth_month=None):
        if not nth_month or nth_month not in self._assessment_deposits:
            return sum(self._assessment_deposits.values())
        else:
            return self._assessment_deposits.get(nth_month)

    def see_my_costs(self, nth_month=None):
        if not nth_month or nth_month not in self._costs:
            return sum(self._costs.values())
        else:
            return self._costs.get(nth_month)

    def see_my_earnings(self, nth_month=None):
        if not nth_month or nth_month not in self._earnings:
            return sum(self._earnings.values())
        else:
            return self._earnings.get(nth_month)