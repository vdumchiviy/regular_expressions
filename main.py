import re
# from pprint import pprint
import csv

contacts_list = list()
# https://regex101.com/r/HI0qmG/1
# ^(\+7|8)?([ -]*\(?[ -]*)(\d+)([ -]*\)?[ -]*)([ -]*)(\d+)([ -]*)(\d+)([ -]*)(\d+)


def read_csv():
    # читаем адресную книгу в формате CSV в список contacts_list

    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def save_csv(contacts_list: list):
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list)


def replace_fio(contacts_list: list):
    for item in contacts_list[1:]:
        fio = item[0] + " " + item[1] + " " + item[2]
        pattern = re.compile(r"\s")
        result = re.split(pattern, fio, maxsplit=2)
        item[0] = result[0].replace(" ", "")
        item[1] = result[1].replace(" ", "")
        item[2] = result[2].replace(" ", "")
        # print(result)


def replace_phone(contacts_list: list):
    for item in contacts_list[1:]:
        phone = item[5]
        pattern = re.compile(
            r"^(\+7|8)?([ -]*\(?[ -]*)(\d+)([ -]*\)?[ -]*)([ -]*)(\d+)([ -]*)(\d+)([ -]*)(\d+)([ ёа-я,\(\.]*)(\d*)([ ёа-я,\)\.]*)")
        subset = r"\3\6\8\10\12"
        find_string = pattern.sub(subset, phone)
        # result = "+" + result[0:1].replace("8", "7")
        result = find_string
        if len(find_string) > 0:
            result = "+7(" + find_string[0:3] + ")" + \
                find_string[3:6] + "-" + find_string[6:8] + \
                "-" + find_string[8:10]
            if len(find_string) > 10:
                result = result + " доб." + find_string[10:]
        item[5] = result


def roll_contacts(contacts_list: list):
    result = contacts_list[0:1]
    index = 1
    index_new = 0
    len_contacts_list = len(contacts_list)
    while index < len_contacts_list:
        new = contacts_list[index]
        result.append(new)
        index_new += 1
        # result[index_new] = new

        for item in contacts_list[index+1:]:
            if (item[0] == new[0]) and (item[1] == new[1]):
                len_item = len(item)-1
                len_new = len(new)-1

                new2 = [item[x]
                        if ((len_item >= x and len_new >= x) and (len(item[x]) > len(new[x]))) or (len_item >= x and len_new < x)
                        else (list() if (len_item < x and len_new < x) else new[x])
                        for x in range(len(result[0]))]
                result[index_new] = new2
                contacts_list.remove(item)

        len_contacts_list = len(contacts_list)
        index += 1

    # print(result)
    return result
    # for item in contacts_list[1:]:


contacts_list = read_csv()
replace_fio(contacts_list)
replace_phone(contacts_list)
contacts_list = roll_contacts(contacts_list)
# print(contacts_list)
save_csv(contacts_list)
# print(contacts_list)
