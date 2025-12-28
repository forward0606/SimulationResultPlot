import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FixedLocator, ScalarFormatter
import os

directory_path = "../ans_cdf2/"

# 設定圖形樣式
matplotlib.rcParams.update({
    "font.family": "Times New Roman",
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
    "axes.labelsize": 20,
    "axes.titlesize": 20,
    "mathtext.fontset": "custom"
})

def load_data(filename):
    print("load: ", directory_path+filename)
    try:
        with open(directory_path+filename, 'r') as f:
            arr =  np.array([float(line.strip()) for line in f if line.strip()])
            mx = 0
            if len(arr) > 0:
                mx = np.max(arr)
            print("mx = ", mx)
            return arr
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return np.array([])

def compute_cdf(data):
    # 為了讓 0 能在 Log 圖上顯示，我們將 0 視為 "等於起始刻度 (0.0001)"
    # 這樣 0 的數據點就會貼在最左邊的 Y 軸上，不會消失
    data = np.maximum(data, 0.001) 
    data = [x for x in data if x <= 1]  
    data = np.sort(data)
    cdf = np.arange(1, len(data)+1) / len(data)
    return data, cdf

def plot_cdf_from_files(file_list, labels, XLabel, output_filename="cdf_plot.jpg"):
    colors = ["#FF0000", "#00FF00", "#0000FF", "#000000",  "#900321"]
    linesty = ["-", "--", ":", "-.", (0, (3, 5, 1, 5))] 

    fig, ax = plt.subplots(figsize=(8, 6), dpi=600)
    ax.tick_params(direction="in", bottom=True, top=True, left=True, right=True, pad=20)

    for i, fname in enumerate(file_list):
        data = load_data(fname)
        if len(data) == 0: continue
        
        # 計算 CDF
        x, y = compute_cdf(data)
        
        ax.plot(
            x, y,
            label=labels[i],
            color=colors[i],
            lw=1.5,
            linestyle=linesty[i],
            zorder=7-i
        )

    # 標籤與圖例
    plt.ylabel("CDF", fontsize = 32, labelpad = 35)
    plt.xlabel(XLabel, fontsize = 32, labelpad = 10)
    
    ax.yaxis.set_label_coords(-0.25, 0.5)
    ax.xaxis.set_label_coords(0.45, -0.27)

    leg = plt.legend(
        labels,
        loc=10,
        bbox_to_anchor=(0.88, 0.27),
        prop={"size": 24},
        frameon=False,
        ncol=1,
        columnspacing=0.5,
        handletextpad=0.2
    )

    # === 核心修改區塊 ===
    
    # 1. 設定為對數座標 (這樣 0.0001->0.001 和 0.1->1 的距離才會一樣)
    #ax.set_xscale("log")
    
    # 2. 手動設定您要的 Ticks
    custom_ticks = [0.2, 0.4, 0.6, 0.8, 1.0]
    ax.set_xticks(custom_ticks)
    
    # 3. 強制設定標籤文字 (不使用科學記號 10^-4)
    #ax.set_xticklabels(["0.0001", "0.001", "0.01", "0.1", "1"], fontsize=28)
    
    # 4. 設定顯示範圍
    # left=0.0001 確保圖從 0.0001 開始，所有原本是 0 的數據都會集中在這裡
    plt.xlim(left=0.001, right=1.6) # right 設為 1.2 是為了給最右邊留點空間

    # ====================

    # Y 軸設定
    plt.yticks(np.linspace(0, 1, 6), fontsize=32)
    
    # X 軸標籤旋轉 (避免擁擠)
    #plt.xticks(rotation=20) 
    ax.yaxis.set_label_coords(-0.15, 0.5)
    ax.xaxis.set_label_coords(0.50, -0.17)
    
    # 邊距調整
    plt.subplots_adjust(top=0.90, left=0.18, right=0.95, bottom=0.20)
    plt.grid(True, linestyle='--', color='0.8')

    # 儲存
    output_dir = directory_path + "pdf/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    plt.savefig(os.path.join(output_dir, output_filename+".jpg"))
    plt.savefig(os.path.join(output_dir, output_filename+".eps"))
    plt.close()
    print(f"Saved plot as {output_filename}")

# --- 執行區塊 ---
params=["0", "10", "20"]
xlabel=["Deadline 0 Seconds", "Deadline 300 Seconds", "Deadline 600 Seconds"];
for j in range(len(params)):
    files = ["AppAlgo", "CCTAlgo", "DDC+WP+DA", "DDC+BFS+DA"]
    for i in range(len(files)):
        # AppAlgo_0_deadline.ans
        files[i] = files[i]+"_"+params[j]+"_deadline.ans"
    
    plot_cdf_from_files(
        file_list=files,
        labels=["ours", "CCT", "DDC-WP", "DDC-BFS"],
        XLabel=xlabel[j],
        output_filename=params[j]+"_cdf_log_fixed"
    )
