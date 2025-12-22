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
            return
        
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        
        
        # Ydiv, Ystart, Yend, Yinterval
        Ypow = 0
        Xpow = 0

        color = [
            "#FF0000",
            "#00FF00",   
            "#0000FF",
            "#000000",
            "#0044FF",
            "#0088FF",
            "#00CCFF"
        ]
        # matplotlib.rcParams['text.usetex'] = True

        fontsize = 36
        Xlabel_fontsize = fontsize
        Ylabel_fontsize = fontsize
        Xticks_fontsize = fontsize
        Yticks_fontsize = fontsize
            
        # matplotlib.rcParams['text.usetex'] = True
        # fig, ax = plt.subplots(figsize=(8, 6), dpi=600) 
        
        andy_theme = {
        # "axes.grid": True,
        # "grid.linestyle": "--",
        # "legend.framealpha": 1,
        # "legend.facecolor": "white",
        # "legend.shadow": True,
        # "legend.fontsize": 14,
        # "legend.title_fontsize": 16,
        "xtick.labelsize": 20,
        "ytick.labelsize": 20,
        "axes.labelsize": 20,
        "axes.titlesize": 20,
        "font.family": "Times New Roman",
        "mathtext.it": "Times New Roman:italic",
        "mathtext.rm": "Times New Roman",
        # "mathtext.default": "regular",
        "mathtext.fontset": "custom"
        # "mathtext.fontset": "custom"
        # "figure.autolayout": True
        # "text.usetex": True,
        # "figure.dpi": 100,
        }
        
        matplotlib.rcParams.update(andy_theme)
        fig, ax1 = plt.subplots(figsize = (8, 6), dpi = 600)
        # ax1.spines['top'].set_linewidth(1.5)
        # ax1.spines['right'].set_linewidth(1.5)
        # ax1.spines['bottom'].set_linewidth(1.5)
        # ax1.spines['left'].set_linewidth(1.5)
        ax1.tick_params(direction = "in")
        ax1.tick_params(bottom = True, top = True, left = True, right = True)
        ax1.tick_params(pad = 20)


        ##data start##
        x = []
        x_data = []
        _y = []
        numOfData = 0
        counter = 0
        line_cnt = 3
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
                    line_cnt += 1
                elif i != numOfline-1:
                    _y.append(data[i])
            #print(_y)
            counter += 1
        numOfAlgo = len(_y) // numOfData

        y = [[] for _ in range(numOfAlgo)]
        for i in range(numOfData * numOfAlgo):
            y[i % numOfAlgo].append(_y[i])

        #print(x)
        #print(y)

        maxData = 0
        minData = math.inf

        for i in range(-10, -1, 1):
            if float(x[numOfData - 1]) <= 10 ** i:
                Xpow = (i - 2)

        for k in range(-10, -1, 1):
            for i in range(numOfAlgo):
                for j in range(numOfData):
                    if(float(y[i][j]) <= 10 ** k):
                        Ypow = k-2

        Ypow = 3
        Ydiv = float(10 ** Ypow)
        Xdiv = float(10 ** Xpow)
        
        for i in range(numOfData):
            x[i] = float(x[i]) / Xdiv
            x[i] = int(x[i])
        
        x = ["7x5", "7x6", "7x7", "7x8", "7x9"]
        
        for i in range(numOfAlgo):
            for j in range(numOfData):
                y[i][j] = float(y[i][j])
                maxData = max(maxData, y[i][j])
                minData = min(minData, y[i][j])

        # Yend = 0
        # Ystart = 0
        # Yinterval = 0.6

        ax1.set_xlim(min(x_data), max(x_data))

        marker = ['o', 's', 'v', 'x', 'd', 'p']
        linesty = ["-", "--", ":", "-."]
        for i in range(numOfAlgo):
            ax1.plot(x_data, y[i], color = color[i], lw = 2.5, linestyle = linesty[i], marker = marker[i], markersize = 15, markerfacecolor = "none", markeredgewidth = 2.5, clip_on=False)
        # plt.show()

        plt.xticks(fontsize = Xticks_fontsize)
        plt.yticks(fontsize = Yticks_fontsize)
        
        AlgoName = ["ours", "CCT", "DDC-WP", "DDC-BFS"] # "MyAlgo1", "MyAlgo2",

        leg = plt.legend(
            AlgoName,
            loc = 10,
            bbox_to_anchor = (0.34, 0.88),
            prop = {"size": fontsize-3, "family": "Times New Roman"},
            frameon = "False",
            labelspacing = 0.2,
            handletextpad = 0.2,
            handlelength = 1,
            columnspacing = 0.1,
            ncol = 2,
            facecolor = "None",
        )

        leg.get_frame().set_linewidth(0.0)
        # Ylabel += self.genMultiName(Ypow)
        Xlabel += self.genMultiName(Xpow)
        plt.subplots_adjust(top = 0.90)
        plt.subplots_adjust(left = 0.18)
        plt.subplots_adjust(right = 0.95)
        plt.subplots_adjust(bottom = 0.20)

        # plt.yticks(np.arange(Ystart, Yend + Yinterval, step = Yinterval), fontsize = Yticks_fontsize)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax1.yaxis.get_offset_text().set_fontsize(32)
        ax1.set_yticks([0, 300, 600, 900, 1200])
        
        plt.xticks(x_data, x)
        plt.ylabel(Ylabel, fontsize = Ylabel_fontsize, labelpad = 35)
        plt.xlabel(Xlabel, fontsize = Xlabel_fontsize, labelpad = 10)
        ax1.yaxis.set_label_coords(-0.15, 0.5)
        ax1.xaxis.set_label_coords(0.50, -0.17)
        plt.grid(True, linestyle='--', color='0.8') 

        pdfName = dataName[0:-4]
        # plt.savefig('./pdf/{}.eps'.format(pdfName)) 
        print("save fig in "+directory_path + 'pdf/{}.jpg'.format(pdfName))
        plt.savefig(directory_path + 'pdf/{}.jpg'.format(pdfName)) 
        plt.savefig(directory_path + 'eps/{}.eps'.format(pdfName)) 
        # Xlabel = Xlabel.replace(' (%)','')
        # Xlabel = Xlabel.replace('# ','')
        # Ylabel = Ylabel.replace('# ','')
        plt.close()

    def genMultiName(self, multiple):
        if multiple == 0:
            return str()
        else:
            return r"($\mathregular{10^{" + str(multiple) + r"}}$)"

if __name__ == "__main__":
    ChartGenerator("num_of_satellite_finishedReq.ans", "# Satellites", "# Served Requests");
