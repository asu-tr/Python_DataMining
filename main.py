# This Python script is for data mining competition of Innoscripta.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def do_all_stuf():

    links = get_links()

    file_no_de = 'Aktenzeichen:'

    company_names = []
    former_addresses = []
    new_addresses = []

    x = 1

    for link in links:
        r = requests.get(str(link)[2:-2])

        if r.status_code == 200:
            print(f"success {x}")
            soup = BeautifulSoup(r.content, 'html.parser')

            info = soup.select('td')[0].get_text(strip=True)
            file_no = info[info.index(file_no_de) + 14:]

            info = soup.select('td')[6].get_text(strip=True)

            # Get company name
            if file_no in info:
                company_name_start_index = info.index(":")
            else:
                company_name_start_index = -2

            company_name_end_index = info.index(",")
            company_name = info[company_name_start_index + 2:company_name_end_index]
            # print(f'name: {company_name}')

            company_names.append(company_name)

            # Get former address
            match = re.search(r'\d{5}', info[company_name_end_index::])
            if match:
                postal_code_index = info.index(match.group())

                former_address_start_index = info.rindex(",", company_name_end_index, postal_code_index)
                former_address_start_index = info.rindex(",", company_name_end_index, former_address_start_index)

                former_address_end_index = info.find(".", former_address_start_index)
                if former_address_end_index == -1:
                    former_address = info[former_address_start_index + 2:]
                else:
                    # if info[former_address_end_index + 1:former_address_end_index + 2] != " ":
                        # former_address_end_index = info.index(".", former_address_end_index + 1)

                    if info[former_address_end_index - 3:former_address_end_index].lower() == 'str' or info[former_address_end_index - 2:former_address_end_index].lower() == 'dr':
                        former_address_end_index = info.index(".", former_address_end_index + 1)

                    if info[former_address_start_index + 1:former_address_start_index + 2] == ".":
                        former_address_start_index = info.rindex(",", company_name_end_index, former_address_start_index)
                        former_address_end_index = info.index(".", former_address_end_index + 1)

                    former_address = info[former_address_start_index + 2:former_address_end_index]

            else:
                former_address = "NOT FOUND"

            # print(f'old: {former_address}')

            former_addresses.append(former_address)

            # Get new address
            new_address_start_index = info.find("Geschäftsanschrift")

            if new_address_start_index == -1:
                new_address = "NOT FOUND"

            else:
                new_address_start_index = info.index(":", new_address_start_index)
                new_address_end_index = info.find(".", new_address_start_index)
                if new_address_end_index == -1:
                    new_address = info[new_address_start_index + 2:]
                else:
                    if info[new_address_end_index - 3:new_address_end_index].lower() == 'str' or info[new_address_end_index - 2:new_address_end_index].lower() == 'dr':
                        new_address_end_index = info.index(".", new_address_end_index + 1)
                    new_address = info[new_address_start_index + 2:new_address_end_index]
                # print(f'new: {new_address}')

            new_addresses.append(new_address)

        else:
            print('error connecting the website')

        x += 1

    df = pd.DataFrame({'Name': company_names, 'Former': former_addresses, 'New': new_addresses})
    df.to_csv('company_info.csv', index=False, encoding='ISO-8859-1')


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
    do_all_stuf()
