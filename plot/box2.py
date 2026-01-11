import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import os

# 指定檔案路徑
file_path = "../ans_cdf/round/10_15_maxLinkLoad_.ans"

# 設定圖形樣式
matplotlib.rcParams.update({
    "font.family": "Times New Roman",
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "axes.labelsize": 18,
    "axes.titlesize": 20,
    "mathtext.fontset": "custom"
})

def load_data(filename):
    print(f"Loading: {filename}")
    try:
        with open(filename, 'r') as f:
            arr = np.array([float(line.strip()) for line in f if line.strip()])
            return arr
    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
        return np.array([])

# --- 主程式 ---
data = load_data(file_path)

if len(data) > 0:
    # 建立畫布
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.tick_params(direction="in", bottom=True, top=True, left=True, right=True, pad=10)

    # 1. 設定 Bins (區間)
    # 我們需要足夠細的 bin 來區分 0 和非 0，同時確保 1.0 落在 bin 的邊界上
    max_val = max(np.max(data), 1.5) # 確保圖表至少畫到 1.5
    # 策略：0 獨立一個 bin 有點難 (因為是連續直方圖)，但我們可以切很細
    bins = np.linspace(0, max_val, 50) 

    # 2. 繪製直方圖 (開啟 log=True)
    # n: 每個 bin 的計數, bins: 邊界, patches: 柱狀圖物件(用於上色)
    n, bins, patches = ax.hist(data, bins=bins, log=True, edgecolor='black', linewidth=0.5)

    # 3. 條件上色 (Highlight Logic)
    # 遍歷每一個柱子 (patch)
    for i in range(len(patches)):
        # 取得這個 bin 的中心點或左邊界
        left_edge = bins[i]
        right_edge = bins[i+1]
        
        # 邏輯 A: 如果這個 bin 包含 1.0 以上的數值 -> 紅色
        if left_edge >= 1.0:
            patches[i].set_facecolor('#d62728') # 紅色 (Overloaded)
            patches[i].set_label('Overloaded (> 1.0)' if 'Overloaded (> 1.0)' not in [l.get_label() for l in ax.patches] else "")
        
        # 邏輯 B: 如果是第一個 bin (通常包含 0) 且計數非常高 -> 灰色
        # 這裡假設第一個 bin 主要是 0
        elif i == 0:
            patches[i].set_facecolor('#bfbfbf') # 灰色 (Idle/Low)
            patches[i].set_label('Idle / Low (~0)')
            
        # 邏輯 C: 其他正常負載 -> 藍色
        else:
            patches[i].set_facecolor('#1f77b4') # 藍色 (Normal)
            patches[i].set_label('Normal (0-1)')

    # 4. 裝飾圖表
    # 加入 x=1 的分界線
    ax.axvline(x=1.0, color='black', linestyle='--', linewidth=2, alpha=0.8)
    ax.text(1.05, ax.get_ylim()[1]*0.5, 'Threshold (1.0)', rotation=90, verticalalignment='center', fontsize=14)

    # 計算統計數據顯示在圖上
    total_count = len(data)
    overload_count = np.sum(data > 1)
    overload_ratio = (overload_count / total_count) * 100
    
    stats_text = (
        f"Total Links: {total_count}\n"
        f"Overloaded: {overload_count}\n"
        f"Ratio: {overload_ratio:.2f}%"
    )
    
    # 在右上角加入文字框
    props = dict(boxstyle='round', facecolor='white', alpha=0.9)
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    # 設定標籤
    plt.xlabel("Link Load", fontsize=24, labelpad=10)
    plt.ylabel("Count", fontsize=24, labelpad=10) # 註明是對數刻度
    
    # 設定格線 (對數軸需要 major 和 minor grid 才好看)
    ax.grid(True, which="major", axis="y", linestyle="-", alpha=0.5)
    ax.grid(True, which="minor", axis="y", linestyle=":", alpha=0.3)

    # 防止圖例重複 (因為我們在迴圈裡設 label)
    # 手動建立圖例物件
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#bfbfbf', edgecolor='black', label='Idle / Low (~0)'),
        Patch(facecolor='#1f77b4', edgecolor='black', label='Normal (0 < x ≤ 1)'),
        Patch(facecolor='#d62728', edgecolor='black', label='Overloaded (x > 1)')
    ]
    ax.legend(handles=legend_elements, loc='center right', fontsize=10, frameon=True)

    plt.tight_layout()

    # 5. 存檔
    output_dir = "../ans_cdf/pdf/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_filename = "5_15_LinkLoad_LogHist"
    plt.savefig(os.path.join(output_dir, output_filename + ".pdf"))
    # plt.savefig(os.path.join(output_dir, output_filename + ".eps"))
    plt.show()
    print(f"Saved plot to {output_dir}{output_filename}.pdf")

else:
    print("No data found.")
