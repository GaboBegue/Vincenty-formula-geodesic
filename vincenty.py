from math import atan
from math import atan2
from math import cos
from math import radians
from math import sin
from math import sqrt
from math import tan


class Vincenty:
    def __init__(self, c1, c2):        
        self.meters = self.calc(c1, c2)                   # output distance in meters
        self.km = self.meters / 1000                      # output distance in kilometers
        self.mm = self.meters * 1000                      # output distance in millimeters
        self.miles = self.meters * 0.000621371            # output distance in miles
        self.n_miles = self.miles * (6080.20 / 5280)      # output distance in nautical miles
        self.feet = self.miles * 5280                     # output distance in feet
        self.inches = self.feet * 12                      # output distance in inches
        self.yards = self.feet / 3                        # output distance in yards
        
        
    def calc(self, c1 ,c2):
        a = 6378137.0                                     # length of semi-major axis of the ellipsoid (radius at equator)
        f = 1 / 298.257223563                             # flattening of the ellipsoid
        b = (1 - f) * a                                   # length of semi-minor axis of the ellipsoid (radius at the poles)
        
        lat1, lon1, = c1                                  # first point coord
        lat2, lon2, = c2                                  # second point coord
        
        U1 = atan((1 - f) * tan(radians(lat1)))
        U2 = atan((1 - f) * tan(radians(lat2)))           #	reduced latitude (latitude on the auxiliary sphere)
        
        L = radians(lon2 - lon1)                          #	difference in longitude of two points;
        Lambda = L
        
        # COMMON USED VALUES
        sin_U1 = sin(U1)
        cos_U1 = cos(U1)
        sin_U2 = sin(U2)
        cos_U2 = cos(U2)
        
        # VINCENTY CALCULATING DISTANCE IN METERS
        
        for iter in range(200):
            sin_Lambda = sin(Lambda)
            cos_Lambda = cos(Lambda) 
            sin_Sigma = sqrt((cos_U2 * sin_Lambda) ** 2 + ((cos_U1 * sin_U2) - (sin_U1 * cos_U2 * cos_Lambda)) ** 2 )
            cos_Sigma = (sin_U1 * sin_U2) + (cos_U1 * cos_U2 * cos_Lambda)
            Sigma = atan2(sin_Sigma, cos_Sigma)
            sin_Alpha = (cos_U1 * cos_U2 * sin_Lambda) / sin_Sigma        
            cos_Sq_Alpha = 1 - (sin_Alpha ** 2)
        
            try:
                cos2_Sigma_M = cos_Sigma - ((2 * sin_U1 * sin_U2) / cos_Sq_Alpha)
            except ZeroDivisionError:
                cos2_Sigma_M = 0.0
        
            C = (f / 16) * cos_Sq_Alpha * (4 + (f * (4 - 3 * cos_Sq_Alpha)))            
            LP = Lambda
            Lambda = L + (1 - C) * f * sin_Alpha * (Sigma + C * sin_Sigma * (cos2_Sigma_M + C * cos_Sigma * (-1 + 2 * (cos2_Sigma_M ** 2))))
        
            if (abs(Lambda - LP)) < 1e-12:
                break
        else:
            return None
            
        u_Sq = cos_Sq_Alpha * ((a ** 2 - b ** 2) / (b ** 2))
        # A = 1 + (u_Sq / 16384) * (4096 + u_Sq * (-768 + u_Sq * (320 - 175 * u_Sq)))               # A original formula Vincenty
        # B = (u_Sq / 1024) * (256 + u_Sq * (-128 + u_Sq * (74 - 47 * u_Sq)))                       # B original formula Vincenty
        k1 = (sqrt(1 + u_Sq) - 1) / (sqrt(1 + u_Sq) + 1)
        A = (1 + 0.25 * k1 **2) / (1 - k1)                                                          # A formula reform by Vincenty
        B = k1 * (1 - (3/8) * k1 ** 2)                                                              # A formula reform by Vincenty
        d_Sigma = B * sin_Sigma * (cos2_Sigma_M + (B / 4) * (cos_Sigma * (-1 + 2 * cos2_Sigma_M ** 2) - (B / 6) * cos2_Sigma_M * (-3 + 4 * sin_Sigma ** 2) * (-3 + 4 * cos2_Sigma_M ** 2)))
        s = b * A * (Sigma - d_Sigma)
        Alpha_1 = atan2(cos_U2 * sin_Sigma, cos_U1 * sin_U2 - sin_U1 * cos_U2 * cos_Sigma)        	# forward azimuths at the points     
        Alpha_2 = atan2(cos_U1 * sin_Sigma, - sin_U1 * cos_U2 + cos_U1 * sin_U2 * cos_Sigma)        # forward azimuths at the points 
        
        return s
