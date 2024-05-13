from vincenty import vincenty
import math
import numpy as np
from scipy.optimize import least_squares



# 声速
c = 343  # m/s

# 给定监测设备数据
coordinates = np.array([
    [110.241, 27.204, 824, 100.767],
    [110.780, 27.456, 727, 112.220],
    [110.712, 27.785, 742, 188.020],
    [110.251, 27.825, 850, 258.985],
    [110.524, 27.617, 786, 118.443],
    [110.467, 27.921, 678, 266.871],
    [110.047, 27.121, 575, 163.024]
])

# 定义误差函数
def residual_function(params, data):
    x, y, z, t0 = params
    residuals = []

    for point in data:
        x_i, y_i, z_i, t_i = point
        computed_time = np.sqrt((x - x_i)**2 + (y - y_i)**2 + (z - z_i)**2) / c + t0
        residual = c * (t_i - computed_time)
        residuals.append(residual)

    return residuals

# 初始参数估计
initial_guess = np.array([110, 27, 800, 100])

# 最小二乘法求解
result1 = least_squares(residual_function, initial_guess, args=(coordinates,))
x_opt, y_opt, z_opt, t0_opt = result1.x
initial_guess2 = np.array([x_opt, y_opt, z_opt, t0_opt])

# Levenberg-Marquardt算法求解
result2 = least_squares(residual_function, initial_guess2, method='lm', args=(coordinates,))
x_opt2, y_opt2, z_opt2, t0_opt2 = result2.x

print(f"残骸位置：经度={x_opt2}, 纬度={y_opt2}, 高程={z_opt2}")
print(f"音爆时间：{t0_opt2} 秒")




#计算两点之间距离
def diatance(x1,y1,z1,x2,y2,z2):
    plane_craft = (x1,y1)
    radio_craft = (x2,y2)
    dte=(math.sqrt((vincenty(plane_craft, radio_craft))**2+(z1-z2)**2))
    return (dte)

'''
# 定义两个地点的经纬度
boston = (42.3541165, -71.0693514)
newyork = (40.7791472, -73.9680804)
a = vincenty(boston, newyork)
print(a)
# 计算距离（单位：公里）
distance = diatance(42.3541165, -71.0693514,0,40.7791472, -73.9680804,0)
print(distance)  # 输出距离
'''
