# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 19:18:33 2018

@author: kunlin.l
"""
import numpy as np
import pandas as pd
from atrader.tframe import sysclsbase as cnt
from atrader.tframe.language import text
from atrader.tframe.udefs import INTEGERS_TYPE
from atrader.tframe.utils.datetimefunc import (is_format_dt, str_date_to_mft, datetime_to_mft)
from atrader.tframe.utils.argchecker import apply_rule, verify_that
from atrader.tframe.sysclsbase import gv
from atrader.tframe.sysclsbase import smm
from . import convertor as reg_func_cvt
from . import _regfuncs

__all__ = [
    'get_current_bar',
    'reg_kdata',
    'reg_factor',
    'reg_userdata',
    'reg_userindi',
    'get_reg_kdata',
    'get_reg_kdata_adj',
    'get_reg_userdata',
    'get_reg_userindi',
    'get_reg_factor',
    'get_instruments'
]


#################################
# 刷新频率对应的kdata
@smm.force_phase(gv.RUMMODE_PHASE_ONDATA, gv.RUMMODE_PHASE_CALC_FACTOR)
@apply_rule(verify_that('target_indices').is_instance_of(*INTEGERS_TYPE, list, tuple))
def get_current_bar(target_indices=()):
    if not isinstance(target_indices, np.ndarray):
        target_indices = np.array([target_indices]).ravel()
    if len(target_indices) < 1:
        target_indices = cnt.vr.g_ATraderCache['input_targets_idx_range']
    else:
        _, target_indices = cnt.env.check_idx('get_current_bar', None, target_indices, toarray=True)
    result = cnt.env.get_bar(target_indices)
    if result is None:
        return None

    return reg_func_cvt.convert_current_bar_to_df(result)


# 数据注册

@smm.force_phase(gv.RUMMODE_PHASE_USERINIT)
@apply_rule(verify_that('frequency').is_valid_frequency(),
            verify_that('fre_num').is_instance_of(int),
            verify_that('adjust').is_in((True, False)))
def reg_kdata(frequency: 'str',
              fre_num: 'int',
              adjust=False):
    print(text.LOG_REG_REG_KDATA)
    if smm.cur_run_mode == 2 and ((str.lower(frequency) == 'day' and fre_num != 1) or cnt.gv.freuency_to_int(frequency) >= 5):
        raise NotImplementedError('暂时不支持实盘 reg_kdata 时频率 frequency 大于 `1day`')
    idx = _regfuncs.reg_k_data(frequency, fre_num, adjust)
    print(text.LOG_REG_REG_KDATA_END)
    cnt.env.user_context.reg_kdata.append(idx)


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT)
@apply_rule(verify_that('factor').is_instance_of(str, list, tuple))
def reg_factor(factor: 'list'):
    if isinstance(factor, str):
        factor = [factor]
    if len(factor) < 1:
        raise ValueError(text.ERROR_INPUT_FACTOR_TOTAL)

    print(text.LOG_REG_REG_FACTOR)
    strategy_input = cnt.env.get_strategy_input()
    reg_idx = _regfuncs.reg_factor(factor,
                                   strategy_input['TargetList'],
                                   strategy_input['BeginDate'],
                                   strategy_input['EndDate'])
    print(text.LOG_REG_REG_FACTOR_END)
    cnt.env.user_context.reg_factor.append({'reg_idx': reg_idx, 'bpfactor': list(factor)})


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT)
@apply_rule(verify_that('timeline').is_instance_of(list, tuple),
            verify_that('data').is_instance_of(list, tuple))
def reg_userdata(timeline, data):
    if len(timeline) != len(data):
        raise ValueError(text.ERROT_INPUT_USER_DATA_TIMELINE_DATALEN)

    if len(timeline) < 1:
        raise ValueError(text.ERROR_EMPTY_TIME_LINE)

    if isinstance(timeline[0], str):
        in_fmt = '%Y-%m-%d' if is_format_dt(timeline[0], '%Y-%m-%d') else '%Y-%m-%d %H:%M:%S'
        new_time_line = str_date_to_mft(timeline, fmt=in_fmt)
    else:
        new_time_line = datetime_to_mft(timeline)

    print(text.LOG_REG_REG_USERDATA)
    reg_idx = _regfuncs.reg_user_data(np.array(new_time_line), np.array(data))
    print(text.LOG_REG_REG_USERDATA_END)
    cnt.env.user_context.reg_userdata.append(reg_idx)


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT)
@apply_rule(verify_that('indi_func').is_callable())
def reg_userindi(indi_func):
    print(text.LOG_REG_REG_USERINDI)
    reg_idx = _regfuncs.reg_user_indices(indi_func)
    print(text.LOG_REG_REG_USERINDI_END)
    cnt.env.user_context.reg_userindi.append({'reg_idx': reg_idx, 'reg_func': indi_func})


@smm.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA,
                 gv.RUMMODE_PHASE_CALC_FACTOR)
@apply_rule(verify_that('target_indices').is_instance_of(list, int, tuple),
            verify_that('length').is_greater_than(0),
            verify_that('fill_up').is_in((True, False)),
            verify_that('df').is_in((True, False)))
def get_reg_kdata(reg_idx,
                  target_indices=(),
                  length=1,
                  fill_up=False,
                  df=False):
    if isinstance(target_indices, int):
        target_indices = [target_indices]
    if len(target_indices) == 0:
        target_indices = cnt.vr.g_ATraderCache['input_targets_idx_range']
    else:
        _, target_indices = cnt.env.check_idx('get_reg_kdata', None, target_indices, toarray=True)
    new_reg_idx = np.full((target_indices.size, 6), np.nan)
    for i, idx in enumerate(target_indices):
        new_reg_idx[i, :] = reg_idx[idx, :]

    if len(new_reg_idx) < 1 or new_reg_idx.size < 1:
        raise ValueError(text.ERROR_REG_IDX_PARAM)

    bar_pos = cnt.env.get_internal_fresh_bar_num(np.nan)
    result = _regfuncs.get_reg_k_data(new_reg_idx.reshape((-1, 6)), bar_pos, length, fill_up).T

    columns = ['target_idx', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'open_interest']
    if df:
        data_df = pd.DataFrame(result, columns=columns)
        return data_df
    else:
        d = {}
        for idx, target_idx in enumerate(target_indices):
            s, e = idx * length, (idx + 1) * length
            d[idx] = pd.DataFrame(result[s:e], columns=columns)
        return d


@smm.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA,
                 gv.RUMMODE_PHASE_CALC_FACTOR)
@apply_rule(verify_that('target_indices').is_instance_of(list, int, tuple),
            verify_that('length').is_greater_than(0),
            verify_that('fill_up').is_in((True, False)),
            verify_that('df').is_in((True, False)))
def get_reg_kdata_adj(reg_idx,
                      target_indices=(),
                      length=1,
                      fill_up=False,
                      df=False):
    if isinstance(target_indices, int):
        target_indices = [target_indices]
    if len(target_indices) == 0:
        target_indices = cnt.vr.g_ATraderCache['input_targets_idx_range']
    else:
        _, target_indices = cnt.env.check_idx('get_reg_k_data', None, target_indices, toarray=True)
    new_reg_idx = np.full((target_indices.size, 6), np.nan)
    for i, idx in enumerate(target_indices):
        new_reg_idx[i, :] = reg_idx[idx, :]

    if len(new_reg_idx) < 1 or new_reg_idx.size < 1:
        raise ValueError(text.ERROR_REG_IDX_PARAM)

    bar_pos = cnt.env.get_internal_fresh_bar_num(np.nan)
    result = _regfuncs.get_reg_k_data_adj(new_reg_idx.reshape((-1, 6)), bar_pos, length, fill_up).T
    columns = ['target_idx', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'open_interest']
    if df:
        data_df = pd.DataFrame(result, columns=columns)
        return data_df
    else:
        d = {}
        for idx, target_idx in enumerate(target_indices):
            s, e = idx * length, (idx + 1) * length
            d[idx] = pd.DataFrame(result[s:e], columns=columns)
        return d


@smm.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA,
                 gv.RUMMODE_PHASE_CALC_FACTOR)
@apply_rule(verify_that('reg_idx').is_instance_of(dict),
            verify_that('target_indices').is_instance_of(list, int, tuple),
            verify_that('length').is_instance_of(int).is_greater_than(0),
            verify_that('df').is_in((True, False)),
            verify_that('sort_by').is_in(('factor', 'target_idx', 'date')))
def get_reg_factor(reg_idx,
                   target_indices=(),
                   length=1,
                   df=False,
                   sort_by='target_idx'):
    if isinstance(target_indices, int):
        target_indices = [target_indices]
    if len(target_indices) < 1:
        target_indices = cnt.vr.g_ATraderCache['input_targets_idx_range']
    else:
        _, target_indices = cnt.env.check_idx('get_reg_factor', None, target_indices, toarray=True)

    factor = reg_idx.get('bpfactor', [])
    reg_idx_ = reg_idx.get('reg_idx')[:, target_indices].ravel()
    bar_pos = cnt.env.get_internal_fresh_bar_num(np.nan)
    dt, value = _regfuncs.get_reg_factor(reg_idx_, bar_pos, length)

    if df:
        data_df = reg_func_cvt.convert_reg_factor_to_df(dt, value, target_indices, factor).sort_values(sort_by, kind='mergesort', ascending=True,
                                                                                                       na_position='first')  # type: pd.DataFrame
        data_df.index = range(data_df.shape[0])
        return data_df
    else:
        data_dict = reg_func_cvt.convert_reg_factor_to_dict(dt, value, target_indices, factor)
        return data_dict


@smm.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA,
                 gv.RUMMODE_PHASE_CALC_FACTOR)
@apply_rule(verify_that('reg_idx').is_instance_of(np.ndarray),
            verify_that('length').is_instance_of(int).is_greater_than(0))
def get_reg_userdata(reg_idx,
                     length=1):
    bar_pos = cnt.env.get_internal_fresh_bar_num(np.nan)
    datetime_tl, value = _regfuncs.get_reg_user_data(reg_idx, bar_pos, length)

    return reg_func_cvt.convert_reg_userdata_to_df(datetime_tl, value)


@smm.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA,
                 gv.RUMMODE_PHASE_CALC_FACTOR)
@apply_rule(verify_that('reg_idx').is_instance_of(dict),
            verify_that('length').is_instance_of(int))
def get_reg_userindi(reg_idx,
                     length=1) -> 'pd.DataFrame':
    bar_pos = cnt.env.get_internal_fresh_bar_num(np.nan)
    reg_idx = reg_idx['reg_idx']
    t, v = _regfuncs.get_reg_user_indicator(reg_idx, bar_pos, length)

    return reg_func_cvt.convert_user_indi_to_df(t, v)


@smm.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA,
                 gv.RUMMODE_PHASE_CALC_FACTOR)
def get_instruments(target_indices=(), length=1, df=False, sort_by_date=True):
    if isinstance(target_indices, int):
        target_indices = [target_indices]
    if len(target_indices) < 1:
        target_indices = cnt.vr.g_ATraderCache['input_targets_idx_range']
    else:
        _, target_indices = cnt.env.check_idx('get_instrument', None, target_indices, toarray=True)
    bar_pos = cnt.env.get_internal_fresh_bar_num(np.nan)
    res_matrix = _regfuncs.get_instruments(target_indices, bar_pos, length)
    target_list = [cnt.vr.g_ATraderInputInfo['TargetListDot'][idx] for idx in target_indices]
    return reg_func_cvt.convert_instrument_matrix_to_output(target_list, res_matrix, df, sort_by_date)





