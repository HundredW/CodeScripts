import math

@staticmethod
def CacuDistacneFromLL(A_lon, A_lat, B_lon, B_lat):
    """
    输入点A、B的经纬度计算平面距离
    :param A_lon: 点A经度
    :param A_lat: 点A纬度
    :param B_lon: 点B经度
    :param B_lat: 点B纬度
    :return: 点A、B的平面距离,单位为m
    """
    Pi = math.pi
    Deg2Rad = (Pi / 180.0)
    EQuator_Radius_meters = 6378137.0
    Polar_Radius_meters = 6356752.3
    EQuator_Circum_meters = 2.0 * Pi * EQuator_Radius_meters
    Polar_Circum_meters = 2.0 * Pi * Polar_Radius_meters
    Avg_lat = (A_lat + B_lat) / 2.0
    WK_Lon = ((A_lon - B_lon) / 360.0) * EQuator_Circum_meters * math.cos(math.fabs(Avg_lat) * Deg2Rad)
    WK_Lat = ((A_lat - B_lat) / 360.0) * Polar_Circum_meters
    WK_Lon = WK_Lon * WK_Lon
    WK_Lat = WK_Lat * WK_Lat
    distance = math.sqrt(WK_Lon + WK_Lat)
    return distance
@staticmethod
def CacuLLBoundsFromDistance(lon,lat,distance)：
    """
    :param lon:中心点经度
    :param lat:中心点纬度
    :return: Tuple,最大范围的经度、纬度
    """
    Pi = math.pi
    Deg2Rad = (Pi / 180.0)
    EQuator_Radius_meters = 6378137.0
    Polar_Radius_meters = 6356752.3
    
    
if __name__=='__main__':
    A_lon=110.080032
    A_lat=36.407765
    B_lon=110.095543
    B_lat=36.400087
    print(CacuDistacneFromLL(A_lon,A_lat,B_lon,B_lat))
