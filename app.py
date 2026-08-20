from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from data_source import get_new_bar


st.set_page_config(page_title="模拟实时行情", layout="wide")
st.title("模拟期货实时行情")
st.caption("目前使用随机数据，每 3 秒更新一次")


products = {
    "棕榈油 2609": 9437,
    "豆油 2609": 8485,
}


# 第一次打开页面时，先准备 30 根 K 线
if "market_data" not in st.session_state:
    st.session_state.market_data = {}

    for name, start_price in products.items():
        rows = []
        start_time = datetime.now() - timedelta(minutes=29)
        last_price = start_price
        last_time = start_time - timedelta(minutes=1)

        for _ in range(30):
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

        st.session_state.market_data[name] = pd.DataFrame(
            rows,
            columns=["时间", "开", "高", "低", "收", "成交量"],
        )


@st.fragment(run_every="3s")
def show_market():
    left, right = st.columns(2)

    for panel, (name, start_price) in zip([left, right], products.items()):
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
        data = data.tail(40).reset_index(drop=True)
        st.session_state.market_data[name] = data

        change = close_price - start_price
        change_pct = change / start_price * 100
        bid_price = close_price - 2
        ask_price = close_price + 2

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

            st.caption(
                "1分钟  |  "
                f"本轮成交量 {volume}  |  "
                f"更新时间 {datetime.now().strftime('%H:%M:%S')}"
            )

            chart_data = data.copy()
            chart_data["MA5"] = chart_data["收"].rolling(5).mean()
            chart_data["MA10"] = chart_data["收"].rolling(10).mean()
            chart_data["MA20"] = chart_data["收"].rolling(20).mean()

            figure = make_subplots(
                rows=2,
                cols=1,
                shared_xaxes=True,
                row_heights=[0.75, 0.25],
                vertical_spacing=0.04,
            )

            figure.add_trace(
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

            figure.add_trace(
                go.Scatter(
                    x=chart_data["时间"], y=chart_data["MA5"], name="MA5"
                ),
                row=1,
                col=1,
            )
            figure.add_trace(
                go.Scatter(
                    x=chart_data["时间"], y=chart_data["MA10"], name="MA10"
                ),
                row=1,
                col=1,
            )
            figure.add_trace(
                go.Scatter(
                    x=chart_data["时间"], y=chart_data["MA20"], name="MA20"
                ),
                row=1,
                col=1,
            )

            bar_colors = [
                "#ef5350" if close >= open_ else "#26a69a"
                for open_, close in zip(data["开"], data["收"])
            ]
            figure.add_trace(
                go.Bar(
                    x=data["时间"],
                    y=data["成交量"],
                    marker_color=bar_colors,
                    name="成交量",
                ),
                row=2,
                col=1,
            )

            figure.update_layout(
                height=520,
                margin=dict(l=10, r=10, t=25, b=10),
                xaxis_rangeslider_visible=False,
                legend=dict(orientation="h", y=1.03, x=0),
                plot_bgcolor="white",
                paper_bgcolor="white",
            )
            figure.update_xaxes(showgrid=True, gridcolor="#eeeeee")
            figure.update_yaxes(showgrid=True, gridcolor="#eeeeee")

            st.plotly_chart(
                figure,
                width="stretch",
                config={"displayModeBar": False},
                key=f"chart_{name}",
            )

            recent = data.tail(6).iloc[::-1][
                ["时间", "开", "高", "低", "收", "成交量"]
            ].copy()
            recent["时间"] = recent["时间"].dt.strftime("%H:%M")
            st.dataframe(recent, hide_index=True, width="stretch", height=250)


show_market()
