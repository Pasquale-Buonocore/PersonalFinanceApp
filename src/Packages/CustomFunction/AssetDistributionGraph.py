
# Import utility for graph
from Packages.DatabaseMng.PathManager import PathImage_Class
from matplotlib import pyplot as plt
import numpy as np

def AssetDistributionGraph(ListOfAssets = [], ListOfAssetValue = [], image_name = ''):
    # Define variables
    PathManager = PathImage_Class()
    newValue = []
    newAsset = []
    color = {}

    for assetIndex in range(0, len(ListOfAssets)):
        newValue.append(ListOfAssetValue[assetIndex])
        newAsset.append(ListOfAssets[assetIndex])
    
    ListOfAssets = ['EMPTY']
    ListOfAssetValue = [1]

    if newValue:
        ListOfAssets = newAsset
        ListOfAssetValue = newValue

    fig, ax = plt.subplots(figsize=(11, 8))
    explode = [0.05] * len(ListOfAssets)
    wedges, texts, autotexts = ax.pie(ListOfAssetValue, explode = explode, autopct='%1.1f%%', shadow=True, startangle=90)

    # Extract Color
    for ElementNum in range(0,len(wedges)): color.update({ElementNum: wedges[ElementNum]._facecolor})

    # Save plot
    plt.setp(autotexts, size = 12, weight = "bold", color = [1,1,1,1])
    plt.tight_layout()
    plt.savefig(PathManager.image_basepath + image_name + '.png', transparent = True)

    fig.clear()
    del fig

    return color