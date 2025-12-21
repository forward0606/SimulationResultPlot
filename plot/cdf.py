import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os


directory_path = "../ans_cdf/"
# directory_path = "../ans_deadline250/"
# directory_path = "../ans_deadline350/"


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
    with open(directory_path+filename, 'r') as f:
        arr =  np.array([float(line.strip()) for line in f if line.strip()])
        mx = 0
        for i in range(len(arr)):
            mx = max(mx, arr[i])
        print("mx = ", mx)
        return arr

def compute_cdf(data):
    data = np.sort(data)
    # data[-1] = 1.0
    cdf = np.arange(1, len(data)+1) / len(data)
    return data, cdf

def plot_cdf_from_files(file_list, labels, XLabel, output_filename="cdf_plot.jpg"):
    colors = ["#FF0000", "#00FF00", "#0000FF", "#000000",  "#900321",]
    markers = ['o', 's', 'v', 'x', 'd']

    fig, ax = plt.subplots(figsize=(7, 6), dpi=600)
    ax.tick_params(direction="in", bottom=True, top=True, left=True, right=True, pad=20)

    for i, fname in enumerate(file_list):
        data = load_data(fname)
        x, y = compute_cdf(data)
        ax.plot(
            x, y,
            label=labels[i],
            color=colors[i],
            lw=1.5,
            linestyle="-",
            zorder=-i
            # marker=markers[i],
            # markersize=15,
            # markerfacecolor="none",
            # markeredgewidth=2.5
        )

    # 標籤與圖例
    plt.ylabel("CDF", fontsize = 32, labelpad = 35)
    
    plt.xlabel(XLabel, fontsize = 32, labelpad = 10)
    ax.yaxis.set_label_coords(-0.3, 0.5)
    ax.xaxis.set_label_coords(0.45, -0.27)

    # 圖例放上方中央
    leg = plt.legend(
        labels,
        loc=10,
        bbox_to_anchor=(0.4, 1.25),
        prop={"size": 32, "family": "Times New Roman"},
        frameon=False,
        labelspacing=0.2,
        handletextpad=0.2,
        handlelength=1,
        columnspacing=0.2,
        ncol=2,
        facecolor = "None",
    )
    leg.get_frame().set_linewidth(0.0)
    
    # 自動設定 y 軸刻度
    y_max = max(1.0, max(y))
    y_ticks = np.linspace(0, y_max, 6)
    x_ticks = np.linspace(0, 1, 6)
    plt.yticks(y_ticks)
    plt.xticks(x_ticks)
    plt.xticks(fontsize = 32)
    plt.yticks(fontsize = 32)
    
    # 邊距調整
    plt.subplots_adjust(top=0.75, left=0.3, right=0.95, bottom=0.25)

    # 儲存圖檔
    output_dir = directory_path + "pdf/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    plt.savefig(os.path.join(output_dir, output_filename+".jpg"))
    plt.savefig(os.path.join(output_dir, output_filename+".eps"))
    plt.close()
    print(f"Saved plot as {output_filename}")

params=["maxBufLoad", "maxLinkLoad"]
xlabel=["Buffer Load", "Link Load"]
for j in range(len(params)):
    files = ["9", "15", "21", "27", "33"]
    for i in range(len(files)):
        files[i] = "round/10_"+files[i]+"_"+params[j]+"_.ans"
    # 執行繪圖
    plot_cdf_from_files(
        file_list=files,
        labels=["9", "15", "21", "27", "33"],
        XLabel=xlabel[j],
        output_filename=params[j]+"_cdf"
    )

