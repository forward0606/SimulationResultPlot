from cmath import log10
import numpy as np
import math
import os
import matplotlib.pyplot as plt
import matplotlib.transforms
import matplotlib
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

# 設定資料夾路徑 (根據您的範例改成 ans_cdf)
directory_path = "../ans_cdf2/"

class ChartGenerator:
    def __init__(self, file_list, algo_labels, outputName, Xlabel, Ylabel):
        print("start generate group: ", outputName)

        # 定義區間 (Bins)
        # 0: 0.0-0.2, 1: 0.2-0.4, 2: 0.4-0.6, 3: 0.6-0.8, 4: 0.8-1.0
        bin_labels = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]
        numOfData = len(bin_labels)
        numOfAlgo = len(file_list)

        # 初始化 y 陣列: y[algo_index][bin_index]
        y = [[0] * numOfData for _ in range(numOfAlgo)]

        # --- 1. 讀檔與統計數據 ---
        for algo_idx, filename in enumerate(file_list):
            full_path = directory_path + filename
            print(f"  Reading: {filename}")
            
            if not os.path.exists(full_path):
                print(f"    [Warning] File not found: {full_path}")
                continue

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line in lines:
                    line = line.strip()
                    if not line: continue
                    try:
                        val = float(line)
                        # 依照數值分類到對應的 Bin
                        if 0.0 <= val < 0.2:
                            y[algo_idx][0] += 1
                        elif 0.2 <= val < 0.4:
                            y[algo_idx][1] += 1
                        elif 0.4 <= val < 0.6:
                            y[algo_idx][2] += 1
                        elif 0.6 <= val < 0.8:
                            y[algo_idx][3] += 1
                        elif 0.8 <= val <= 1.0001: # 包含 1.0
                            y[algo_idx][4] += 1
                        # 超出範圍的忽略或可自行決定是否歸類到最後
                    except ValueError:
                        continue
            except Exception as e:
                print(f"    Error reading {filename}: {e}")

        # --- 2. 樣式設定 ---
        color = [
            "#FF0000", "#00FF00", 
            "#0000FF", "#000000", "#0044FF", "#0088FF", "#00CCFF"
        ]

        fontsize = 36
        Xlabel_fontsize = fontsize
        Ylabel_fontsize = fontsize
        Xticks_fontsize = 28 #稍微調小一點以免重疊
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

        # --- 3. 繪圖 (Bar Chart) ---

        # x_data 代表每個群組的中心索引: 0, 1, 2, 3, 4
        x_data = list(range(numOfData)) 

        # 設定每個長條的寬度
        total_width = 0.8  # 一組數據的總寬度
        bar_width = total_width / numOfAlgo
        patterns = ["xx", "..", "**", "++"]

        for i in range(numOfAlgo):
            # 計算偏移量
            offset = (i - (numOfAlgo - 1) / 2) * bar_width
            this_x_pos = [p + offset for p in x_data]

            ax1.bar(
                this_x_pos,
                y[i],
                width = bar_width,
                color = "white", 
                edgecolor = color[i],
                linewidth = 2.0,
                hatch = patterns[i % len(patterns)],
                label = algo_labels[i]
            )

        # --- 4. 軸與標籤設定 ---
        
        # 設定 X 軸範圍 (左右留白)
        ax1.set_xlim(min(x_data) - 0.4, max(x_data) + 0.4)

        # 設定 Y 軸 (自動取得最大值並留空間)
        max_val = max(map(max, y)) if y and y[0] else 0
        if max_val == 0: max_val = 10 # 避免全是 0 時報錯
        ax1.set_ylim(0, max_val * 1.2)

        plt.xticks(fontsize = Xticks_fontsize)
        plt.yticks(fontsize = Yticks_fontsize)

        # 圖例設定
        leg = plt.legend(
            algo_labels,
            loc = 10,
            bbox_to_anchor = (0.5, 0.90), # 調整圖例位置到上方中間
            prop = {"size": fontsize-6, "family": "Times New Roman"},
            frameon = False,
            labelspacing = 0.2,
            handletextpad = 0.4,
            handlelength = 1.2,
            columnspacing = 0.8,
            ncol = 4, # 讓圖例排成一列 (如果有4個演算法)
            facecolor = "None",
        )
        leg.get_frame().set_linewidth(0.0)

        # 版面調整
        plt.subplots_adjust(top = 0.85)
        plt.subplots_adjust(left = 0.15) # 根據 Y 軸數值大小可能需要調整
        plt.subplots_adjust(right = 0.98)
        plt.subplots_adjust(bottom = 0.20)

        # 科學記號設定 (Y軸)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax1.yaxis.get_offset_text().set_fontsize(28)

        # X 軸標籤設定
        plt.xticks(x_data, bin_labels) 
        plt.ylabel(Ylabel, fontsize = Ylabel_fontsize, labelpad = 20)
        plt.xlabel(Xlabel, fontsize = Xlabel_fontsize, labelpad = 10)
        
        # 手動調整 Label 位置
        # ax1.yaxis.set_label_coords(-0.12, 0.5) 
        ax1.xaxis.set_label_coords(0.50, -0.17)

        # 網格
        ax1.set_axisbelow(True)
        plt.grid(True, linestyle='--', color='0.8')

        # 存檔
        if not os.path.exists(directory_path + 'pdf/'):
            os.makedirs(directory_path + 'pdf/')
        if not os.path.exists(directory_path + 'eps/'):
            os.makedirs(directory_path + 'eps/')

        print("  save fig in " + directory_path + 'pdf/{}.pdf'.format(outputName))
        plt.savefig(directory_path + 'pdf/{}.pdf'.format(outputName))
        plt.savefig(directory_path + 'eps/{}.eps'.format(outputName))
        plt.close()

if __name__ == "__main__":
    
    # 定義參數
    params = ["0", "10", "20"]
    xlabels = ["Avg. Deadline 0s", "Avg. Deadline 300s", "Avg. Deadline 600s"] # 自訂 X 軸標題
    
    # 定義演算法對應的檔名字首與圖例名稱
    algo_prefixes = ["AppAlgo", "CCTAlgo", "DDC+WP+DA", "DDC+BFS+DA"]
    legend_labels = ["ours", "CCT", "DDC-WP", "DDC-BFS"]

    for j in range(len(params)):
        # 建構該回合的檔案列表
        current_files = []
        for prefix in algo_prefixes:
            # 檔名格式: AppAlgo_0_deadline.ans
            fname = f"{prefix}_{params[j]}_deadline.ans"
            current_files.append(fname)
        
        # 產出檔名
        output_filename = f"bar_deadline_{params[j]}"
        
        # 呼叫繪圖
        ChartGenerator(
            file_list = current_files, 
            algo_labels = legend_labels, 
            outputName = output_filename,
            Xlabel = "Completion Time / Deadline", # X 軸大標題
            Ylabel = "# Served Requests"      # Y 軸標題
        )
