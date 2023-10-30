import csv
import re

def split_name(names_list):
    for j, full_name in enumerate(names_list):
        full_name = full_name.split()
        if len(full_name) > 1:
            names_list[j] = full_name.pop(0)
            names_list[j+1] = ' '.join(full_name)
    return names_list

def make_phone(row):
    if re.search('доб', row, re.IGNORECASE):
        pattern = r'\+?([7|8])\s?\(?(\d{3})\)?[\s-]?(\d{2,})[\s-]?(\d{2,})[\s-]?(\d{2,})\s\(?\w+[.\s]*(\d+)\)?'
        replacement = r'+7(\2)\3-\4-\5 доб.\6'
        regex = re.sub(pattern, replacement, row)
    else:
        pattern = r'\+?([7|8])\s?\(?(\d{3})\)?[\s-]?(\d{2,})[\s-]?(\d{2,})[\s-]?(\d{2,})'
        replacement = r'+7(\2)\3-\4-\5'
        regex = re.sub(pattern, replacement, row)
    return regex

def correct_data(reader):
    for row in reader:
        row[:3], row[5] = split_name(row[:3]), make_phone(row[5])
    return reader


def remove_duplicates(reader):
    result_dict = {}
    for row in correct_data(reader):
        key = ' '.join(row[:2])
        data_dict = {'surname': row[2], 'organization': row[3], 'position': row[4], 'phone': row[5], 'email': row[6]}
        if result_dict.get(key):
            for value in result_dict.get(key):
                if row[2] in value.get('surname'):
                    value.update({key: data_dict.get(key) for key in value if not value.get(key)})
                else:
                    result_dict.get(key).append(data_dict)
        else:
            result_dict[key] = [data_dict]
    return result_dict


if __name__ == '__main__':
    with open('phonebook_raw.csv', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        header = reader.pop(0)

    correct_data(reader)

    remove_duplicates(reader)

    with (open('phonebook.csv', 'w', newline='', encoding='utf-8') as file):
        datawriter = csv.DictWriter(file, fieldnames=header, delimiter=',')
        datawriter.writeheader()
        for key, value_list in remove_duplicates(reader).items():
            for value in value_list:
                datawriter.writerow({'lastname': key.split()[0], 'firstname': key.split()[1], 'surname': value.get('surname'),
                                     'organization': value.get('organization'), 'position': value.get('position'),
                                     'phone': value.get('phone'), 'email': value.get('email')}
                                    )


