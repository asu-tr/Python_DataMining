# This Python script is for data mining competition of Innoscripta.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
from bs4 import BeautifulSoup
import requests
import timeit


def print_hi(name):
    start = timeit.default_timer()
    print(f'Hi, {name}')

    links = get_links()

    r = requests.get(str(links[0])[2:-2])

    if r.status_code == 200:
        print('success')
        soup = BeautifulSoup(r.content, 'html.parser')
        info = soup.select('td')[6].get_text(strip=True)

        print(info)

        # Get company name

        company_name_start_index = info.index(":")
        company_name_end_index = info.index(",")
        company_name = info[company_name_start_index + 2:company_name_end_index]
        print(company_name)

        # Get former address

        former_address_start_index = info.index(",", company_name_end_index+1)
        former_address_end_index = info.index(".", former_address_start_index)
        former_address = info[former_address_start_index + 2:former_address_end_index]
        print(former_address)

        # Get new address

        new_address_start_index = info.index(":", former_address_end_index)
        new_address = info[new_address_start_index + 2:-1]
        print(new_address)

    else:
        print('error when reaching the website')

    stop = timeit.default_timer()
    execution_time = stop - start
    print(execution_time)


def get_links():
    file = open('1000 address action.csv')
    csv_reader = csv.reader(file)

    header = next(csv_reader)

    rows = []
    for row in csv_reader:
        rows.append(row)

    file.close()

    return rows


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Asu')
