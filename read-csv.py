import csv
import pandas
import timeit

# https://realpython.com/python-csv/#what-is-a-csv-file

"""  """
with open('tickers.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            # print(f'\tSymbol: {row[0]} - {row[1]}')
            line_count += 1
    print(f'Processed {line_count} lines.')


# SCV to Dict
# with open('tickers.csv', mode='r', encoding='utf-8') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     line_count = 0
#     for row in csv_reader:
#         print(row.keys())
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         print(f'\t{row["symbol"]} - {row["id"]}')
#         line_count += 1
#     print(f'Processed {line_count} lines.')

timeit.timeit()
# Open by pandas
myfile = open('tickers.csv')
data = pandas.read_csv(myfile, encoding='utf-8', quotechar='"', delimiter=',')
print(data.values)

# # Write to a CSV file
# with open('tickers.csv', mode='w') as employee_file:
#     employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#     employee_writer.writerow(['John Smith', 'Accounting', 'November'])
#     employee_writer.writerow(['Erica Meyers', 'IT', 'March'])

# # Writing CSV File From a Dictionary With csv
# with open('employee_file2.csv', mode='w') as csv_file:
#     fieldnames = ['emp_name', 'dept', 'birth_month']
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#     writer.writeheader()
#     writer.writerow({'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'})
#     writer.writerow({'emp_name': 'Erica Meyers', 'dept': 'IT', 'birth_month': 'March'})