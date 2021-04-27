import numpy as np
import pandas as pd

"""""""""""
本月应扣缴税额 = （ 本月累计应扣预缴纳税所得额 * 预扣税率 - 速算扣除数）-累计减免税额 - 累计已预扣预缴税额
本月累计应扣预缴纳税所得额= 累计收入 - 累计免税收入 - 累计减除费用 - 累计专项扣除 - 累计专项附加扣除 - 累计依法确定的其他扣除
"""""""""""


class TaxCalculator:
    def __init__(self):
        data = {'lower_bound': [0, 36000, 144000, 300000, 420000, 660000, 960000],
                'upper_bound': [36000, 144000, 300000, 420000, 660000, 960000, 1000000000000000000],
                'rate': [0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.45]}
        self.rate_matrix = pd.DataFrame(data)

    def getCurrentMonthPay(self, past_month_pays, past_month_already_costs, current_month_salary,
                           current_month_already_cost):
        """
        计算实习生当月到手工资（不含五险一金）
        :param past_month_pays: arr, 本年度在本月之前每月税前工资
        :param monthly_salary:  float, 当前月薪
        :return: 本月实际到手工资
        """
        exceed_sums = []
        texs = []
        final_get_moneys = []
        past_month_pays.append(current_month_salary)
        past_month_already_costs.append(current_month_already_cost)
        for i in range(len(past_month_pays)):
            if i == 0:
                exceed_sums.append(past_month_pays[i] - 5000 - past_month_already_costs[i])
            else:
                exceed_sums.append(past_month_pays[i] - 5000 - past_month_already_costs[i] + exceed_sums[i - 1])
            sum_tex = 0
            for j in range(len(self.rate_matrix)):
                if exceed_sums[i] > self.rate_matrix.ix[j]['upper_bound']:
                    sum_tex += (self.rate_matrix.ix[j]['upper_bound'] - self.rate_matrix.ix[j]['lower_bound']) * \
                               self.rate_matrix.ix[j]['rate']
                else:
                    sum_tex += (exceed_sums[i] - self.rate_matrix.ix[j]['lower_bound']) * self.rate_matrix.ix[j]['rate']
                break
            if i == 0:
                texs.append(sum_tex)
            else:
                texs.append(sum_tex - np.sum(texs))
            final_get_moneys.append(past_month_pays[i] - texs[i])
        return past_month_pays, exceed_sums, texs, final_get_moneys


if __name__ == '__main__':
    tex_calculator = TaxCalculator()
    # 示例：已经实习三个月，日薪（日薪+餐补）*出勤天数，再加上房补，假设税前月薪分别是6000，7000，8000
    # 根据地区政策或者公司政策，每个月扣除项合计金额为X元，以300元为例
    # 假设本月税前工资是9000，还是扣除项合计金额300，则可计算出当月薪资
    past_month_pays, exceed_sums, texs, final_get_moneys = tex_calculator.getCurrentMonthPay([6000, 7000, 8000],
                                                                                             [300, 300, 300],
                                                                                             9000, 300)
    # 如果你是第一个月实习，则前两个数组都为空即可
    # past_month_pays, exceed_sums, texs, final_get_moneys = tex_calculator.getCurrentMonthPay([],[],
    #                                                                                          9000, 300)
    for i in range(len(past_month_pays)):
        # if i<len(past_month_pays)-1:
        #     continue
        print("===================================================")
        print("第 " + str(i+1) + " 个月工资：")
        print("税前工资金额： {:.2f} 元".format(past_month_pays[i]))
        print("累计应缴预缴所得额： {:.2f} 元".format(exceed_sums[i]))
        print("本月应扣缴额： {:.2f} 元".format(texs[i]))
        print("税后工资金额： {:.2f} 元".format(final_get_moneys[i]))
