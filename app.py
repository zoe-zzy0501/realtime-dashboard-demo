"""Streamlit page for the simulated futures market dashboard."""

from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from data_source import get_new_bar


PAGE_TITLE = "模拟期货行情"
REFRESH_SECONDS = 3
REFRESH_INTERVAL = f"{REFRESH_SECONDS}s"
INITIAL_BAR_COUNT = 30
CHART_BAR_COUNT = 40
MOVING_AVERAGE_WINDOWS = (5, 10, 20)
RECENT_ROW_COUNT = 6

PRODUCTS = {
    "棕榈油 2609": 9437,
    "豆油 2609": 8485,
}

st.set_page_config(page_title=PAGE_TITLE, layout="wide")
st.title(PAGE_TITLE)
st.caption(f"随机数据演示，每 {REFRESH_SECONDS} 秒刷新一次")

st.sidebar.header("价格预警")
st.sidebar.caption("最新价超过设定值时，页面会显示预警提示。")
alert_thresholds = {
    name: st.sidebar.number_input(
        f"{name} 预警价",
        min_value=1,
        value=start_price + 20,
        step=1,
        key=f"alert_threshold_{name}",
    )
    for name, start_price in PRODUCTS.items()
}


# 第一次打开时先准备一段历史数据，避免图表为空
if "market_data" not in st.session_state:
    st.session_state.market_data = {}

    for name, start_price in PRODUCTS.items():
        rows = []
        start_time = datetime.now() - timedelta(minutes=INITIAL_BAR_COUNT - 1)
        last_price = start_price
        last_time = start_time - timedelta(minutes=1)

        for _ in range(INITIAL_BAR_COUNT):
            bar = get_new_bar(name, last_price, last_time)

            rows.append(
                [
                    bar["时间"],
                    bar["开"],
                    bar["高"],
                    bar["低"],
                    bar["收"],
                    bar["成交量"],
                ]
            )
            last_price = bar["收"]
            last_time = bar["时间"]

        columns = ["时间", "开", "高", "低", "收", "成交量"]
        st.session_state.market_data[name] = pd.DataFrame(rows, columns=columns)


@st.fragment(run_every=REFRESH_INTERVAL)
def show_market():
    panels = st.columns(2)

    for panel, (name, start_price) in zip(panels, PRODUCTS.items()):
        data = st.session_state.market_data[name]
        old_price = int(data.iloc[-1]["收"])

        bar = get_new_bar(name, old_price, data.iloc[-1]["时间"])
        close_price = bar["收"]
        volume = bar["成交量"]

        data.loc[len(data)] = [
            bar["时间"],
            bar["开"],
            bar["高"],
            bar["低"],
            bar["收"],
            bar["成交量"],
        ]
        data = data.tail(CHART_BAR_COUNT).reset_index(drop=True)
        st.session_state.market_data[name] = data

        change = close_price - start_price
        change_pct = change / start_price * 100
        bid_price = close_price - 2
        ask_price = close_price + 2
        alert_threshold = int(alert_thresholds[name])

        with panel:
            st.subheader(name)

            p1, p2, p3 = st.columns([1.3, 1, 1])
            p1.metric(
                "最新价",
                str(close_price),
                f"{change:+d}  {change_pct:+.2f}%",
            )
            p2.metric("买价", str(bid_price))
            p3.metric("卖价", str(ask_price))

            if close_price > alert_threshold:
                st.error(
                    f"价格预警：最新价 {close_price} 已超过设定值 "
                    f"{alert_threshold}"
                )
            else:
                st.caption(
                    f"预警价 {alert_threshold}  |  "
                    f"距离预警价 {alert_threshold - close_price}"
                )

            st.caption(
                "1分钟  |  "
                f"本轮成交量 {volume}  |  "
                f"更新时间 {datetime.now().strftime('%H:%M:%S')}"
            )

            chart_data = data.copy()
            for window in MOVING_AVERAGE_WINDOWS:
                chart_data[f"MA{window}"] = chart_data["收"].rolling(window).mean()

            fig = make_subplots(
                rows=2,
                cols=1,
                shared_xaxes=True,
                row_heights=[0.75, 0.25],
                vertical_spacing=0.04,
            )

            fig.add_trace(
                go.Candlestick(
                    x=data["时间"],
                    open=data["开"],
                    high=data["高"],
                    low=data["低"],
                    close=data["收"],
                    name="K线",
                    increasing_line_color="#ef5350",
                    decreasing_line_color="#26a69a",
                    increasing_fillcolor="#ef5350",
                    decreasing_fillcolor="#26a69a",
                ),
                row=1,
                col=1,
            )

            fig.add_hline(
                y=alert_threshold,
                line_dash="dot",
                line_color="#ff9800",
                annotation_text=f"预警价 {alert_threshold}",
                annotation_position="top left",
                row=1,
                col=1,
            )

            for window in MOVING_AVERAGE_WINDOWS:
                fig.add_trace(
                    go.Scatter(
                        x=chart_data["时间"],
                        y=chart_data[f"MA{window}"],
                        name=f"MA{window}",
                    ),
                    row=1,
                    col=1,
                )

            bar_colors = [
                "#ef5350" if close >= open_ else "#26a69a"
                for open_, close in zip(data["开"], data["收"])
            ]
            fig.add_trace(
                go.Bar(
                    x=data["时间"],
                    y=data["成交量"],
                    marker_color=bar_colors,
                    name="成交量",
                ),
                row=2,
                col=1,
            )

            fig.update_layout(
                height=520,
                margin=dict(l=10, r=10, t=25, b=10),
                xaxis_rangeslider_visible=False,
                legend=dict(orientation="h", y=1.03, x=0),
                plot_bgcolor="white",
                paper_bgcolor="white",
            )
            fig.update_xaxes(showgrid=True, gridcolor="#eeeeee")
            fig.update_yaxes(showgrid=True, gridcolor="#eeeeee")

            st.plotly_chart(
                fig,
                width="stretch",
                config={"displayModeBar": False},
                key=f"chart_{name}",
            )

            recent = data.tail(RECENT_ROW_COUNT).iloc[::-1][
                ["时间", "开", "高", "低", "收", "成交量"]
            ].copy()
            recent["时间"] = recent["时间"].dt.strftime("%H:%M")
            st.dataframe(recent, hide_index=True, width="stretch", height=250)


show_market()
