from lib import k8s

from st2actions.runners.pythonrunner import Action

class deleteCoreV1CollectionNode(Action):

    def run(self,fieldSelector=None,labelSelector=None,resourceVersion=None,timeoutSeconds=None,watch=None,pretty=None,config_override=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if fieldSelector is not None:
          args['fieldSelector'] = fieldSelector
        if labelSelector is not None:
          args['labelSelector'] = labelSelector
        if resourceVersion is not None:
          args['resourceVersion'] = resourceVersion
        if timeoutSeconds is not None:
          args['timeoutSeconds'] = timeoutSeconds
        if watch is not None:
          args['watch'] = watch
        if pretty is not None:
          args['pretty'] = pretty
        if config_override is not None:
          args['config_override'] = config_override

        return (True, myk8s.runAction('deleteCoreV1CollectionNode', **args))
