'''
Created on 04.02.2018

@author: despair1
'''

import sql_turnover_profit
import config_init
import db


def populate_profit_sheet(profit_sheet):
    database = db.db.db
    configuration = config_init.config_init

    class EmptyClass:
        pass

    return_object = EmptyClass()
    sql_turnover_profit.profit(database, configuration, return_object)
    summary_profit_cell = profit_sheet.getCellRangeByName(configuration.get("summary_profit"))
    summary_profit_cell.Value = return_object.summary_profit
    summary_profit_cell = profit_sheet.getCellRangeByName(configuration.get("monthly_profit"))
    summary_profit_cell.Value = return_object.monthly_profit
    summary_profit_cell = profit_sheet.getCellRangeByName(configuration.get("monthly_profit_forday"))
    summary_profit_cell.Value = return_object.monthly_profit_forday
    summary_profit_cell = profit_sheet.getCellRangeByName(configuration.get("weekly_profit"))
    summary_profit_cell.Value = return_object.weekly_profit
    summary_profit_cell = profit_sheet.getCellRangeByName(configuration.get("weekly_profit_forday"))
    summary_profit_cell.Value = return_object.weekly_profit_forday

    ypos_detail_profit = int(configuration.get("ypos_detail_profit"))
    xpos_goods_of_week = configuration.get("xpos_goods_of_week")
    xpos_daily_profit_for_week = configuration.get("xpos_daily_profit_for_week")
    xpos_margin_for_week = configuration.get("xpos_margin_for_week")
    for i in return_object.l_profit_week:
        goods_name_cell = profit_sheet.getCellByPosition(xpos_goods_of_week, ypos_detail_profit)
        goods_name_cell.String = i[0]
        daily_profit_for_week_cell = profit_sheet.getCellByPosition(xpos_daily_profit_for_week, ypos_detail_profit)
        daily_profit_for_week_cell.Value = i[1]/7
        margin_for_week_cell = profit_sheet.getCellByPosition(xpos_margin_for_week, ypos_detail_profit)
        margin_for_week_cell.Value = float(return_object.d_margin_week[i[0]])-1.0
        ypos_detail_profit += 1
