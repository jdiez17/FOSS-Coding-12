import ConfigParser, os

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join(os.path.dirname(__file__), 'config.ini')))
