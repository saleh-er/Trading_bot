import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Visualizer:
    @staticmethod
    def plot_professional(df, symbol):
        """
        Generates a high-end interactive financial dashboard using Plotly.
        Includes Candlesticks, Volume, RSI, and SMA overlays.
        """
        
        # Industry standard color palette (TradingView Style)
        COLOR_UP = '#089981'        # Emerald Green
        COLOR_DOWN = '#F23645'      # Vivid Red
        COLOR_SMA_FAST = '#FF9800'   # Amber/Orange
        COLOR_SMA_SLOW = '#2196F3'   # Marine Blue
        COLOR_RSI = '#9C27B0'        # Deep Purple

        # Create a 3-tier layout: Price (60%), Volume (15%), RSI (25%)
        fig = make_subplots(
            rows=3, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.02, 
            row_heights=[0.6, 0.15, 0.25],
            subplot_titles=(f'{symbol} - MAIN CHART', 'VOLUME', 'RELATIVE STRENGTH INDEX (RSI)')
        )

        # 1. PRIMARY CHART: Candlesticks
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            increasing_line_color=COLOR_UP, decreasing_line_color=COLOR_DOWN,
            increasing_fillcolor=COLOR_UP, decreasing_fillcolor=COLOR_DOWN,
            name="Price Action"
        ), row=1, col=1)

        # 2. OVERLAYS: Simple Moving Averages (SMA)
        fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA_Fast'], 
            name="Fast SMA (20)", 
            line=dict(color=COLOR_SMA_FAST, width=1.5)
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA_Slow'], 
            name="Slow SMA (50)", 
            line=dict(color=COLOR_SMA_SLOW, width=1.5)
        ), row=1, col=1)

        # 3. VOLUME: Dynamic coloring based on price movement
        # Green bar if Close > Open, Red if Close < Open
        vol_colors = [COLOR_UP if c >= o else COLOR_DOWN for o, c in zip(df['Open'], df['Close'])]
        
        fig.add_trace(go.Bar(
            x=df.index, y=df['Volume'], 
            name="Volume", 
            marker_color=vol_colors, 
            opacity=0.6
        ), row=2, col=1)

        # 4. SIGNALS: Buy & Sell Execution Markers
        buys = df[df['Signal'] == 1]
        sells = df[df['Signal'] == -1]

        # Buy Markers (Positioned slightly below Low price)
        fig.add_trace(go.Scatter(
            x=buys.index, y=buys['Low'] * 0.98,
            mode='markers', name='BUY SIGNAL',
            marker=dict(symbol='triangle-up', size=14, color='#3fff00', line=dict(width=1, color='white')),
            hovertemplate="ENTRY BUY at %{y:.2f}<extra></extra>"
        ), row=1, col=1)

        # Sell Markers (Positioned slightly above High price)
        fig.add_trace(go.Scatter(
            x=sells.index, y=sells['High'] * 1.02,
            mode='markers', name='SELL SIGNAL',
            marker=dict(symbol='triangle-down', size=14, color='#ff0000', line=dict(width=1, color='white')),
            hovertemplate="EXIT SELL at %{y:.2f}<extra></extra>"
        ), row=1, col=1)

        # 5. OSCILLATOR: RSI with Overbought/Oversold shading
        fig.add_trace(go.Scatter(
            x=df.index, y=df['RSI'], 
            name="RSI", 
            line=dict(color=COLOR_RSI, width=2)
        ), row=3, col=1)
        
        # Shading for extreme zones (Visual Thresholds)
        fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1, line_width=0, row=3, col=1)
        fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1, line_width=0, row=3, col=1)
        
        # Threshold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)

        # 6. UI & LAYOUT: TradingView Dark Theme
        fig.update_xaxes(
            rangebreaks=[dict(bounds=["sat", "mon"])], # Remove market gaps on weekends for stocks
            gridcolor='#2D2E32',
            zeroline=False
        )
        
        fig.update_yaxes(gridcolor='#2D2E32', zeroline=False)

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='#131722', # Chart Background
            plot_bgcolor='#131722',
            xaxis_rangeslider_visible=False,
            height=900,
            margin=dict(l=50, r=50, t=80, b=50),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified" # Shows all data points at a specific date on hover
        )
        
        return fig