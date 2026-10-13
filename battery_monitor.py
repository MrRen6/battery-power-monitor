import random
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

BG = "#10141c"
PANEL = "#171d29"
TEXT = "#e6ebf5"
MUTED = "#8a97ad"
ACCENT = "#3b82f6"
DONE = "#22c55e"
RESULT_COLOR = "#22c55e"

FAMILY = "Microsoft YaHei UI"
MAX_RESULT_PT = 220  # 字号上限，实际大小按窗口剩余空间自动适配

STEPS = [
    "加载依赖组件",
    "AI 大模型思考中",
    "扫描电池传感器",
    "校验电源管理驱动",
    "生成监测报告",
]


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("电脑电量监测工具")
        w, h = 720, 760
        x = (root.winfo_screenwidth() - w) // 2
        y = max(0, (root.winfo_screenheight() - h) // 2 - 20)
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.minsize(620, 640)
        root.configure(bg=BG)

        self.running = False
        self._timers = []

        tk.Label(root, text="⚡ 电脑电量监测工具", font=(FAMILY, 17, "bold"), bg=BG, fg=TEXT).pack(
            pady=(22, 2)
        )

        self.panel = tk.Frame(root, bg=PANEL)
        self.panel.pack(fill="x", padx=30, pady=(12, 0))

        self.step_rows = []
        for name in STEPS:
            row = tk.Frame(self.panel, bg=PANEL)
            row.pack(fill="x", padx=24, pady=9)
            mark = tk.Label(row, text="○", width=3, font=(FAMILY, 12), bg=PANEL, fg=MUTED)
            mark.pack(side="left")
            label = tk.Label(row, text=name, font=(FAMILY, 12), bg=PANEL, fg=MUTED, anchor="w")
            label.pack(side="left", fill="x", expand=True)
            state = tk.Label(row, text="等待", width=8, font=(FAMILY, 11), bg=PANEL, fg=MUTED)
            state.pack(side="right")
            self.step_rows.append((mark, label, state))

        self.bar = ttk.Progressbar(self.panel, mode="determinate")
        self.bar.pack(padx=24, pady=(12, 4), fill="x")
        self.bar["value"] = 0

        self.hint = tk.Label(self.panel, text="点击下方按钮开始监测", font=(FAMILY, 11), bg=PANEL, fg=MUTED)
        self.hint.pack(pady=(2, 16))

        self.button = tk.Button(
            root,
            text="开始检测",
            font=(FAMILY, 14, "bold"),
            bg=ACCENT,
            fg="white",
            activebackground="#2f6bd6",
            activeforeground="white",
            relief="flat",
            bd=0,
            width=18,
            cursor="hand2",
            command=self.start,
        )
        self.button.pack(side="bottom", pady=(0, 24))

        # 结果区：占据窗口剩余全部空间，字号按可用区域自适应，保证不出界
        self.result_frame = tk.Frame(root, bg=BG)
        self.result_frame.pack(fill="both", expand=True, padx=20)
        self.result = tk.Label(self.result_frame, text="", bg=BG, fg=RESULT_COLOR)
        self.result.place(relx=0.5, rely=0.5, anchor="center")

        root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.bind("<Configure>", self._on_resize)

    def _on_resize(self, _event):
        if self.result.cget("text") == "有电":
            self.root.after(120, self._refit)

    def _refit(self):
        if self.result.cget("text") != "有电":
            return
        self.result.configure(font=(FAMILY, self._fit_size(), "bold"))

    def _fit_size(self):
        self.root.update_idletasks()
        avail_w = max(80, self.result_frame.winfo_width() - 20)
        avail_h = max(60, self.result_frame.winfo_height() - 20)
        probe = tkfont.Font(family=FAMILY, size=12, weight="bold")
        size = 24
        for pt in range(10, MAX_RESULT_PT + 1):
            probe.configure(size=pt)
            if probe.measure("有电") > avail_w or probe.metrics("linespace") > avail_h:
                size = max(24, pt - 1)
                break
            size = pt
        return size

    def start(self):
        if self.running:
            return
        self.running = True
        self.button.configure(text="检测中…", state="disabled", bg="#3a4457")
        for mark, label, state in self.step_rows:
            mark.configure(text="○", fg=MUTED)
            label.configure(fg=MUTED)
            state.configure(text="等待", fg=MUTED)
        self.result.configure(text="")
        self.bar["value"] = 0
        self.hint.configure(text="正在监测，请稍候…", fg=MUTED)

        total = random.uniform(5.0, 8.0)
        segment = total / len(STEPS)
        elapsed = 0.0
        for i in range(len(STEPS)):
            self._schedule(elapsed + 0.05, lambda idx=i: self._begin(idx))
            self._schedule(elapsed + segment * 0.85, lambda idx=i: self._finish(idx))
            elapsed += segment
        self._schedule(total, self.show_result)

    def _schedule(self, delay, fn):
        self._timers.append(self.root.after(int(delay * 1000), fn))

    def _begin(self, idx):
        mark, label, state = self.step_rows[idx]
        mark.configure(text="◐", fg=ACCENT)
        label.configure(fg=TEXT)
        state.configure(text="进行中", fg=ACCENT)

    def _finish(self, idx):
        mark, label, state = self.step_rows[idx]
        mark.configure(text="●", fg=DONE)
        label.configure(fg=TEXT)
        state.configure(text="完成", fg=DONE)
        self.bar["value"] = (idx + 1) / len(STEPS) * 100

    def show_result(self):
        self.bar["value"] = 100
        self.hint.configure(text="监测完成", fg=DONE)
        target = self._fit_size()
        self._reveal(target, 28)
        self.button.configure(text="再次检测", state="normal", bg=ACCENT)
        self.running = False

    def _reveal(self, target, size):
        self.result.configure(text="有电", font=(FAMILY, size, "bold"))
        if size < target:
            step = max(3, (target - size) // 5)
            self._timers.append(self.root.after(50, lambda: self._reveal(target, min(target, size + step))))

    def on_close(self):
        for t in self._timers:
            self.root.after_cancel(t)
        self.root.destroy()


def main():
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(
        "Horizontal.TProgressbar",
        troughcolor=PANEL,
        background=DONE,
        bordercolor=PANEL,
        lightcolor=DONE,
        darkcolor=DONE,
        thickness=8,
    )
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
