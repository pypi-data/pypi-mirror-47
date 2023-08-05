# coding=utf-8
# pylint: disable=import-error, broad-except
import json
from resources.models.helper import rest_get_call
from resources.models.helper import rest_post_json_call
from resources.models.helper import rest_delete_call
from resources.models.helper import RestError
from resources.models.helper import State
from resources.models.database import SqlConnection

class TestCaseResource(object):

    def __init__(self, host, port, session, time_out):
        self.host = host
        self.port = port
        self.session = session
        self.time_out = time_out

    def list(self, filter_):
        """
        :param filter_: list filter
        :return: type: list, return test case list meet the filter
        """
        url_ = "http://{0}:{1}/tc/{2}".format(self.host, self.port, filter_)
        result = rest_get_call(url_, self.session, self.time_out)
        return result["resource"]

    def run(self, test_case, mode="sync", **kwargs):
        """
        :param test_case: type string, test case name
        :param  mode: sync or async, run test case
        :return: type bool, return test case run result
        """
        data = {"tc": test_case, "mode":mode}
        for key in kwargs:
            data[key] = kwargs[key]
        try:
            url_ = "http://{0}:{1}/tc".format(self.host, self.port)
            result = rest_post_json_call(url_, self.session, json.dumps(data), self.time_out)
        except RestError:
            pass
        return result["resource"]

    def get_async_result(self, key):
        result = dict()
        url_ = "http://{0}:{1}/tc/results/{2}".format(self.host, self.port, key)
        try:
            result = rest_get_call(url_, self.session, self.time_out)
        except RestError:
            pass
        if result["resource"]["state"] in [State.ERROR_TIMEOUT, State.ERROR_CONNECTION, State.ERROR_NOT_FOUND]:
            sql_connection = SqlConnection()
            ret = sql_connection.get_result(key)
            if ret:
                result["resource"] = {"msg": "Get result from database\n{}".format(ret[7]), "state": ret[4]}
        return result["resource"]

    def get_result_from_db(self, key):
        result = dict()
        sql_connection = SqlConnection()
        ret = sql_connection.get_result(key)
        if ret:
            result["resource"] = {"msg": ret[7], "state": ret[4]}
        else:
            result["resource"] = {"msg": "Database not find this test: {}".format(key), "state": State.ERROR_NOT_FOUND}

    def stop_tests(self, key=None):
        if key is None:
            url_ = "http://{0}:{1}/tc".format(self.host, self.port)
        else:
            url_ = "http://{0}:{1}/tc/{2}".format(self.host, self.port, key)
        try:
            result = rest_delete_call(url_, self.session, self.time_out)
        except RestError:
            pass
        return result["resource"]
