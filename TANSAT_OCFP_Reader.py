# -*- coding: utf-8 -*-
# @Time    : 2022/05/28 14:42
# @Author  : Henrich Wang
# @Github  : https://github.com/HundredW
# @Email   : han.wang@stu.pku.edu.cn
# @File    : TANSAT_OCFP_Reader.py
# @Des     : Scripts for reading and converting data from TANSAT_OCFP products to general GIS formats.
#            Reference from the documents from GHD_CCI  products.
#            1.https://catalogue.ceda.ac.uk/uuid/2cc63301f1854239aa61c70e58c61207
#            2.https://www.iup.uni-bremen.de/carbon_ghg/docs/GHG-CCIplus/PSD/PSDv3_GHG-CCI_final.pdf
#            Requirements: geopandas, shapely, netCDF4


import time
import geopandas as gpd
import pandas
from shapely.geometry import Point
import glob
import netCDF4 as nc
import os


def convert_tansatocfp_2vec(nc_files_path='2017.06\\06', outType='shp',
                            nc_target_variables=['xco2', 'xco2_uncertainty', 'retr_flag', 'xco2_quality_flag']):
    """
    TANSATOCFP数据 NC 文件数据属性转矢量点
    # ['xco2_averaging_kernel', 'surface_air_pressure_apriori_std', 'pressure_weight', 'xco2_uncertainty',
    #  'pressure_levels', 'solar_zenith_angle', 'xco2_no_bias_correction', 'surface_air_pressure_apriori',
    #  'surface_altitude', 'air_temperature_apriori', 'gain', 'h2o_profile_apriori', 'time', 'exposure_id',
    #  'retr_flag', 'total_aod', 'latitude', 'xco2_quality_flag', 'surface_altitude_stdev', 'xco2',
    #  'longitude', 'sensor_zenith_angle', 'cirrus', 'aod_type1', 'co2_profile_apriori', 'aod_type2']
    :param nc_files_path: 某一个月的NC文件路径
    :param outType: 矢量格式，默认shp，提取的单个字段名称过长(大于10个字符)时，推荐geojson、
    :param nc_target_variables: 待提取的变量名称
    :return:
    """
    if isinstance(nc_target_variables, list):
        nc_files = glob.glob(nc_files_path + '\\*.nc')
        try:
            for nc_file in nc_files:
                nc_data = nc.Dataset(nc_file)
                times = nc_data.variables['time'][:]
                times = list(map(lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t))), times))
                longitude = nc_data.variables['longitude'][:]
                latitude = nc_data.variables['latitude'][:]
                geometries = [Point(ll) for ll in zip(longitude, latitude)]
                target_values = []
                for tv in nc_target_variables:
                    target_values.append(nc_data.variables[tv][:])
                if len(target_values) > 1:
                    data_attrs = zip(*target_values)
                else:
                    data_attrs = target_values[0]
                df = pandas.DataFrame(list(data_attrs), columns=nc_target_variables)
                df['longitude'] = longitude
                df['latitude'] = latitude
                df['time'] = times
                gdf = gpd.GeoDataFrame(df, crs='EPSG:4326', geometry=geometries)
                file_name = str(os.path.basename(nc_file)).replace('nc', outType)
                if not os.path.exists(nc_files_path + '\\ConvertedFiles'):
                    os.mkdir(nc_files_path + '\\ConvertedFiles')
                gdf.to_file(nc_files_path + '\\ConvertedFiles\\' + file_name, encodings='UTF-8')
                print('Converted done, data has been extracted to  ' + file_name)
        except Exception as e:
            print('Error information:', e)

    else:
        print("Error information: Target variables error")


if __name__ == '__main__':
    # 转换nc数据到矢量点

    ## 给定nc所在文件夹路径
    nc_file_path_month = '2017.06\\06'
    ## 给定需要导出的属性字段
    nc_target_variables = ['xco2', 'xco2_uncertainty', 'retr_flag', 'xco2_quality_flag']
    convert_tansatocfp_2vec(nc_file_path_month, outType='shp', nc_target_variables=nc_target_variables)
