
# Import utility for graph
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from matplotlib import pyplot as plt
import numpy as np

def UpdateDashboardAsset(ListOfAssets = ['Bitcoin', 'Ethereum'], ListOfAssetValue = ['600', '400']):
    # Remove all asset with 0 %
    newValue = []
    newAsset = []

    for assetIndex in range(0, len(ListOfAssets)):
        if int(ListOfAssetValue[assetIndex]) > 0:
            newValue.append(ListOfAssetValue[assetIndex])
            newAsset.append(ListOfAssets[assetIndex])
    
    if newValue:
        ListOfAssets = newAsset
        ListOfAssetValue = newValue
    else:
        ListOfAssets = ['EMPTY']
        ListOfAssetValue = [1]

    fig, ax = plt.subplots(figsize=(11, 8))
    explode = [0.05] * len(ListOfAssets)

    wedges, texts, autotexts = ax.pie(ListOfAssetValue, explode = explode, autopct='%1.1f%%', shadow=True, startangle=90)

    ax.legend(wedges, ListOfAssets, loc="center left", prop={"size":12}, bbox_to_anchor = (1,0,0.5,1))

    plt.setp(autotexts, size = 12, weight = "bold", color = [1,1,1,1])
    #plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 1, wspace = 0)
    plt.tight_layout()
    plt.savefig('images/Support/AssetsInPortfolio.png', transparent = True)
