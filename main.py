from datetime import date

from dotplus import dotplus


def main():
    end_date = date.today()
    start_date = date(end_date.year, end_date.month, 1)

    work_days_data = dotplus.time_cards(start_date, end_date)
    print(work_days_data)


if __name__ == '__main__':
    main()
