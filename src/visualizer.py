import matplotlib.pyplot as plt

class Visualizer:
    @staticmethod
    def plot_signals(df, symbol):
        """Generates a professional chart with Price, RSI, and Signals"""
        # Create a figure with two subplots (Price and RSI)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, 
                                       gridspec_kw={'height_ratios': [3, 1]})

        # --- Subplot 1: Price and SMAs ---
        ax1.plot(df.index, df['Close'], label='Close Price', color='blue', alpha=0.6)
        ax1.plot(df.index, df['SMA_Fast'], label='SMA Fast', color='orange', linestyle='--')
        ax1.plot(df.index, df['SMA_Slow'], label='SMA Slow', color='green', linestyle='--')

        # Add Buy signals (Green Triangles)
        buy_signals = df[df['Signal'] == 1]
        ax1.scatter(buy_signals.index, buy_signals['Close'], 
                    label='BUY', marker='^', color='green', s=100, zorder=5)

        # Add Sell signals (Red Triangles)
        sell_signals = df[df['Signal'] == -1]
        ax1.scatter(sell_signals.index, sell_signals['Close'], 
                    label='SELL', marker='v', color='red', s=100, zorder=5)

        ax1.set_title(f"{symbol} - Strategy Visualization", fontsize=16)
        ax1.set_ylabel("Price (USD)")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # --- Subplot 2: RSI ---
        ax2.plot(df.index, df['RSI'], color='purple', label='RSI')
        ax2.axhline(70, color='red', linestyle='--', alpha=0.5) # Overbought line
        ax2.axhline(30, color='green', linestyle='--', alpha=0.5) # Oversold line
        
        ax2.set_ylabel("RSI")
        ax2.set_ylim(0, 100)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show() # This opens the window with the chart