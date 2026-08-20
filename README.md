# 模拟实时行情

这个 demo 用随机数据模拟两个期货品种，页面上会显示：

- 最新价、涨跌、买价和卖价
- 1 分钟 K 线
- MA5、MA10、MA20
- 成交量
- 最近几条数据

运行方法：

Mac 可以直接双击文件夹里的 `启动本地看板.command`。第一次运行需要等待安装依赖，随后浏览器会自动打开：

```text
http://localhost:8501
```

如果看到 Streamlit 询问 `Email:`，邮箱不用填写，直接按回车即可。

也可以在终端运行：

```bash
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m venv .dashboard_env
.dashboard_env/bin/python -m pip install -r requirements.txt
.dashboard_env/bin/python -m streamlit run app.py --browser.gatherUsageStats false
```

现在是每 3 秒增加一根模拟 K 线。以后把生成随机价格的部分换成真实行情即可。

`localhost` 只能在当前电脑访问。要让其他人通过固定网址打开，需要把这个文件夹部署到 Streamlit Community Cloud 等云端服务。

## 换成真实数据

数据读取单独放在 `data_source.py` 中。现在的 `get_new_bar()` 用随机数生成一条 K 线，返回：

```text
时间、开、高、低、收、成交量
```

以后只需要修改这个函数，让它从真实行情接口、数据库或本地指标程序读取数据，并保持这几个返回字段不变。`app.py` 中的报价、K 线、均线、成交量和表格不需要重新写。
