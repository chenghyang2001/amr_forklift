# study／amr_forklift 學習資料夾

這個資料夾不是原作者的內容，是為了學習 [furkankarsli/amr_forklift](https://github.com/furkankarsli/amr_forklift) 另外加的。

| 檔案 | 內容 |
| --- | --- |
| [01-新手完整導讀.md](01-新手完整導讀.md) | 給大一新生的完整導讀：ROS 2 觀念、架構、逐檔精讀、資料流、坑、學習路線、練習題 |
| [02-逐步實作講解.md](02-逐步實作講解.md) | 在 Windows 11＋WSL Ubuntu 24.04＋ROS 2 Jazzy 實際跑起來的 15 個步驟（含實測輸出） |
| `jazzy/` | Gazebo Harmonic 移植檔（複製到套件同名資料夾後 colcon build） |
| `jazzy/patches/estop-logger-fix.patch` | 緊急停止當掉的一字修正 |
| `run-logs/` | 實測紀錄：SLAM 地圖、Gazebo／RViz 截圖、各節點 log、NotebookLM 簡報第一頁 |

## NotebookLM

Notebook：「AMR 自主堆高機 Nebula（amr_forklift）新手導讀」（id `0dd71297-666e-4679-88bb-f59e66a645b9`），
來源＝01 導讀；已產生語音摘要、影片摘要、簡報（15 頁，第一頁為大綱）、心智圖。

<https://notebooklm.google.com/notebook/0dd71297-666e-4679-88bb-f59e66a645b9>

## 快速重跑（WSL）

```bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
source /opt/ros/jazzy/setup.bash && cd ~/amr_ws && source install/setup.bash
ros2 launch amr_forklift gz_sim.launch.py          # 終端機 1
ros2 launch amr_forklift slam_nav_gz.launch.py     # 終端機 2，之後在 RViz 按 Nav2 Goal
```
