import matplotlib.pyplot as plt
import math

class Visualizer:
    @staticmethod
    def plot_multi_assets(data_dict):
        """
        data_dict: Dictionary where key is 'Symbol' and value is its DataFrame
        """
        n_assets = len(data_dict)
        cols = 2  # Set to 2 or 3 columns
        rows = math.ceil(n_assets / cols)

        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows), sharex=True)
        axes = axes.flatten() # Flatten 2D array to 1D for easy looping

        for i, (symbol, df) in enumerate(data_dict.items()):
            ax = axes[i]
            # Plot Price
            ax.plot(df.index, df['Close'], label='Close', color='blue', alpha=0.5)
            
            # Add Buy/Sell Markers
            buys = df[df['Signal'] == 1]
            sells = df[df['Signal'] == -1]
            ax.scatter(buys.index, buys['Close'], marker='^', color='green', s=50)
            ax.scatter(sells.index, sells['Close'], marker='v', color='red', s=50)

            ax.set_title(f"{symbol} Signals", fontsize=12)
            ax.legend(loc='upper left', fontsize=8)
            ax.grid(True, alpha=0.2)

        # Hide unused subplots if n_assets is odd
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')

        plt.tight_layout()
        plt.show()