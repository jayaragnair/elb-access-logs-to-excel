import os
import gzip
from tkinter.filedialog import askopenfilenames
from openpyxl import Workbook

download_folder = f'{os.path.expanduser("~")}/Downloads/'
filenames = askopenfilenames(initialdir=download_folder, title="Select the GZIP files of Access logs")
print(filenames)
access_log_syntax = ['type', 'time', 'elb', 'client:port', 'target:port', 'request_processing_time',
                     'target_processing_time', 'response_processing_time', 'elb_status_code', 'target_status_code',
                     'received_bytes', 'sent_bytes', '"request"', '"user_agent"', 'ssl_cipher', 'ssl_protocol',
                     'target_group_arn', 'trace_id', 'domain_name', 'chosen_cert_arn', 'matched_rule_priority',
                     'request_creation_time', 'actions_executed', 'redirect_url', 'error_reason', 'target:port_list',
                     'target_status_code_list', 'classification', 'classification_reason']

wb = Workbook()
ws = wb.active
ws.append(access_log_syntax)

for filename in filenames:
    with gzip.open(filename, 'rt') as txt_file:
        for line in txt_file.readlines():
            raw_list = line.split(' ')
            join_list = []
            for item in raw_list:
                if item[0] == '"' and item[-1] != '"':
                    start_index = raw_list.index(item)
                    for next_item in raw_list[start_index + 1::]:
                        if next_item[-1] == '"':
                            end_index = raw_list.index(next_item)
                            break
                        else:
                            pass
                    join_list.append([start_index, end_index])

            for indexes in join_list:
                current_index = join_list.index(indexes)
                raw_list[indexes[0] - current_index:indexes[1] + 1 - current_index] = \
                    [' '.join(raw_list[indexes[0] - current_index:indexes[1] + 1 - current_index])]
            print(raw_list)
            ws.append(raw_list)

ws.auto_filter.ref = ws.dimensions
wb.save(f"{download_folder}/ELB_ACCESS_LOGS_{filenames[0][-15:-7:]}.xlsx")
wb.close()
