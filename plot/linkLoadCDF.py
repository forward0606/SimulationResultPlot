from cmath import log10
import numpy as np
import math
import os
import matplotlib.pyplot as plt
import matplotlib.transforms
import matplotlib
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

# 修改資料夾路徑
directory_path = "../ans_cdf/"

class CDFChartGenerator:
    def __init__(self, dataName, Xlabel, Ylabel):
        filename = directory_path + dataName
        print("start generate", filename)

        if not os.path.exists(filename):
            print(f"file doesn't exist: {filename}")
            # 產生假資料測試用 (若檔案不存在)
            # lines = [str(x) + "\n" for x in np.random.exponential(0.5, 1000)]
            return

        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # --- 1. 資料處理 (轉成一維陣列) ---
        data_points = []
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # 處理可能是一行一個數字，或是一行多個空格分開的數字
            parts = line.split()
            for p in parts:
                try:
                    val = float(p)
                    data_points.append(val)
                except ValueError:
                    continue
        
        if not data_points:
            print("No valid data found.")
            return

        # --- 2. 計算 CDF ---
        # 排序數據
        sorted_data = np.sort(data_points)
        # 產生對應的 Y 軸 (從 0 到 1)
        # 方法 A: y = k / n
        y_vals = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        
        # --- 3. 樣式設定 (沿用模板) ---
        color = ["#FF0000", "#00FF00", "#0000FF", "#000000"]
        
        fontsize = 36
        Xlabel_fontsize = fontsize
        Ylabel_fontsize = fontsize
        Xticks_fontsize = fontsize
        Yticks_fontsize = fontsize

        andy_theme = {
            "xtick.labelsize": 20,
            "ytick.labelsize": 20,
            "axes.labelsize": 20,
            "axes.titlesize": 20,
            "font.family": "Times New Roman",
            "mathtext.it": "Times New Roman:italic",
            "mathtext.rm": "Times New Roman",
            "mathtext.fontset": "custom"
        }

        matplotlib.rcParams.update(andy_theme)
        fig, ax1 = plt.subplots(figsize = (8, 6), dpi = 600)
        
        ax1.tick_params(direction = "in")
        ax1.tick_params(bottom = True, top = True, left = True, right = True)
        ax1.tick_params(pad = 20)

        # --- 4. 繪圖 ---
        # 畫 CDF 線
        ax1.plot(sorted_data, y_vals, 
                 color="#0044FF",  # 使用藍色，可自行修改
                 lw=3.0, 
                 linestyle="-", 
                 clip_on=False) # clip_on=False 讓線條貼齊軸時不被切掉

        # --- 5. 軸範圍與刻度設定 ---
        
        # X 軸範圍：從 0 到 最大值 (或稍大一點)
        # 如果你只關心 0~1 的分布，可以用 ax1.set_xlim(0, 1)
        # max_val = max(sorted_data)
        # ax1.set_xlim(0, max_val if max_val > 1 else 1.05) 
        ax1.set_xlim(left=0) # 確保從 0 開始
        
        # Y 軸範圍：CDF 固定是 0 到 1
        ax1.set_ylim(0, 1.05)
        ax1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])

        plt.xticks(fontsize = Xticks_fontsize)
        plt.yticks(fontsize = Yticks_fontsize)

        # 調整邊距
        plt.subplots_adjust(top = 0.90)
        plt.subplots_adjust(left = 0.18) 
        plt.subplots_adjust(right = 0.95)
        plt.subplots_adjust(bottom = 0.18)

        # 格線
        plt.grid(True, linestyle='--', color='0.8')

        # Label 設定
        plt.ylabel(Ylabel, fontsize = Ylabel_fontsize, labelpad = 35)
        plt.xlabel(Xlabel, fontsize = Xlabel_fontsize, labelpad = 10)
        
        # 手動調整 Label 位置 (可選)
        # ax1.yaxis.set_label_coords(-0.15, 0.5)
        # ax1.xaxis.set_label_coords(0.50, -0.15)

        # --- 6. 存檔 ---
        pdfName = dataName.replace('.ans', '_cdf') # 檔名加上 _cdf
        
        # 建立資料夾
        if not os.path.exists(directory_path + 'pdf/'):
            os.makedirs(directory_path + 'pdf/')
        if not os.path.exists(directory_path + 'eps/'):
            os.makedirs(directory_path + 'eps/')

        print("save fig in "+directory_path + 'pdf/{}.jpg'.format(pdfName))
        plt.savefig(directory_path + 'pdf/{}.jpg'.format(pdfName))
        plt.savefig(directory_path + 'eps/{}.eps'.format(pdfName))
        plt.close()

if __name__ == "__main__":
    # 這裡輸入檔名，路徑已在 directory_path 設定為 ../ans_cdf/
    CDFChartGenerator("15_maxBufLoad_.ans", "Link Load", "CDF")
