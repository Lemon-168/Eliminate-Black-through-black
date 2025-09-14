import os
import colorsys
from tkinter import Tk, Button, Label, filedialog
from PIL import Image, ImageTk

def process_image():
    # 1. 选择图片，支持三种常见格式，特别是png
    file_path = filedialog.askopenfilename(
        title="选择图片",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )
    if not file_path:
        return

    # 2. 打开图片并转换为 RGBA（Alpha）
    img = Image.open(file_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size

    # 3. 遍历处理像素
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            if a == 0:  # 完全透明的像素跳过，不用管，节省资源
                continue

            # 将 RGB 转换为 HSB（应该存在计算误差，但这个更好理解，最终结果无论RGB还是HSB，还是#000000最好）
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            
            # 思路：
            # - 原 B（Brightness/Value）越低 → 新 Alpha 越低（越透明）
            # - 同时将 B 值拉满（v=1.0，即最亮）
            new_alpha = int(v * 255)  # v∈[0,1] → Alpha∈[0,255]
            new_r, new_g, new_b = colorsys.hsv_to_rgb(h, s, 1.0)  # v=1.0（最亮）
            new_r, new_g, new_b = int(new_r*255), int(new_g*255), int(new_b*255)

            pixels[x, y] = (new_r, new_g, new_b, new_alpha)

    # 4. 保存结果（在原路径下生成 _transparent.png）
    output_path = os.path.splitext(file_path)[0] + "_transparent.png"
    img.save(output_path, "PNG")

    # 5. 预览，实际保证完全正确。目前常规的任何黑底图都可以提取原图，典型的比如冰块 水 火 烟雾等，这个逻辑比PS的更直观。
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

# 创建 GUI
root = Tk()
root.title("HSB纯黑转透明工具")

Button(root, text="选择图片并处理", command=process_image).pack(pady=10)
label = Label(root)
label.pack()

root.mainloop()