# coding=utf-8
# pylint: disable=import-error,eval-used
import json
from resources.models.helper import rest_get_call
from resources.models.helper import rest_post_json_call
from resources.models.helper import rest_delete_call
from resources.models.helper import State
from resources.models.database import SqlConnection


class TestSuiteResource(object):

    def __init__(self, host, port, session, time_out):
        self.host = host
        self.port = port
        self.session = session
        self.time_out = time_out

    def list(self, filter_):
        """
        :param filter_: string, filter_ condition
        :return: list, return list result
        """
        url_ = "http://{0}:{1}/ts/{2}".format(self.host, self.port, filter_)
        result = rest_get_call(url_, self.session, self.time_out)
        return result["resource"]

    def run(self, test_suite, mode="sync"):
        """
        :param test_suite: which test suite need to run
        :param  mode: sync or async, run test suite
        :return: list, return the test suite run results. include each test case in test suite
        """
        data = {"ts": test_suite, "mode": mode}
        url_ = "http://{0}:{1}/ts".format(self.host, self.port)
        result = rest_post_json_call(url_, self.session, json.dumps(data), self.time_out)
        return result["resource"]

    def get_async_result(self, key):
        url_ = "http://{0}:{1}/ts/results/{2}".format(self.host, self.port, key)
        result = rest_get_call(url_, self.session, self.time_out)
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

    def stop_tests(self):
        url_ = "http://{0}:{1}/ts".format(self.host, self.port)
        result = rest_delete_call(url_, self.session, self.time_out)
        return result["resource"]

    def get_test_lists(self, test_suite_name):
        url_ = "http://{0}:{1}/ts/testlist/{2}".format(self.host, self.port, test_suite_name)
        result = rest_get_call(url_, self.session, self.time_out)
        if result["resource"]["state"] == State.PASS:
            result["resource"]["data"] = eval(result["resource"]["data"][0])
        return result["resource"]
