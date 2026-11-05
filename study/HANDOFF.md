# 交接文件：amr_forklift 自主堆高機學習專案

> 暫停時間：2026-11-06 04:50（台北），暫停機器：**HP1**（Windows 11＋WSL Ubuntu-24.04＋ROS 2 Jazzy）
> 程式與文件：<https://github.com/chenghyang2001/amr_forklift> 的 **`study` 分支**（fork 自 furkankarsli/amr_forklift，作者原檔沒改）

---

## 1. 這個專案在做什麼

使用者要求的五件事與狀態：

| # | 工作 | 狀態 | 產物 |
| --- | --- | --- | --- |
| 1 | clone 原專案並分析 | ✅ | `~/workspace/amr_forklift`（原網址 `amr_forklif` 少一個 t，正確是 `amr_forklift`） |
| 2 | 給大一新生的完整導讀 | ✅ | `study/01-新手完整導讀.md`（13 章） |
| 3 | 導讀放進 NotebookLM，做語音、影片、簡報、心智圖 | ✅ | notebook `0dd71297-666e-4679-88bb-f59e66a645b9`，四件都 completed（心智圖標題沒改成功，其他三件已正名「01-…」） |
| 4 | 在 PC 的 WSL＋ROS 2 把範例跑起來並分析 | ✅ | `study/jazzy/` 移植檔、`study/02-逐步實作講解.md`、`study/run-logs/` |
| 5 | 現場一步一步講解（tmux 多格＋語音＋錄影） | ⏸️ **進行中，暫停在這裡** | `study/drill/20261106-amr-sim/` |
| 附 | Amazon Kindle「AMR＋ROS 2」評價最好的前 5 本 | ✅ | `study/kindle-amr-ros2-top5.md` |

NotebookLM：<https://notebooklm.google.com/notebook/0dd71297-666e-4679-88bb-f59e66a645b9>

---

## 2. 現場演練（第 5 項）停在哪裡

計畫共 9 步，見 `study/drill/20261106-amr-sim/plan.md`。

| 進度 | 內容 |
| --- | --- |
| ✅ 開場 | 畫面介紹＋9 步總覽（語音 `00-opening`） |
| ✅ 插話 | AMR 與 AGV 的差別（語音 `01-explain-amr-agv`，對照表 `amr_vs_agv.txt`） |
| ⏭️ **下一步＝第 1 步** | 在 ④ 格認識工作區：`ls src/amr_forklift`＋`git -C src/amr_forklift status --short` |
| 未做 | 第 2～9 步：通訊測試 → 開 Gazebo → 看感測器 → 看雷射過濾 → SLAM＋Nav2 → 導航目標 → 行為樹緊急停止與充電 → 總結做影片 |

錄影：第一段已錄完（04:10～04:50），在 **HP1 本機** `~/Videos/amr-drill/amrdrill-20261106-041024.mp4`（51 MB，**沒上雲**）。
繼續時開新的一段錄影，最後做影片時把兩段接起來（只有在 HP1 上接才拿得到第一段）。

---

## 3. 一定要知道的事（踩過的坑）

1. **環境不同**：作者用 Humble＋Gazebo Classic；這裡是 Jazzy＋Gazebo Harmonic。新增 6 個檔（`study/jazzy/`），複製到 WSL 套件同名資料夾後 `colcon build`。
2. **作者程式 bug**：`amr_behavior_tree.py` 的 `self.logger.critical(` 會讓緊急停止時節點當掉 → 改成 `self.logger.error(`（`study/jazzy/patches/estop-logger-fix.patch`）。改完**一定要重新 colcon build**（CMake 是複製安裝，不是連結）。
3. **HP1 的 WSL 用 FastDDS 時節點互相看不到** → 每個終端機先 `export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`。
4. **螢幕編號**：使用者說的「螢幕 3」是 Windows 設定裡的 3＝**主螢幕右邊那台**（HP1 上是 `\\.\DISPLAY2`，DPI 感知座標 x=1920～3840）。**螢幕 1 絕對不要放東西。** 錄影腳本 `drill-record.ps1` 用 `-Monitor 3`。
5. **擺視窗**：Python 先 `SetProcessDpiAwarenessContext(-4)`，`SetWindowPos` 要呼叫兩次（第一次跨螢幕時大小會被縮放）。
6. **Windows Terminal 標題不能有空白**（`--title 'AMR 演練'` 會把「演練」當指令），用 `AMR演練`。
7. **殺程序別自殺**：在 `bash -c "..."` 裡用 `awk "/[r]os2|.../"` 時，每個字串都要加括號（例如 `[_]server`），否則會殺到自己（exit 9）。
8. **NotebookLM 一律走 VPS**：`ssh claude@187.127.109.145`，CLI 絕對路徑 `/home/claude/.local/bin/notebooklm`。
9. **出生點在場地角落**：前方 1.15 m、右方 1.9 m 是牆；導航目標用 map 座標 `(-3.0, 1.0)`（實測 39 秒抵達）。`(1.2, 0)` 會回 error 204（地圖外）。

