# amr_forklift 模擬逐步演練（2026-11-06，WSL Ubuntu 24.04＋ROS 2 Jazzy）

螢幕 3：左半 Windows Terminal（WSL tmux session `amr`，四格）；右半上 Gazebo、下 RViz。

| 格子 | tmux | 用途 |
| --- | --- | --- |
| ① 模擬器 Gazebo（左上） | amr:0.0 | 長駐：gz_sim.launch.py |
| ② 導航 SLAM+Nav2（右上） | amr:0.2 | 長駐：slam_nav_gz.launch.py |
| ③ 觀察 topic（左下） | amr:0.1 | topic hz／echo、行為樹節點 |
| ④ 指令（右下） | amr:0.3 | 一次性指令 |

| 步驟 | 格子 | 指令 | 預期效果 |
| --- | --- | --- | --- |
| 1 | ④ | `ls src/amr_forklift` ＋ `git -C src/amr_forklift status --short` | 看到套件結構與 6 個 Jazzy 新檔、1 個修正 |
| 2 | ③④ | ③ `ros2 run demo_nodes_cpp talker`；④ `ros2 topic echo /chatter --once` | CycloneDDS 下收得到 Hello World |
| 3 | ① | `ros2 launch amr_forklift gz_sim.launch.py` | Gazebo 與 RViz 開啟，放到右半 |
| 4 | ③④ | ③ `ros2 topic hz /scan`；④ `ros2 topic list` | 約 9 Hz；列出 /scan /odom /cmd_vel… |
| 5 | ④ | 印正前方 ±20° 的 /scan 與 /scan_filtered | 柱子 0.41 m → inf |
| 6 | ② | `ros2 launch amr_forklift slam_nav_gz.launch.py` | Managed nodes are active；RViz 出現地圖 |
| 7 | ④ | `ros2 action send_goal /navigate_to_pose ... x:-3.0 y:1.0` | 規劃路線、機器人移動、SUCCEEDED |
| 8 | ②③④ | ② Ctrl+C；③ `ros2 run amr_forklift amr_behavior_tree`；④ 發 safety_hazard／battery_voltage | 巡邏 → 緊急停止 → 充電 |
| 9 | — | 總結、關閉、做影片 | — |
