from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from sensor_base import SensorBase


class PodsResource(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            extension="/api/v1/watch/pods",
            trigger_ref="kubernetes.pods"):
        super(
            self.__class__,
            self).__init__(
            sensor_service=sensor_service,
            config=config,
            extension=extension,
            trigger_ref=trigger_ref)
