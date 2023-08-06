# -*- coding: utf-8 -*-

import datetime
# noinspection PyUnresolvedReferences
from ..utils.utilcls import DotDict, OrderedDotDict
# noinspection PyUnresolvedReferences
from ..utils.logger import write_syslog, user_warning
# noinspection PyUnresolvedReferences
from ..language import text


def send_serial(func_name, buffer):
    from atrader.tframe import sysclsbase as cnt

    start_time = datetime.datetime.now()
    result = cnt.vr.g_ATraderSocket.send_data(buffer)
    elapsed_time = datetime.datetime.now() - start_time
    total_milliseconds = elapsed_time.days * 86400000 + elapsed_time.seconds * 1000 + elapsed_time.microseconds / 1000
    tips = 'id: %d, `%s` Send ATCore Request Data, bytes: %d, use: %d ms' % (id(cnt.vr.g_ATraderSocket), func_name, len(buffer), total_milliseconds)
    write_syslog(tips, level='debug')
    return result


def recv_serial(tips=None):
    from atrader.tframe import sysclsbase as cnt

    start_time = datetime.datetime.now()
    binary_data, parsed_data = cnt.vr.g_ATraderSocket.read_tlv()
    elapsed_time = datetime.datetime.now() - start_time
    total_milliseconds = elapsed_time.days * 86400000 + elapsed_time.seconds * 1000 + elapsed_time.microseconds / 1000
    tips = 'id: %d, `%s` Wait ATCore Response Data, bytes: %d, use: %d ms' % (id(cnt.vr.g_ATraderSocket), tips, len(binary_data), total_milliseconds)
    write_syslog(tips, level='debug')
    return parsed_data


def send_serial_sub(func_name, buffer):
    from atrader.tframe import sysclsbase as cnt

    start_time = datetime.datetime.now()
    result = cnt.vr.g_ATraderSocketSub.send_data(buffer)
    elapsed_time = datetime.datetime.now() - start_time
    total_milliseconds = elapsed_time.days * 86400000 + elapsed_time.seconds * 1000 + elapsed_time.microseconds / 1000
    tips = 'id: %d, `%s` Send ATCore Request SubData, bytes: %d, use: %d ms' % (id(cnt.vr.g_ATraderSocketSub), func_name, len(buffer), total_milliseconds)
    write_syslog(tips, level='debug')
    return result


def recv_serial_sub(tips=None):
    from atrader.tframe import sysclsbase as cnt

    start_time = datetime.datetime.now()
    binary_data, parsed_data = cnt.vr.g_ATraderSocketSub.read_tlv()
    elapsed_time = datetime.datetime.now() - start_time
    total_milliseconds = elapsed_time.days * 86400000 + elapsed_time.seconds * 1000 + elapsed_time.microseconds / 1000
    tips = 'id: %d, `%s` Wait ATCore Response SubData, bytes: %d, use: %d ms' % (id(cnt.vr.g_ATraderSocketSub), tips, len(binary_data), total_milliseconds)
    write_syslog(tips, level='debug')
    return parsed_data
