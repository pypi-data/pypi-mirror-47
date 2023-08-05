#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/5/20 21:09
@File    : factor.py
@contact : mmmaaaggg@163.com
@desc    : 用来对时间序列数据建立因子
"""
import datetime
import logging
import ffn
import numpy as np
import pandas as pd

from ibats_common.example.data import get_delivery_date_series

logger = logging.getLogger(__name__)
logger.debug('引用ffn %s', ffn)


def add_factor_of_trade_date(df: pd.DataFrame, trade_date_series):
    """
    自然日，交易日相关因子
    :param df:
    :param trade_date_series:
    :return:
    """
    # 自然日相关因子
    index_s = pd.Series(df.index)
    df['dayofweek'] = index_s.apply(lambda x: x.dayofweek).to_numpy()
    df['day'] = index_s.apply(lambda x: x.day).to_numpy()
    df['month'] = index_s.apply(lambda x: x.month).to_numpy()
    df['daysleftofmonth'] = index_s.apply(lambda x: x.days_in_month - x.day).to_numpy()

    # 本月第几个交易日, 本月还剩几个交易日
    groups = trade_date_series.groupby(trade_date_series.apply(lambda x: datetime.datetime(x.year, x.month, 1)))

    def get_td_of_month(dt):
        first_day_of_month = datetime.datetime(dt.year, dt.month, 1)
        month_s = groups.get_group(first_day_of_month)
        td_of_month = (month_s <= dt).sum()
        td_left_of_month = (month_s > dt).sum()
        return month_s.shape[0], td_of_month, td_left_of_month

    result_arr = index_s.apply(get_td_of_month).to_numpy()
    df['td_of_month'] = [_[0] for _ in result_arr]
    df['td_pass_of_month'] = [_[1] for _ in result_arr]
    df['td_left_of_month'] = [_[2] for _ in result_arr]

    # 本周第几个交易日, 本周还剩几个交易日
    groups = trade_date_series.groupby(trade_date_series.apply(lambda x: x.year * 100 + x.weekofyear))

    def get_td_of_week(dt):
        name = dt.year * 100 + dt.weekofyear
        week_s = groups.get_group(name)
        td_pass_of_week = (week_s <= dt).sum()
        td_left_of_week = (week_s > dt).sum()
        return week_s.shape[0], td_pass_of_week, td_left_of_week

    result_arr = index_s.apply(get_td_of_week).to_numpy()
    df['td_of_week'] = [_[0] for _ in result_arr]
    df['td_pass_of_week'] = [_[1] for _ in result_arr]
    df['td_left_of_week'] = [_[2] for _ in result_arr]

    # 距离下一次放假交易日数（超过2天以上的休息日）
    # 计算距离下一个交易日的日期
    days_2_next_trade_date_s = (trade_date_series.shift(-1) - trade_date_series).fillna(pd.Timedelta(days=0))
    days_2_next_trade_date_s.index = pd.DatetimeIndex(trade_date_series)
    # 倒序循环，计算距离下一次放假的日期
    days_count, trade_date_count, result_dic, first_date = np.nan, np.nan, {}, index_s[0]
    for trade_date, delta in days_2_next_trade_date_s.sort_index(ascending=False).items():
        if trade_date < first_date:
            break
        days = delta.days
        if days > 3:
            trade_date_count, days_count = 0, 0
        elif pd.isna(days_count) >= 0 and days >= 1:
            trade_date_count += 1
            days_count += days
        else:
            trade_date_count, days_count = np.nan, np.nan

        result_dic[trade_date] = [days_count, trade_date_count]

    vacation_df = pd.DataFrame(result_dic).T.sort_index().rename(columns={0: 'days_2_vacation', 1: 'td_2_vacation'})
    df = df.join(vacation_df, how='left')

    return df


def add_factor_of_delivery_date(df, delivery_date_series):
    index_s = pd.Series(df.index)

    # 当期合约距离交割日天数
    result_arr = []
    for _, trade_date in index_s.items():
        next_2_date = delivery_date_series[delivery_date_series > trade_date].head(2)
        if next_2_date.shape[0] < 2:
            day_2_first_del_date, day_2_second_del_date = np.nan, np.nan
        else:
            first_del_date, secend_del_date = next_2_date[0], next_2_date[1]
            day_2_first_del_date = (first_del_date - trade_date).days
            day_2_second_del_date = (secend_del_date - trade_date).days

        result_arr.append([day_2_first_del_date, day_2_second_del_date])

    df['days_2_first_del_date'] = [_[0] for _ in result_arr]
    df['days_2_second_del_date'] = [_[1] for _ in result_arr]
    return df


def add_factor_of_price(df: pd.DataFrame, close_key='close'):
    # 均线因子
    close_s = df[close_key]
    df[f'rr'] = close_s.to_returns()
    for n in [5, 10, 15, 20, 30, 60]:
        df[f'ma{n}'] = close_s.rolling(n).mean()
    # EMA
    for n in [12, 26, 60]:
        df[f'ema{n}'] = close_s.ewm(span=n).mean()
    # 波动率因子
    expanding = close_s.expanding(5)
    df[f'volatility_all'] = expanding.std() / expanding.mean()
    for n in [20, 60, 120, 240]:
        df[f'volatility{n}'] = close_s.rolling(n).std() / close_s.rolling(n).mean()

    # 收益率方差
    rr = close_s.to_returns()
    for n in [20, 60]:
        df[f'rr_std{n}'] = rr.rolling(n).std()

    df[f'ema{n}'] = close_s.ewm(span=n).mean()
    return df


def get_factor(df: pd.DataFrame, close_key='close', vol_key='volume', trade_date_series=None, delivery_date_series=None,
               dropna=True) -> pd.DataFrame:
    """
    在当期时间序列数据基础上增加相关因子
    目前已经支持的因子包括量价因子、时间序列因子、交割日期因子
    :param df: 时间序列数据索引为日期
    :param close_key:
    :param vol_key:
    :param trade_date_series: 交易日序列
    :param delivery_date_series:交割日序列
    :param dropna: 是否 dropna
    :return:
    """
    ret_df = df.copy()

    # 增加量价因子
    if close_key is not None:
        ret_df = add_factor_of_price(ret_df, close_key)

    # 交易日相关因子
    if trade_date_series is not None:
        ret_df = add_factor_of_trade_date(ret_df, trade_date_series)

    # 交割日相关因子
    if delivery_date_series is not None:
        ret_df = add_factor_of_delivery_date(ret_df, delivery_date_series)

    if dropna:
        ret_df.dropna(inplace=True)
    return ret_df


def _test_get_factor():
    from ibats_common.example.data import load_data, get_trade_date_series
    instrument_type = 'RU'
    file_name = f"{instrument_type}.csv"
    df = load_data(file_name).set_index('trade_date').drop('instrument_type', axis=1)
    df.index = pd.DatetimeIndex(df.index)
    factor = get_factor(df,
                        trade_date_series=get_trade_date_series(),
                        delivery_date_series=get_delivery_date_series(instrument_type))
    logger.info("\n%s\t%s \n%s\t%s", df.shape, list(df.columns), factor.shape, list(factor.columns))
    print("\n%s\t%s \n%s\t%s" % (df.shape, list(df.columns), factor.shape, list(factor.columns)))


if __name__ == '__main__':
    _test_get_factor()
