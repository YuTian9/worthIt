def get_monthly_payment(interest_rate, principal, durantion_yrs):
    N = durantion_yrs*12
    R = interest_rate*1.0/12
    pymt = principal * (R/(1-(1 + R)**(-N)))
    return pymt


class myHousePurchase(object):

    def __init__(self, house_price, hoa, tax_rate, yr_insurance, loan_principal, loan_annual_rate, loan_yrs):

        self.house_price = house_price
        self.rental = 0

        # simplify it, hoa, tax and insurance don't change
        self._hoa = hoa
        self._tax_rate = tax_rate
        self._yr_insurance = yr_insurance
        self._monthly_hoa = self._hoa
        self._monthly_tax = self._tax_rate*self._house_price/12
        self._monthly_insurance = self._yr_insurance/12

        self._loan_principal = loan_principal
        self._loan_annual_rate = loan_annual_rate
        self._loan_yrs = loan_yrs
        self._monthly_payment = self._loan_principal * \
                                (self._loan_annual_rate/12 / (1 - (1 + self._loan_annual_rate/12)**(-self._loan_yrs * 12)))

        self.big_map = self.init_big_map()
        self.loan_left = self._loan_principal

    def init_big_map(self):
        return {0: {0: self.get_month_data(0, 0)}}

    def update_house_price(self, new_val): self._house_price = new_val

    def update_rental(self, new_val): self._rental = new_val

    def monthly_update(self, y, m, house_price=None, rental=None):
        if house_price:
            self.update_house_price(house_price)
        if rental:
            self.update_rental(rental)
        self.big_map[y][m] = self.get_month_data(y, m)

    def get_month_data(self, y, m):
        interest_paid = self.loan_left*self._loan_annual_rate/12
        principal_paid = self._monthly_payment - interest_paid
        if y!=0 or m!=0: self.loan_left -= principal_paid

        if y==0 and m==0:
            ret = {"value": self.house_price, "rental_income": self.rental, "principal_pay": 0, "interest_pay": 0}
        else:
            ret = {"value": self.house_price, "rental_income": self.rental, "principal_pay": principal_paid,
               "interest_pay": interest_paid}
        return ret

    def now_accumulated_principal(self):
        ret = 0
        for y, m_dict in self._big_map.items():
            for m, month_dict in m_dict.items():
                ret += month_dict["principal_pay"]
        return ret

    def now_accumulated_principal(self):
        ret = 0
        for y, m_dict in self._big_map.items():
            for m, month_dict in m_dict.items():
                ret += month_dict["principal_pay"]
        return ret


    def get_monthly_payment(self, principal, rate, yrs):
        return


class myLoan(object):

    def __init__(self, principal, interest_rate, duration_yrs):
        self._principal = principal
        self._interest_rate = interest_rate
        self._duration_yrs = duration_yrs

        self._remaining_principal = principal
        self._remaining_yrs = duration_yrs
        self._current_interest_rate = interest_rate
        self._current_monthly_pymt = get_monthly_payment(self._current_interest_rate, self._remaining_principal, self._remaining_yrs)
        self.create_adjustment_table(self._duration_yrs*12)

    def create_adjustment_table(self, num_of_pymt):
        self._adjustment = {}
        self._adjustment[0] = {"remaining_principal" : self._remaining_principal,
                                "current_interest_rate": self._remaining_principal,
                                ""}

    def alter_interest_rate(self):
        return