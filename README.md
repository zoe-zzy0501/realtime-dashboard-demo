# 模拟期货行情看板

这是一个用 Streamlit 做的行情展示 demo。目前先用随机游走模拟棕榈油和豆油，主要是把 Python 数据更新、网页展示和云端部署这条路径跑通。

页面包括：

- 最新价、涨跌、买价和卖价
- 1 分钟 K 线
- MA5、MA10、MA20
- 成交量
- 最近几条数据
- 可分别设置两个品种的价格预警阈值

在线页面：

https://zoe-zzy0501-realtime-dashboard-demo-app-5qwn4d.streamlit.app/

## 项目结构

- `app.py`：看板页面、图表和定时刷新逻辑
- `data_source.py`：模拟行情数据源，也是后续接入真实行情的替换入口
- `requirements.txt`：运行看板需要的 Python 依赖
- `realtime_dashboard_demo.ipynb`：在 Notebook 中查看代码和启动项目的辅助入口
- `启动本地看板.command`：macOS 本地启动脚本

## 本地运行

Mac 可以直接双击 `启动本地看板.command`。脚本会优先使用 Python 3.12，没有对应安装时则使用系统中的 `python3`。第一次会安装依赖，稍等一会儿浏览器就会打开：

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

## Docker 部署

项目可以使用 Docker 部署到公司内网服务器或国内云服务器：

```bash
docker compose up -d --build
```

容器启动后，通过下面的地址访问：

```text
http://服务器IP:8501
```

在腾讯云测试时，需要在实例防火墙中允许 TCP 8501 端口。正式对外使用时，建议通过 Nginx 配置域名、HTTPS 和访问权限，不直接暴露测试端口。

查看运行状态或日志：

```bash
docker compose ps
docker compose logs -f dashboard
```

## 数据从哪里换

模拟数据放在 `data_source.py`。其中的 `get_new_bar()` 每次返回一条数据：

```text
时间、开、高、低、收、成交量
```

接真实行情时，改这个函数，让它从 API 或数据库读取最新结果，并保留这几个字段。页面上的报价、K 线、均线和表格可以继续使用。

如果指标程序仍然运行在本地电脑，需要先把结果写入一个云端数据库或 API；部署在云端的网页不能直接读取本地文件和变量。
