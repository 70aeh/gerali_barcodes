import pandas as pd
import os
from gerali_barcode import generate_code
from size_map import SizeMapper
# import tqdm

EAN_CODES_PATH = '/Users/70aeh/Gerali/Barcodes'
EAN_SHEET = 'cereri_produse'
ID_NAME_MAP = 'id_name_map.xlsx'
SAVE_DIR = os.path.join(EAN_CODES_PATH, 'transport_08_2022')

if not os.path.isdir(SAVE_DIR):
  os.mkdir(SAVE_DIR)

ean_dir_path = os.path.join(EAN_CODES_PATH, 'ean_gs1')
id_map_path = os.path.join(EAN_CODES_PATH, ID_NAME_MAP)

size_mapper = SizeMapper(id_map_path)

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

ean_map_data = pd.read_excel(id_map_path).drop_duplicates()

barcode_list = list()

for item in gs1_df.iterrows():
  barcode_element = dict()
  barcode_element['GTIN'] = item[1]['GTIN']
  barcode_element['gerali_id'] = item[1]['gerali_id']
  barcode_element['color'] = item[1]['color']
  barcode_element['size_ro'] = item[1]['size']

  querry_gerali_id = item[1]['gerali_id']

  if querry_gerali_id not in list(ean_map_data['gerali_id']):
    continue

  ret_item = ean_map_data.loc[ean_map_data['gerali_id'] == querry_gerali_id]['name']
  ret_size_map = ean_map_data.loc[ean_map_data['gerali_id'] == querry_gerali_id]['size_map'].item()
  ret_size_map_old = ean_map_data.loc[ean_map_data['gerali_id'] == querry_gerali_id]['size_map_old'].item()
  barcode_element['size_intl'] = size_mapper.ro_to_intl(item[1]['size'], ret_size_map)
  barcode_element['size_intl_old'] = size_mapper.ro_to_intl(item[1]['size'], ret_size_map_old)

  barcode_element['name'] = ''
  if not(ret_item.empty):
    barcode_element['name'] = ret_item.item()
  # Skip non-existent codes
  else:
    continue

  barcode_list.append(barcode_element)

  print(barcode_element)

  bar_text = barcode_element['name'] + ', ' + barcode_element['color'] + ', ' + barcode_element['size_ro']
  bar_text = bar_text.title()
  bar_text += ' / ' + barcode_element['size_intl']

  file_id = barcode_element['gerali_id'] + '-' + barcode_element['color'] + '-' + barcode_element['size_ro'] + '-' + barcode_element['size_intl'] + '.png'
  save_file = os.path.join(SAVE_DIR, file_id)
  generate_code(str(barcode_element['GTIN']), bar_text, save_file)

  barcode_df = pd.DataFrame(barcode_list)
  barcode_df.to_excel('New_sizes.xlsx', index=False)

print('Done')