#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .predict_client import PredictClient
from .predict_client import ENDPOINT_TYPE_VIPSERVER
from .predict_client import ENDPOINT_TYPE_DIRECT
from .string_request import StringRequest
from .tf_request import TFRequest
from .torch_request import TorchRequest
from .exception import PredictException


class PredictClientTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PredictClientTestCase, self).__init__(*args, **kwargs)
        self.client = PredictClient()

    def setUp(self):
        self.client.set_endpoint('http://pai-eas-vpc.cn-shanghai.aliyuncs.com')
        self.client.set_service_name('scorecard_pmml_example')
        self.client.set_token('YWFlMDYyZDNmNTc3M2I3MzMwYmY0MmYwM2Y2MTYxMTY4NzBkNzdjOQ==')
        self.client.init()

    def tearDown(self):
        self.client.destroy()

    def test_predict_pmml_empty(self):
        req = StringRequest()
        ex = None
        try:
            self.client.predict(req)
        except PredictException as ex:
            pass

        self.assertEqual(ex, None)

    def test_prediction_pmml_bad_json(self):
        req = StringRequest('[{]]')
        ex = None
        try:
            self.client.predict(req)
        except Exception as e:
            ex = e

        self.assertEqual(True, isinstance(ex, PredictException))

    def test_prediction_bad_endpoint(self):
        req = StringRequest('[{}]')
        response = self.client.predict(req)


    def test_prediction_direct(self):
        self.client.set_endpoint_type(ENDPOINT_TYPE_DIRECT)
        self.client.init()

        request = StringRequest('[{}]')
        response = self.client.predict(request)


    def test_prediction_tensorflow(self):
        self.client.set_service_name('mnist_saved_model_example')
        self.client.set_token('YTg2ZjE0ZjM4ZmE3OTc0NzYxZDMyNmYzMTJjZTQ1YmU0N2FjMTAyMA==')
        self.client.init()

        req = TFRequest('predict_images')
        req.add_feed('images', [1, 784], TFRequest.DT_FLOAT, [8] * 784)
        response = self.client.predict(req)


    def test_prediction_vipserver(self):
        client = PredictClient('echo.shanghai.eas.vipserver', 'echo')
        client.set_endpoint_type(ENDPOINT_TYPE_VIPSERVER)
        client.init()

        request = StringRequest('[{}]')
        response = self.client.predict(request)


    def test_vipserver_endpoint(self):
        from .vipserver_endpoint import VipServerEndpoint
        ep = VipServerEndpoint('echo.shanghai.eas.vipserver')

    def test_vipserver_sync(self):
        from .vipserver_endpoint import VipServerEndpoint
        endpoint = VipServerEndpoint('echo.shanghai.eas.vipserver')
        endpoint.sync()
        endpoint.get()


if __name__ == '__main__':
    unittest.main()
