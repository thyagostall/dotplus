from dotplus import config, dotplus


def main():
    credentials = dotplus.login(config.read_config('config.ini'))
    work_days_data = dotplus.time_cards(credentials)
    print(work_days_data)


if __name__ == '__main__':
    main()
