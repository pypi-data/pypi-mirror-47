# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Wjy
import os
import json
import socket

MACHINE_NAME = os.environ.get("HOSTNAME", "") + os.environ.get("hostname", "")


class JournalLog:
    """
    新流水日志
    """

    def __init__(self, req_app_name: str = "",
                 res_app_name: str = "",
                 req_time="",
                 res_time="",
                 elapse_time="",
                 req_content: str = "",
                 res_content: str = "",
                 req_host: str = "",
                 res_host: str = "",
                 code: str = "",
                 err_desc: str = "",
                 transaction_id: str = "",
                 request_id: str = ""):
        self.req_app_name: str = req_app_name
        self.res_app_name: str = res_app_name
        self.req_time = req_time
        self.res_time = res_time
        self.elapse_time = elapse_time
        self.req_content: str = req_content
        self.res_content: str = res_content
        self.req_host: str = req_host
        self.res_host: str = res_host
        self.code: str = code
        self.err_desc: str = err_desc
        self.transaction_id: str = transaction_id
        self.request_id: str = request_id

    def json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class InternalLog:
    """
    (旧)内部流水模型
    """

    def __init__(self, id_: str = "1",
                 call_time=None,
                 call_ip: str = "",
                 call_rev: str = "",
                 xml_contents: str = "",
                 response_result: str = "",
                 response_content: str = "",
                 response_time=None,
                 transaction_id: str = "",
                 action_code: str = "",
                 bus_code: str = "",
                 service_contractor: str = "",
                 service_level: str = "",
                 src_org_id: str = "",
                 src_sys_id: str = "",
                 src_sys_sign: str = "",
                 dst_org_id: str = "",
                 dstsysid: str = "",
                 reqtime=None,
                 createdateppm: str = "",
                 disable_opid: str = "",
                 disable_date: str = "",
                 create_opid: str = "",
                 create_date: str = "",
                 rec_status: int = 0,
                 flow: int = 0,
                 order_id: str = "",
                 machinename: str = MACHINE_NAME,
                 feedback_code: str = "",
                 feedback_content: str = ""):
        self.id: str = id_
        self.call_time = call_time
        self.call_ip: str = call_ip
        self.call_rev: str = call_rev
        self.xml_contents: str = xml_contents
        self.response_result: str = response_result
        self.response_content: str = response_content
        self.response_time = response_time
        self.transaction_id: str = transaction_id
        self.action_code: str = action_code
        self.bus_code: str = bus_code
        self.service_contractor: str = service_contractor
        self.service_level: str = service_level
        self.src_org_id: str = src_org_id
        self.src_sys_id: str = src_sys_id
        self.src_sys_sign: str = src_sys_sign
        self.dst_org_id: str = dst_org_id
        self.dstsysid: str = dstsysid
        self.reqtime = reqtime
        self.createdateppm: str = createdateppm
        self.disable_opid: str = disable_opid
        self.disable_date: str = disable_date
        self.create_opid: str = create_opid
        self.create_date: str = create_date
        self.rec_status: int = rec_status
        self.flow: int = flow
        self.order_id: str = order_id
        self.machinename: str = machinename
        self.feedback_code: str = feedback_code
        self.feedback_content: str = feedback_content

    def json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class ExternalInterfaceLoggingEvent:
    """
    (旧)外部流水
    """

    def __init__(self, id_: str = "",
                 call_time=None,
                 call_ip: str = "",
                 call_rev: str = "",
                 xml_contents: str = "",
                 response_result: str = "",
                 response_content: str = "",  # 业务层响应报文_
                 response_time=None,
                 transactionid: str = "",  # IT报文流水号
                 actioncode: str = "",
                 buscode: str = "",
                 servicecontractver: str = "",
                 servicelevel: str = "",
                 srcorgid: str = "",
                 srcsysid: str = "",
                 srcsyssign: str = "",
                 dstorgid: str = "",
                 dstsysid: str = "",
                 reqtime=None,
                 createdateppm: str = "",
                 disable_opid: str = "",
                 disable_date: str = "",
                 create_opid: str = "",
                 create_date: str = "",
                 rec_status: int = 0,
                 flow: int = 0,
                 order_id: str = "",
                 machinename: str = MACHINE_NAME,
                 feedback_code: str = "",
                 feedback_content: str = ""):
        self.id: str = id_
        self.call_time = call_time
        self.call_ip: str = call_ip
        self.call_rev: str = call_rev
        self.xml_contents: str = xml_contents
        self.response_result: str = response_result
        self.response_content: str = response_content
        self.response_time = response_time
        self.transactionid: str = transactionid
        self.actioncode: str = actioncode
        self.buscode: str = buscode
        self.servicecontractver: str = servicecontractver
        self.servicelevel: str = servicelevel
        self.srcorgid: str = srcorgid
        self.srcsysid: str = srcsysid
        self.srcsyssign: str = srcsyssign
        self.dstorgid: str = dstorgid
        self.dstsysid: str = dstsysid
        self.reqtime = reqtime
        self.createdateppm: str = createdateppm
        self.disable_opid: str = disable_opid
        self.disable_date: str = disable_date
        self.create_opid: str = create_opid
        self.create_date: str = create_date
        self.rec_status: int = rec_status
        self.flow: int = flow
        self.order_id: str = order_id
        self.machinename: str = machinename
        self.feedback_code: str = feedback_code
        self.feedback_content: str = feedback_content

    def json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class OrderJournalEvent:
    """
    (旧)订单日志
    """

    def __init__(self, is_last_try: str = "1",
                 response_content: str = "",
                 request_content: str = "",
                 response_code: str = "",
                 transaction_id: str = "",
                 result: str = "",
                 ctime=None,
                 order_id: str = "",
                 if_type: str = "41",
                 phone_number: str = "",
                 prov_code: str = "",
                 city_code: str = "",
                 prov_name: str = "",
                 city_name: str = ""):
        self.is_last_try: str = is_last_try
        self.response_content: str = response_content
        self.request_content: str = request_content
        self.response_code: str = response_code
        self.transaction_id: str = transaction_id
        self.result: str = result
        self.ctime = ctime
        self.order_id: str = order_id
        self.if_type: str = if_type
        self.phone_number: str = phone_number
        self.prov_code: str = prov_code
        self.city_code: str = city_code
        self.prov_name: str = prov_name
        self.city_name: str = city_name

    def json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class IssueJobJournal(object):
    """
    (旧)业务层日志
    """

    def __init__(self, phone_number: str = "",
                 log_status: str = "",
                 prov_name2: str = "",
                 ctime="2018-01-12 10:22:24",
                 prov_code: str = "",
                 response_content: str = "",
                 order_id: str = "",
                 response_code: str = "00000",
                 city_name2: str = "",
                 prov_name: str = "",
                 is_last_try: int = 1,
                 request_content: str = "",
                 result: int = 1,
                 if_type: int = 1,
                 city_name: str = "",
                 prov_code2: str = "",
                 city_code2: str = "",
                 transaction_id: str = "",
                 city_code: str = ""):
        self.phone_number = phone_number
        self.log_status = log_status
        self.prov_name2 = prov_name2
        self.ctime = ctime
        self.prov_code = prov_code
        self.response_content = response_content
        self.order_id = order_id
        self.response_code = response_code
        self.city_name2 = city_name2
        self.prov_name = prov_name
        self.is_last_try: int = is_last_try
        self.request_content = request_content
        self.result: int = result
        self.if_type: int = if_type
        self.city_name = city_name
        self.prov_code2 = prov_code2
        self.city_code2 = city_code2
        self.transaction_id = transaction_id
        self.city_code = city_code


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    if ip:
        return ip

    try:
        # linux和windows都可以获取
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.connect(("8.8.8.8", 80))
        ip = client.getsockname()[0]
    except Exception as e:
        print(e)
        return "未获取到IP"
    else:
        client.close()
    return ip
