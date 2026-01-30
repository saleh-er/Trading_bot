import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Visualizer:
    @staticmethod
    def plot_professional(df, symbol):
        """
        Generates a high-end interactive financial dashboard using Plotly.
        Includes Candlesticks, SMAs, Bollinger Bands, Volume, RSI, and MACD.
        """
        
        # Industry standard color palette (TradingView Style)
        COLOR_UP = '#089981'        # Emerald Green
        COLOR_DOWN = '#F23645'      # Vivid Red
        COLOR_SMA_FAST = '#FF9800'   # Amber/Orange
        COLOR_SMA_SLOW = '#2196F3'   # Marine Blue
        COLOR_RSI = '#9C27B0'        # Deep Purple
        COLOR_BB_FILL = 'rgba(173, 216, 230, 0.15)' # Translucent light blue for bands

        # 4-tier layout: Price (50%), Volume (10%), RSI (20%), MACD (20%)
        fig = make_subplots(
            rows=4, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.02, 
            row_heights=[0.5, 0.1, 0.2, 0.2],
            subplot_titles=(f'{symbol} - MAIN CHART', 'VOLUME', 'RSI', 'MACD MOMENTUM')
        )

        # --- 1. PRIMARY CHART: Candlesticks & Overlays ---
        # Bollinger Bands Shading (Added as Scatter traces with 'tonexty' fill)
        fig.add_trace(go.Scatter(
            x=df.index, y=df['BB_High'], 
            line=dict(color=COLOR_BB_FILL, width=0), 
            showlegend=False, hoverinfo='skip'
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=df.index, y=df['BB_Low'], 
            fill='tonexty', fillcolor=COLOR_BB_FILL, 
            line=dict(color=COLOR_BB_FILL, width=0), 
            name="Bollinger Bands", hoverinfo='skip'
        ), row=1, col=1)

        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            increasing_line_color=COLOR_UP, decreasing_line_color=COLOR_DOWN,
            increasing_fillcolor=COLOR_UP, decreasing_fillcolor=COLOR_DOWN,
            name="Price Action"
        ), row=1, col=1)

        # SMAs
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_Fast'], name="Fast SMA", line=dict(color=COLOR_SMA_FAST, width=1.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_Slow'], name="Slow SMA", line=dict(color=COLOR_SMA_SLOW, width=1.5)), row=1, col=1)

        # Execution Signals (Keep your markers)
        buys = df[df['Signal'] == 1]
        sells = df[df['Signal'] == -1]
        fig.add_trace(go.Scatter(x=buys.index, y=buys['Low']*0.98, mode='markers', name='BUY', marker=dict(symbol='triangle-up', size=14, color='#3fff00', line=dict(width=1, color='white'))), row=1, col=1)
        fig.add_trace(go.Scatter(x=sells.index, y=sells['High']*1.02, mode='markers', name='SELL', marker=dict(symbol='triangle-down', size=14, color='#ff0000', line=dict(width=1, color='white'))), row=1, col=1)

        # --- 2. VOLUME ---
        vol_colors = [COLOR_UP if c >= o else COLOR_DOWN for o, c in zip(df['Open'], df['Close'])]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color=vol_colors, opacity=0.6), row=2, col=1)

        # --- 3. RSI ---
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI", line=dict(color=COLOR_RSI, width=2)), row=3, col=1)
        fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1, line_width=0, row=3, col=1)
        fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1, line_width=0, row=3, col=1)

        # --- 4. MACD HISTOGRAM ---
        macd_colors = [COLOR_UP if val >= 0 else COLOR_DOWN for val in df['MACD_Diff']]
        fig.add_trace(go.Bar(x=df.index, y=df['MACD_Diff'], name="MACD Hist", marker_color=macd_colors), row=4, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name="MACD Line", line=dict(color='white', width=1)), row=4, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name="Signal Line", line=dict(color='yellow', width=1)), row=4, col=1)

        # UI & LAYOUT
        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])], gridcolor='#2D2E32', zeroline=False)
        fig.update_yaxes(gridcolor='#2D2E32', zeroline=False)
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='#131722', plot_bgcolor='#131722',
            xaxis_rangeslider_visible=False, height=1100, # Increased height for 4 rows
            margin=dict(l=50, r=50, t=80, b=50),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified"
        )
        
        return fig