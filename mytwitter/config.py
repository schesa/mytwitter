import sys

if sys.version_info < (3, 0):
    import ConfigParser as configparser
else:
    import configparser as configparser


# This is a really simple config handler. It may be worth
# adding a way in which supported config options may be defined.
# (see oslo.config).
class Config(object):
    def __init__(self):
        self._parser = configparser.RawConfigParser()

    def load_config(self, config_file):
        self._parser.read(config_file)

    def __getattr__(self, key):
        if self._parser.has_section(key):
            return ConfigSection(self._parser, key)

        section = ConfigSection(self._parser, "DEFAULT")
        return getattr(section, key)


class ConfigSection(object):
    def __init__(self, parser, section_name):
        self._parser = parser
        self._name = section_name

    def __getattr__(self, key):
        return self._parser.get(self._name, key).strip('"\'')


CONF = Config()
