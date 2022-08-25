import pandas as pd


class SizeMapper:
    def __init__(self, map_path):
        self.maps_data = pd.read_excel(map_path, 'size_maps').drop_duplicates()

    def ro_to_intl(self, ro_size, map):
        ro_size = int(ro_size)
        ret_str = self.maps_data.loc[self.maps_data['ro'] == ro_size][map].item()
        return ret_str

if __name__ == '__main__':
    import os

    EAN_CODES_PATH = '/Users/70aeh/Gerali/Barcodes'
    ID_NAME_MAP = 'id_name_map.xlsx'

    maps_path = os.path.join(EAN_CODES_PATH, ID_NAME_MAP)
    maps = SizeMapper(maps_path)

    print(maps.maps_data.head())

    print(maps.ro_to_intl(48, 'f2'))



    print('Done.')