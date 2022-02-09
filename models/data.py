import streamlit as st
import numpy as np
import functools


class Data:
    def __init__(
        self,
        equipment_service_life=40,
        omega_base=5.63,
        omega_new=1.487,
        delta_q=50,
        oil_production_decline=0.08,
        switch_quantity=2,
        switch_price=850,
        switch_mount_price=350,
        et_length=1,
        et_price=6700,
        oil_price=81,
        oil_barrel=7.59,
        dollar_rate=72,
        oil_price_inside=35,
        oil_export=0.537,
        conditional_var_cost=2.6,
        property_tax=0.02,
        profit_tax=0.2,
        discount_rate=0.12,
        mining_tax=9.088,
    ):

        self.omega_base = st.number_input(
            "Интенсивность потока отказов, ω, базовый", value=omega_base
        )
        self.omega_new = st.number_input(
            "Интенсивность потока отказов, ω новый", value=omega_new
        )
        self.delta_q = st.number_input(
            "Потери добычи нефти на одно отключение в сети 35 кВ, ΔQ", value=delta_q
        )
        self.oil_production_decline = st.number_input(
            "Темп падения добычи нефти в год", value=oil_production_decline
        )
        self.switch_quantity = st.number_input(
            "Кол-во выключателей", value=switch_quantity
        )
        self.switch_price = st.number_input("Выключатель", value=switch_price)
        self.switch_mount_price = st.number_input("СМР", value=switch_mount_price)
        self.et_length = st.number_input("Длина ВЛ", value=et_length)
        self.et_price = st.number_input("Базовая стоимость ВЛ", value=et_price)
        self.oil_price = st.number_input("Цена нефти ", value=oil_price)
        self.oil_barrel = st.number_input("В 1 т.нефти баррелей", value=oil_barrel)
        self.dollar_rate = st.number_input("Курс доллара", value=dollar_rate)
        self.oil_price_inside = st.number_input(
            "цена нефти на внутр.рынке",
            value=oil_price_inside,
        )
        self.oil_export = st.number_input("экпорт нефти ", value=oil_export)
        self.equipment_service_life = st.number_input(
            "срок службы оборудования",
            value=equipment_service_life,
        )
        self.conditional_var_cost = st.number_input(
            "условно-переменные затраты",
            value=conditional_var_cost,
        )
        self.property_tax = st.number_input("Налог наимущество", value=property_tax)
        self.profit_tax = st.number_input("Налог на прибыль", value=profit_tax)
        self.discount_rate = st.number_input(
            "Ставка дисконтирования",
            value=discount_rate,
        )
        self.mining_tax = st.number_input("Ндпи", value=mining_tax)

    # calculation

    @property
    def delta_omega(self):
        return self.omega_base - self.omega_new

    @property
    def oil_inside_sell(self):
        return 1 - self.oil_export

    @property
    def lose_oil_production(self):
        return (
            self.oil_inside_sell * self.oil_price_inside
            + self.oil_export
            * self.oil_barrel
            * self.oil_price
            * self.dollar_rate
            / 1000
        )

    @property
    def year_q(self):
        return self.delta_omega * self.delta_q

    # table

    # 32
    @property
    def indexes(self) -> np.ndarray:
        return np.arange(0, self.equipment_service_life + 1)

    # 33
    @property
    def oil_production_increase(self) -> np.ndarray:
        return np.array(
            [
                self.year_q * (1 - self.oil_production_decline) ** i
                for i in range(self.equipment_service_life)
            ]
        )

        # return [int(i) for i in self.inexes]

    # 34
    @property
    def capital_investments(self):
        return (
            self.switch_quantity * self.switch_price
            + self.switch_mount_price * self.switch_quantity
            + self.et_length * self.et_price
        )

    # 35
    @property
    def addition_profit_growth(self) -> np.ndarray:
        return self.oil_production_increase * self.lose_oil_production

    # 36
    @property
    def production_cost_increase(self) -> np.ndarray:
        return np.array(
            list(
                map(
                    lambda i: sum(i),
                    zip(self.condition_variables, self.deprication, self.mining_taxes),
                )
            )
        )

    # 37
    @property
    def condition_variables(self) -> np.ndarray:
        return self.oil_production_increase * self.conditional_var_cost

    # 38
    @property
    def deprication(self) -> np.ndarray:
        return self.norm_deprication * self.capital_investments

    # 39
    @property
    def norm_deprication(self):
        return self.years / self.years.sum()

    # 40
    @property
    def years(self) -> np.ndarray:
        return np.array(
            [
                self.equipment_service_life - i
                for i in range(self.equipment_service_life)
            ]
        )

    # 41
    @property
    def mining_taxes(self) -> np.ndarray:
        return self.oil_production_increase * self.mining_tax

    # 42
    @property
    def balance_income(self) -> np.ndarray:
        return self.addition_profit_growth - self.production_cost_increase

    # # 43
    @property
    def property_taxes(self) -> np.ndarray:
        return self.property_tax_base * self.property_tax

    # 44
    @property
    def residual_cost(self) -> np.ndarray:
        def enumerate_list(arr: list, element):
            arr.append(arr[-1] - element)
            return arr

        return np.array(functools.reduce(
            enumerate_list, self.deprication, [self.capital_investments]
        ))

    # 45
    @property
    def property_tax_base(self) -> np.ndarray:
        return np.array(
            list(
                map(
                    lambda i: (self.residual_cost[i[0]] + i[1]) / 2,
                    enumerate(self.residual_cost[1:]),
                )
            )
        )

    # 46
    @property
    def taxation_profit(self) -> np.ndarray:
        return self.balance_income - self.property_taxes

    # 47
    @property
    def profit_taxes(self) -> np.ndarray:
        result = self.taxation_profit.copy()
        result[result > 0] *= self.profit_tax
        result[result <= 0] = 0
        return result

    # 48
    @property
    def clear_profit(self) -> np.ndarray:
        return self.taxation_profit - self.profit_taxes

    # 49
    @property
    def money_flow(self):
        return np.insert(
            self.clear_profit + self.deprication, 0, [-self.capital_investments]
        )

    # 50
    @property
    def discounted_money_flow(self) -> np.ndarray:
        return np.array(
            list(
                map(
                    lambda i: i[1] / (1 + self.discount_rate) ** i[0],
                    enumerate(self.money_flow),
                )
            )
        )

    # 51
    @property
    def cumulative_discount_money_flow(self):
        def enumerate_list(arr: list, element):
            arr.append(arr[-1] + element)
            return arr

        return np.array(
            functools.reduce(
                enumerate_list,
                self.discounted_money_flow[1:],
                [self.discounted_money_flow[0]],
            ),
        )

    @property
    def result_dict(self):
        result = {
            '': self.indexes,
            'Прирост добычи нефти, т.': self.oil_production_increase,
            'Дополнительный прирост выручки в результате сокращения потока отказов, тыс. руб': self.addition_profit_growth,
            'Прирост производств.себестоимости (условно-переменные+амортизация+НДПИ), тыс.руб': self.production_cost_increase,
            '\t-условно-переменные, тыс.руб' :self.condition_variables,
            '\t-амортизация  (методом по сумме лет использования) , тыс.руб.':self.deprication,
            'норма амортизации, доли ед.': self.norm_deprication,
            'года': self.years,
            '\t-НДПИ, тыс. руб': self.mining_taxes,
            'Балансовая прибыль, тыс.руб.': self.balance_income,
            'Налог на имущество, тыс. руб': self.property_taxes,
            'остаточная стоимость, тыс. руб': self.residual_cost,
            'база для нагога на имущество, тыс. руб': self.property_tax_base,
            'Прибыль для налогообл, тыс.руб.': self.taxation_profit,
            'Налог на прибыль': self.profit_taxes,
            'Чистая прибыль, тыс.руб': self.clear_profit,
            'Сальдо денежного потока, тыс.руб': self.money_flow,
            'Дисконтированный денежный поток, тыс.руб': self.discounted_money_flow,
            'Дисконтированный денежный поток нарастающим итогом,тыс. руб':self.cumulative_discount_money_flow
        }
        
        max_length = functools.reduce(lambda max, row: max if max >= len(row) else len(row), result.values(), 0)
        for key, row in result.items():
            result[key] =  (max_length - len(row)) * [np.nan] + row.tolist()
        return result