---

## 4. 在 HP1 上繼續

tmux session `amr` 可能還在（WSL 沒關機的話）。檢查：

```bash
wsl -d Ubuntu-24.04 -e tmux ls
```

- 還在：把 Windows Terminal 視窗「AMR演練」擺回螢幕 3 左半（x=1920, y=0, 960×1032），④ 格執行 `tmux resize-pane -Z -t amr:0.3` 還原四格。
- 不在：照下面第 5 節的「重建 tmux」做。

## 5. 在別台電腦繼續（或 HP1 重開機後）

```bash
# Windows 端
cd ~/workspace && git clone -b study https://github.com/chenghyang2001/amr_forklift.git
# WSL 端
sudo apt install ros-jazzy-py-trees ros-jazzy-rmw-cyclonedds-cpp
mkdir -p ~/amr_ws/src && cd ~/amr_ws/src && git clone -b study https://github.com/chenghyang2001/amr_forklift.git
cd amr_forklift && S=study/jazzy
cp $S/models/nebula_urdf/*.xacro models/nebula_urdf/ && cp $S/worlds/*.world worlds/ \
 && cp $S/launch/*.py launch/ && cp $S/config/*.yaml config/ && git apply $S/patches/estop-logger-fix.patch
cd ~/amr_ws && source /opt/ros/jazzy/setup.bash && colcon build --packages-select amr_forklift --symlink-install
```

重建 tmux（四格：①左上 模擬器 Gazebo＝0.0、③左下 觀察 topic＝0.1、②右上 導航 SLAM+Nav2＝0.2、④右下 指令＝0.3）：

```bash
printf '%s\n' "source /opt/ros/jazzy/setup.bash" "source ~/amr_ws/install/setup.bash" \
  "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" "cd ~/amr_ws" > ~/amr_ws/drill_env.sh
tmux new-session -d -s amr -x 180 -y 60 -n 演練
tmux set -t amr -g mouse on; tmux set -t amr -g pane-border-status top; tmux set -t amr -g pane-border-format " #{pane_title} "
tmux split-window -t amr:0 -h; tmux split-window -t amr:0.0 -v; tmux split-window -t amr:0.2 -v
tmux select-pane -t amr:0.0 -T "① 模擬器 Gazebo"; tmux select-pane -t amr:0.1 -T "③ 觀察 topic"
tmux select-pane -t amr:0.2 -T "② 導航 SLAM+Nav2"; tmux select-pane -t amr:0.3 -T "④ 指令"
for p in 0 1 2 3; do tmux send-keys -t amr:0.$p "source ~/amr_ws/drill_env.sh" Enter; done
```

演練形式照 skill `pi5-live-drill` 的「電腦 WSL 版」：每步先 TTS 說明（edge-tts `zh-TW-HsiaoChenNeural`，`~/.claude/skills/tts/scripts/tts_play.py`）→ 念完才在格子下指令 → 截圖自己看 → 念結果 → 停下等「繼續」。語音稿與 mp3 存 `study/drill/<日期>-amr-sim/`，`tts_log.tsv` 記播放時間。

別台電腦要先重查螢幕配置（主螢幕右邊那台是哪個 DISPLAY、座標多少），不能照抄 HP1 的數字。

---

## 6. 繼續用的提示詞（貼到新的 Claude Code session）

```text
請讀 ~/workspace/amr_forklift/study/HANDOFF.md（若沒有，先 git clone -b study https://github.com/chenghyang2001/amr_forklift.git 到 ~/workspace/amr_forklift），
接續 amr_forklift 的現場逐步演練。用 skill pi5-live-drill 的「電腦 WSL 版」形式：
先檢查環境（WSL Ubuntu-24.04、ROS 2 Jazzy、amr_ws 已 build、CycloneDDS），
把 tmux session amr 四格放到「螢幕 3（主螢幕右邊那台）」左半，螢幕 1 不要放任何東西，
開始錄影後，從計畫的第 1 步「認識工作區」開始，每步先語音說明再下指令，做完停下等我說「繼續」。
```

---

## 7. 相關檔案總表

| 檔案 | 用途 |
| --- | --- |
| `study/README.md` | study 資料夾索引 |
| `study/01-新手完整導讀.md` | 導讀（NotebookLM 的來源） |
| `study/02-逐步實作講解.md` | 15 步實作紀錄（含實測輸出） |
| `study/jazzy/` | Gazebo Harmonic 移植檔＋patch |
| `study/run-logs/` | 地圖、截圖、log |
| `study/drill/20261106-amr-sim/` | 現場演練：plan、語音稿、mp3、tts_log、截圖 |
| `study/kindle-amr-ros2-top5.md` | Kindle 書單前 5 名 |
| `study/HANDOFF.md` | 本文件 |
