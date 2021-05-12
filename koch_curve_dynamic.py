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
def plot_snow(snow_list):
    """返回雪花数组"""
    ret = []
    for triangle, k in snow_list:
        data = np.array(snow(triangle, k))
        x, y = np.split(data, [1], axis=1)
        ret.append((x,y))
    return ret

snow_list = [
    ([(0,0), (0.5,0.8660254), (1,0)], 3),
    ([(1.1,0.4), (1.35,0.8330127), (1.6,0.4)], 4),
    ([(1.1,-0.1), (1.25,0.15980761), (1.4,-0.1)], 3)
]
fig, ax = plt.subplots()
x,y = plot_snow(snow_list[:1])[0]
xlen = len(x)
line, = ax.plot(x,y)


def init():  # only required for blitting to give a clean slate.
    line, = ax.plot(x,[np.nan] * len(x))  # update the data.
    ax.figure.canvas.draw()
    return line,

def animate(i):
    line, = ax.plot(x[0:(i+1)%xlen],y[0:(i+1)%xlen])  # update the data.
    ax.figure.canvas.draw()
    return line,

divide = 4**(3-2) # sum:3*4**k
frames = [i for i in range(0,xlen,divide)]
ani = FuncAnimation(fig, animate, init_func=init, interval=2, blit=True, frames=frames) 

plt.axis('equal') 
plt.show()
# ani.save('animation.gif', writer='pillow')