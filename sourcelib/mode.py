from creationism.registration.factory import RegistrantFactory
from creationism.utils import first_lowered


class Mode(RegistrantFactory):
    STATIC = True
    AUTO = True
    REPLACE = False
    CONVERT_NAME = first_lowered


class DefaultMode(Mode):
    ...
