import json
import importlib
import requests
import re
import base64

from pyswagger import App, Security
from pyswagger.utils import jp_compose
from pyswagger.core import BaseClient
from pyswagger.io import Request

from k8sbase import Client

from datetime import datetime

class K8sClient:

    def __init__(self, config):

        self.config = config
        self.templates = config['template_path']

        self.swagger = self.templates + "/swagger.json"

    def _json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

    def _encode_intOrString(self, obj, val, ctx):
        # val is the value used to create this primitive, for example, a
        # dict would be used to create a Model and list would be used to
        # create an Array

        # obj in the spec used to create primitives, they are
        # Header, Items, Schema, Parameter in Swagger 2.0.

        # ctx is parsing context when producing primitives. Some primitves needs
        # multiple passes to produce(ex. Model), when we need to keep some globals
        # between passes, we should place them in ctx
        pass


    def overwriteConfig(self, newconf):

        for key in newconf:
            self.config[key] = newconf[key]

    def runAction(self, action, **kwargs):

        if "config_override" in kwargs:
            self.overwriteConfig(kwargs['config_override'])

        factory = Primitive()
        factory.register('string', 'int-or-string', self._encode_intOrString)

        #app = App.create(self.swagger)
        app = App.load(url=self.swagger, prim=factory)
        app.prepare()
        client = Client(config=self.config, send_opt=({'verify': False}))

        opt=dict(
            url_netloc = self.config['kubernetes_api_url'][8:]  # patch the url of petstore to localhost:8001
        )

        op = app.op[action]

        # bit of a hack - pyswagger can't handle */* currently
        if op.consumes[0] == u'*/*':
            op.consumes[0] = u'application/json'

        a = op(**kwargs)

        resp = client.request(a, opt=opt)

        return resp

if __name__ == "__main__":

    config = {'master_url': "master-a.andrew.kube", 'username': 'admin', 'password': 'andypass', 'templates': '/opt/stackstorm/packs/kubernetes'}

    k8s = K8sClient(config)

    args = {'name': 'default'}
    resp = k8s.runAction('readCoreV1Namespace', **args)

    print "content: %s" % resp['content']
    print "status: %s" % resp['status']
    print "headers: %s" % resp['headers']
