import collections
import configparser


Config = collections.namedtuple('Config', [
    'email',
    'password',
    'sign_in_url',
    'time_cards_url',
    ])


def read_config(config_filename):
    config = configparser.ConfigParser()
    config.read(config_filename)
    config_default_section = config['DEFAULT']
    config_urls_section = config['URLS']

    return Config(
        config_default_section['email'],
        config_default_section['password'],
        config_urls_section['sign_in'],
        config_urls_section['time_cards']
    )
