import turtle
import math

# 设置画布和画笔
screen = turtle.Screen()
screen.title("六芒星阵")
screen.setup(800, 600)  # 设置窗口大小
t = turtle.Turtle()
t.speed(5)  # 设置绘制速度
t.pensize(2)  # 设置线条粗细

def draw_hexagram(size):
    # 计算六芒星的总高度，用于居中
    height = size * math.sqrt(3)
    
    # 移动到起始位置（考虑到六芒星的整体大小，使其居中）
    t.penup()
    t.goto(-size/2, -height/4)  # 向左移动半个边长，向下移动四分之一高度
    t.pendown()
    
    # 绘制第一个三角形（向上）
    t.color("blue")
    for _ in range(3):
        t.forward(size)
        t.left(120)
    
    # 计算第二个三角形的起始位置
    t.penup()
    # 移动到第一个三角形的顶点位置
    t.goto(-size/2, -height/4)  # 回到第一个三角形的起始点
    t.forward(size/4)  # 向右移动四分之一边长
    t.left(60)        # 向上转
    t.forward(height/3)  # 向上移动高度的1/3
    t.right(60)       # 回正
    t.pendown()
    
    # 绘制第二个三角形（向下）
    t.color("red")
    for _ in range(3):
        t.forward(size)
        t.right(120)

# 绘制六芒星
draw_hexagram(200)

# 隐藏画笔
t.hideturtle()

# 保持窗口显示
screen.mainloop()