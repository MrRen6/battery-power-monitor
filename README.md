# 电脑电量监测工具

点一下**开始检测**，程序依次跑完五个步骤，最后以大字号居中告诉你结论：**有电**。

- 纯中文界面的 Windows 小工具，单窗口、深色主题
- 检测过程 5~8 秒随机
- "有电"的字号按窗口剩余空间自动缩放，始终居中且不会超出窗口边界；窗口大小变化时会重新适配

## 下载

到 [Releases](../../releases) 下载 `BatteryCheck-v1.0.0.exe`（约 10.9 MB），PyInstaller 单文件打包，免安装，双击即可运行。

## 五个检测步骤

| 步骤 | 实际在做什么 |
| --- | --- |
| 加载依赖组件 | 进度动画，无真实操作 |
| AI 大模型思考中 | 进度动画，无真实操作 |
| 扫描电池传感器 | 进度动画，无真实操作 |
| 校验电源管理驱动 | 进度动画，无真实操作 |
| 生成监测报告 | 进度动画，无真实操作 |

需要说清楚的是：这些步骤只是视觉效果。程序不读取电池状态，也不做任何诊断，结果永远是"有电"。

## 从源码运行

只需要 Python 3.12+（自带 tkinter），无第三方依赖：

```bash
python battery_monitor.py
```

## 自己打包成 exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name BatteryCheck battery_monitor.py
```

产物在 `dist/BatteryCheck.exe`。仓库里的 `电脑电量监测工具.spec` 是同一套打包参数的固化配置，`dist/` 已被 `.gitignore` 忽略。

## 文件说明

- `battery_monitor.py` — 全部逻辑：界面布局、步骤计时、字号自适应
- `电脑电量监测工具.spec` — PyInstaller 打包配置

## 已知限制

- 仅支持 Windows（界面字体为 Microsoft YaHei UI）
- 窗口建议不小于 620×640，过小时步骤面板会挤压结果区
