import pandas as pd
import pandas_datareader as pdr
from markets import coingecko as cg
import matplotlib.pyplot as plt
import seaborn as sns


colors = sns.diverging_palette(250, 30, l=65,  as_cmap=False)
sns.set_palette(colors)

btc = cg.get_prices('bitcoin')
btc.index = pd.to_datetime(btc.index)
tens = pdr.DataReader('DGS10', 'fred', '1900-01-01')
tens.index = pd.to_datetime(tens.index)

prices = pd.concat([btc, tens], axis=1).ffill().dropna()
yo2y_tens = tens.ffill().diff(504).dropna()
yo2y_btc = btc.ffill().pct_change(504).dropna().multiply(100)
yoy_btc = btc.ffill().pct_change(252).dropna().multiply(100)

fwd = pd.concat(
    [
        yo2y_tens,  
        yo2y_btc.shift(-504), 
        yoy_btc.shift(-252)
    ], 
    axis=1
)
fwd.columns = ['10y yield yo2y delta', 'btc yo2y pct', 'btc yoy pct']
fwd.loc[:,'year'] = fwd.index.year
fwd = fwd.truncate(before='2014-09-15')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,5))

ax3 = ax1.twinx()
fwd['10y yield yo2y delta'].plot(ax=ax1)
fwd['btc yo2y pct'].plot(ax=ax3, color=colors[-1])
ax1.set_ylabel('US 10y yield yo2y change (blue)')
ax1.axhline(0, color=colors[0], linewidth=0.5)
ax3.set_ylabel('btc price yo2y pct change, 2yrs fwd (orange)')
ax3.axhline(0, color=colors[-1], linewidth=0.5)

sns.scatterplot(
    ax=ax2,
    data=fwd.truncate(before='2017-01-01').dropna(),
    x='10y yield yo2y delta',
    y='btc yo2y pct',
    hue='year',
    palette=sns.diverging_palette(250, 30, l=65,  as_cmap=True)
)
ax2.axhline(0, color='gray', linewidth=0.5)
ax2.axvline(0, color='gray', linewidth=0.5)
ax2.set_ylabel('btc price yo2y pct change, 2yrs fwd')
ax2.set_xlabel('US 10y yield yo2y change')

plt.subplots_adjust(wspace=0.3)
plt.suptitle('US 10yr Treasury Yield 2yr Momentum vs. BTC 2yr Forward Returns')

fig.savefig(
    '/home/ubuntu/projects/research/rates/rates_mo_vs_btc_scatter.png', 
    bbox_inches='tight', 
    dpi=1000, 
    facecolor='white'
)
