from cmath import log10
import numpy as np
import math
import os
import matplotlib.pyplot as plt
import matplotlib.transforms
# import latex
import matplotlib
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker


directory_path = "../ans/"

class ChartGenerator:
    # data檔名 Y軸名稱 X軸名稱 Y軸要除多少(10的多少次方) Y軸起始座標 Y軸終止座標 Y軸座標間的間隔
    def __init__(self, dataName, Xlabel, Ylabel):
        filename = directory_path + dataName
        print("start generate", filename)

        if not os.path.exists(filename):
            print("file doesn't exist")
            # 為了測試方便，如果檔案不存在，這裡暫時產生假資料，實際使用請移除下面這段
            # return 
            pass

        # 讀取檔案邏輯 (保持不變)
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except:
             # 假資料 fallback (若無檔案時使用)
            lines = ["10 500 600 700 800", "20 1000 1200 1300 1400", "30 1500 1600 1700 1800"]

        # Ydiv, Ystart, Yend, Yinterval
        Ypow = 0
        Xpow = 0

        color = [
            "#FF0000",
            "#800080",
            "#FF8800",
            "#00FF00",
            "#0000FF",
            "#000000",
            "#0044FF",
            "#0088FF",
            "#00CCFF"
        ]
        
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
        fig, ax1 = plt.subplots(figsize = (12, 6), dpi = 600)
        
        ax1.tick_params(direction = "in")
        ax1.tick_params(bottom = True, top = True, left = True, right = True)
        ax1.tick_params(pad = 20)


        ##data start##
        x = []
        x_data = []
        _y = []
        numOfData = 0
        counter = 0
        
        for line in lines:
            line = line.replace('\n','')
            data = line.split(' ')
            numOfline = len(data)
            if(numOfline <= 1):
                continue
            numOfData += 1
            for i in range(numOfline):
                if i == 0:
                    x.append(data[0])
                    x_data.append(counter)
                elif i != numOfline-1:
                    _y.append(data[i])
            counter += 1
            
        numOfAlgo = len(_y) // numOfData
        y = [[] for _ in range(numOfAlgo)]
        for i in range(numOfData * numOfAlgo):
            y[i % numOfAlgo].append(float(_y[i])) # 確保轉為 float

        for i in range(numOfData):
            x[i] = float(x[i]) / 30

        for i in range(numOfAlgo):
            for j in range(numOfData):
                y[i][j] = float(y[i][j])
        # --- 繪圖核心修改 ---
        
        # 設定每個長條的寬度
        total_width = 0.8  # 一組數據的總寬度 (0~1)
        bar_width = total_width / numOfAlgo
        
        # 設定長條圖的紋理 (Hatch)，對應原本的 marker
        patterns = ["//", "\\\\", "xx", "..", "**", "++"] 
        
        # 繪製 Bar Chart
        for i in range(numOfAlgo):
            # 計算每個長條的 X 軸位置偏移量，讓它們置中對齊
            # x_data 是 [0, 1, 2...]
            # offset 讓長條往左或往右移
            offset = (i - (numOfAlgo - 1) / 2) * bar_width
            this_x_pos = [p + offset for p in x_data]
            
            ax1.bar(
                this_x_pos, 
                y[i], 
                width = bar_width, 
                color = "white",  # 內部顏色通常設為白或淺色，讓 hatch 明顯，或是直接用 color[i]
                edgecolor = color[i], # 邊框顏色
                linewidth = 2.0,
                hatch = patterns[i % len(patterns)], # 加入紋理
                label = str(i) # 暫時標籤
            )
            
            # 如果想要實心顏色，可以改用：
            # ax1.bar(this_x_pos, y[i], width=bar_width, color=color[i], edgecolor='black')

        # --- 設定軸範圍 ---
        # 重要：長條圖不能貼齊 (min, max)，需要左右留白，否則最旁邊的長條會被切掉
        ax1.set_xlim(min(x_data)-0.415, max(x_data)+0.415)

        plt.xticks(fontsize = Xticks_fontsize)
        plt.yticks(fontsize = Yticks_fontsize)

        AlgoName = ["ours-BD", "ours-AD", "ours-GR", "CCT", "DDC-WP", "DDC-BFS"]

        leg = plt.legend(
            AlgoName,
            loc = 10,
            bbox_to_anchor = (0.24, 0.82),
            prop = {"size": fontsize-3, "family": "Times New Roman"},
            frameon = False, # 修正字串 "False" 為布林值 False 較佳，但 "False" 在某些版本也可行
            labelspacing = 0.2,
            handletextpad = 0.4, # 稍微增加間距因為 bar 比較寬
            handlelength = 0.8,
            columnspacing = 0.4,
            ncol = 2,
            facecolor = "None",
        )

        leg.get_frame().set_linewidth(0.0)
        Xlabel += self.genMultiName(Xpow)
        
        plt.subplots_adjust(top = 0.90)
        plt.subplots_adjust(left = 0.13)
        plt.subplots_adjust(right = 0.98)
        plt.subplots_adjust(bottom = 0.19)

        # 科學記號設定
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax1.yaxis.get_offset_text().set_fontsize(32)
        ax1.set_yticks([0, 500, 1000, 1500, 2000])

        plt.xticks(x_data, x) # X 軸標籤放回原本的中心點
        plt.ylabel(Ylabel, fontsize = Ylabel_fontsize, labelpad = 35)
        plt.xlabel(Xlabel, fontsize = Xlabel_fontsize, labelpad = 10)
        ax1.yaxis.set_label_coords(-0.10, 0.5)
        ax1.xaxis.set_label_coords(0.50, -0.17)
        
        # 網格線設定 (將 grid 設在 bar 的後面)
        ax1.set_axisbelow(True) 
        plt.grid(True, linestyle='--', color='0.8')

        pdfName = dataName[0:-4]
        print("save fig in "+directory_path + 'pdf/{}.jpg'.format(pdfName))
        # 確保目錄存在
        if not os.path.exists(directory_path + 'pdf/'):
            os.makedirs(directory_path + 'pdf/')
        if not os.path.exists(directory_path + 'eps/'):
            os.makedirs(directory_path + 'eps/')
            
        plt.savefig(directory_path + 'pdf/{}.jpg'.format(pdfName))
        plt.savefig(directory_path + 'eps/{}.eps'.format(pdfName))
        plt.close()

    def genMultiName(self, multiple):
        if multiple == 0:
            return str()
        else:
            return r"($\mathregular{10^{" + str(multiple) + r"}}$)"

if __name__ == "__main__":
    ChartGenerator("arrival_rate_finishedReq_all.ans", "Arrival Rate", "# Served Requests");
