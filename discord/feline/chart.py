import requests
import datetime
import discord
import matplotlib.pyplot as plt

class priceChart():
  def __init__(self,allowed_channels: list, client, address: str = '0x79ebc9a2ce02277a4b5b3a768b1c0a4ed75bd936', days: int = 5):
    self.contract_address = address
    self.url = f'https://api.coingecko.com/api/v3/coins/bsc/market_chart?vs_currency=usd&contract_address={self.contract_address}&days={days}'
    self.allowed_channels = allowed_channels
    self.client = client
    
  def fetch(self) -> dict:
    response = requests.get(self.url)
    return response.json()
    
  def plot(self) -> str:
    data = [element for element in self.fetch()['prices']]
    timestamps, prices = zip(*[(timestamp, price) for timestamp, price in data])
    datetimes = [datetime.datetime.fromtimestamp(timestamp / 1000) for timestamp in timestamps]
    prices_billion = [price * 1_000_000_000 for price in prices]
    # Set plot style
    plt.style.use('dark_background')
    # Set plot parameters
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['axes.edgecolor'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    # Create the chart
    fig, ax = plt.subplots()
    # Add grid
    ax.grid(color='white', linestyle='--', linewidth=0.5)
    # Iterate over prices and draw candles
    for i in range(1, len(prices_billion)):
        if prices_billion[i] < prices_billion[i-1]:
            color = 'red'
        else:
            color = 'green'
        ax.plot([datetimes[i], datetimes[i]], [prices_billion[i-1], prices_billion[i]], color=color, linewidth=2)
    # Set x-axis tick labels
    plt.xticks(rotation=45)
    # Set chart title and axis labels
    plt.title('Catgirl Coin price')
    plt.xlabel('')
    plt.ylabel('Price (USD per billion tokens)')
    # Save the chart as a JPEG file
    filepath = 'charts/chart.jpg'
    plt.savefig(filepath, format='jpeg')
    # Return the file path
    return filepath

  async def requestChart(self, message):
    channel = self.client.get_channel(message.channel.id)
    if channel.id not in self.allowed_channels:
      return False
    if "!chart" not in message.content:
      return False
    path = self.plot()
    await message.reply(file=discord.File(path))
