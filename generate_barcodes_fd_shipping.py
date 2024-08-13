import pandas as pd
import os
from gerali_barcode import generate_code
# import tqdm

INPUT_FILE_PREFIX_NAME = 'transport_2024_04'

EAN_CODES_PATH = os.path.expanduser("~") + '/Gerali/Barcodes'
EAN_SHEET = 'cereri_produse'
# ID_NAME_MAP = 'id_name_map.xlsx'

FD_SHIP_LIST = os.path.join(EAN_CODES_PATH, INPUT_FILE_PREFIX_NAME + '_packing_list' + '.xlsx')
SAVE_DIR = os.path.join(EAN_CODES_PATH, 'barcodes_' + INPUT_FILE_PREFIX_NAME)

if not os.path.isdir(SAVE_DIR):
  os.mkdir(SAVE_DIR)

ean_dir_path = os.path.join(EAN_CODES_PATH, 'ean_gs1')

fd_ship_list_data = pd.read_excel(FD_SHIP_LIST)

gs1_df = pd.DataFrame()

for excel_file in os.listdir(ean_dir_path):
  if excel_file.startswith('gs1') and excel_file.endswith('.xlsx'):
    excel_file_path = os.path.join(ean_dir_path, excel_file)
    excel_data = pd.read_excel(excel_file_path, EAN_SHEET)
    excel_data['gerali_id'] = excel_file[4:-5]

    # Get Color and Size and add them to the main DataFrame
    for idx in range(len(excel_data)):
      denumire_produs = excel_data.iloc[idx]['Denumire produs'].replace(' ', '').lower()
      denumire_produs = denumire_produs.split(',')

      excel_data.at[idx, 'color'] = denumire_produs[-2]
      excel_data.at[idx, 'size'] = denumire_produs[-1]

    gs1_df = gs1_df.append(excel_data)

barcode_list = list()

for item in fd_ship_list_data.iterrows():
  barcode_element = dict()
  barcode_element['GTIN'] = item[1]['EAN']
  barcode_element['name'] = item[1]['Denumire Produs']
  barcode_element['color'] = item[1]['Color code'].capitalize()
  barcode_element['size_ro'] = str(item[1]['SizeRO'])
  barcode_element['size_intl'] = str(item[1]['SizeFD'])
  barcode_element['gerali_id'] = item[1]['Style'].lower()

  barcode_element['quantity'] = item[1]['Quantity']

  barcode_list.append(barcode_element)

  print(barcode_element)

  bar_text = barcode_element['name'] + ', ' + barcode_element['color'] + ', ' + barcode_element['size_ro']
  bar_text = bar_text.title()
  bar_text = bar_text.replace('\'S', '\'s')
  bar_text += ' / ' + barcode_element['size_intl']

  for i in range(barcode_element['quantity']):
    suffix = '' if i == 0 else '_' + str(i)

    file_id = barcode_element['gerali_id'] + '-' + barcode_element['color'] + '-' + barcode_element['size_ro'] + '-' + \
              barcode_element['size_intl'] + suffix + '.png'
    save_file = os.path.join(SAVE_DIR, file_id)
    generate_code(str(barcode_element['GTIN']), bar_text, save_file)

  barcode_df = pd.DataFrame(barcode_list)
  barcode_df.to_excel('New_sizes.xlsx', index=False)

print('Done')