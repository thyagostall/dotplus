from datetime import date

from dotplus import config, dotplus


def main():
    end_date = date.today()
    start_date = date(end_date.year, end_date.month, 1)

    credentials = dotplus.login(config.read_config('config.ini'))
    work_days_data = dotplus.time_cards(credentials, start_date, end_date)
    print(work_days_data)


if __name__ == '__main__':
    main()
