# 模拟期货行情看板

这是一个用 Streamlit 做的行情展示 demo。目前先用随机游走模拟棕榈油和豆油，主要是把 Python 数据更新、网页展示和云端部署这条路径跑通。

页面包括：

- 最新价、涨跌、买价和卖价
- 1 分钟 K 线
- MA5、MA10、MA20
- 成交量
- 最近几条数据

在线页面：

https://zoe-zzy0501-realtime-dashboard-demo-app-5qwn4d.streamlit.app/

## 本地运行

Mac 可以直接双击 `启动本地看板.command`。第一次会安装依赖，稍等一会儿浏览器就会打开：

```text
http://localhost:8501
```

如果 Streamlit 询问 `Email:`，不用填写，直接按回车。

也可以在终端中运行：

```bash
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m venv .dashboard_env
.dashboard_env/bin/python -m pip install -r requirements.txt
.dashboard_env/bin/python -m streamlit run app.py --browser.gatherUsageStats false
```

现在每 3 秒增加一条模拟数据。网页上的一分钟 K 线只是演示效果，所以时间走得比真实行情快。

`localhost` 只能在当前电脑打开；上面的在线页面由 Streamlit Community Cloud 运行，可以直接发给其他人。

## 数据从哪里换

模拟数据放在 `data_source.py`。其中的 `get_new_bar()` 每次返回一条数据：

```text
时间、开、高、低、收、成交量
```

接真实行情时，改这个函数，让它从 API 或数据库读取最新结果，并保留这几个字段。页面上的报价、K 线、均线和表格可以继续使用。

如果指标程序仍然运行在本地电脑，需要先把结果写入一个云端数据库或 API；部署在云端的网页不能直接读取本地文件和变量。
