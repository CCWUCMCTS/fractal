import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import copy

def rotate(p, d):
    """返回**向量p**绕原点逆时针旋转d度的坐标"""
    a = np.radians(d)
    m = np.array([[np.cos(a), np.sin(a)],[-np.sin(a), np.cos(a)]])
    return p @ m # np.dot(p,m)

def koch_curve(p, q):
    """将线段pq生成科赫曲线，返回uvw三个点"""
    p, q = np.array(p), np.array(q)
    u = p + (q-p)/3 # 三等分点u的坐标
    v = q - (q-p)/3 # 三等分点V的坐标
    w = rotate(v-u, 60) + u # 线段uv绕u点逆时针旋转60°得到点w的坐标
    
    return u.tolist(), v.tolist(), w.tolist()
    
def snow(triangle, k):
    """给定三角形，生成封闭的科赫雪花"""
    
    for i in range(k):# 处理每条曲线，处理k次
        result = []
        t_len = len(triangle)
        # print(triangle)
        for j in range(t_len):
            p = triangle[j]
            q = triangle[(j+1)%t_len]
            # print(p)
            u, v, w = koch_curve(p, q)
            result.extend([p, u, w, v])
        # triangle = copy.deepcopy(result)
        triangle = result.copy() # 内部对象不会修改，使用浅拷贝即可
        # print(result)
    
    triangle.append(triangle[0])
    return triangle
import math
import threading
from time import sleep

def build_snow_list(n):
    s = 0
    ret = []
    for i in range(n):
        l = (s+0.5,0)
        r = (s+i+1.5,0)
        m = ((l[0]+r[0])/2,(i+1)/2*math.sqrt(3))
        ret.append(([l,m,r],i))
        # print(l)
        s = s + i + 2
    return ret

def plot_snow(snow_list):
    """返回雪花坐标数组列表"""
    ret = []
    for triangle, k in snow_list:
        data = np.array(snow(triangle, k))
        x, y = np.split(data, [1], axis=1)
        ret.append((k,x,y))
    return ret

fig = plt.figure()
ax = plt.subplot()

pool_size = 6
t = plot_snow(build_snow_list(pool_size))
control = [0] * pool_size
xlen = [len(i[1]) for i in t]
runtime_data_x = [[i[1][0]] for i in t]
runtime_data_y = [[i[2][0]] for i in t]
def animate(_):
    for i in range(pool_size):
        # print(control[i])
        if len(runtime_data_x[i]) < control[i]:
            runtime_data_x[i].extend(t[i][1][len(runtime_data_x[i]):control[i]+1])
            runtime_data_y[i].extend(t[i][2][len(runtime_data_y[i]):control[i]+1])
        else:
            runtime_data_x[i] = list(t[i][1][0:control[i]+1])
            runtime_data_y[i] = list(t[i][2][0:control[i]+1])
        line, = ax.plot(runtime_data_x[i],runtime_data_y[i])
    ax.figure.canvas.draw()
    return line,
    
for i in range(pool_size):
    line, = ax.plot(t[i][1],t[i][2],color='white')
ani = FuncAnimation(fig, animate, interval=2, blit=True)
def dataUpdate_thead(i):
    while True:
        control[i] = (control[i]+1)%xlen[i]
        sleep(0.01)
ad_rdy_ev = threading.Event()
ad_rdy_ev.set()  # 设置线程运行
for i in range(pool_size):
    ti = threading.Thread(target=dataUpdate_thead, args=(i,))
    ti.daemon = True
    ti.start()

plt.axis('equal') 
plt.show()
    
'''
plt.axis('equal') 
plt.show()
'''