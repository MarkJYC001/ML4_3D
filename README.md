# ML4_3D

****哦哦哦，just in case, 如果有任何修改，大家记得create branch!!!****
<img width="657" alt="WeChatfbeb5ea79de69e08fd26b4cf3c4a3282" src="https://github.com/MarkJYC001/ML4_3D/assets/90122592/3a9a0cfe-d1ae-4402-a29b-2fcc88f8658c">

## This is a pipeline that we currently want to achieve, and we welcome to make it better.😄

Engineing Prospective:
 * Expected Input: 2D 照片 
 * Expected Output: 3D 场景及物理推理
 1. projection投射：
   - 第一步：3D点云
   - OR 第一步：质点 质心等物理信息（以后搞成点云）； 
   - 第二步：输入"物理"系统
        - Requires:
 		- a. 3D 数据集 + 3D重建
 		- b. 物理系统（静）
 2. generation推演:
   - 第三步：合适的输出方式可视化
   - advanced:基于PINN推演/反推演（熵减）
	- Requires:
 		- a. 物理系统内物体追踪
	      	- b. 物理系统（动）
 		- c. 呈现方式:可视/仿真（色彩）


最终：
1. 物理实验
2. 3D film


Research prospective:
1. 视觉角度的生成: 3D reconstruction + NERF -- > 没有碰撞，近似饱和:https://jonbarron.info/zipnerf/
2. 3D 重建：几何信息-->mesh :picture  > pose > feature point > sparse 3D point > more accurate point > ponit cloud > SDF(structure for motion)
   -> Algorithm: Mesh;
   -> Not accurate + bias + time comsuming
3. Not picture based: RGB + laser
4. Robotic : 理解碰撞 + 结束 + 决策 RL

5. Therefore: --> many picutures --> time cheap + 

   
Candidate Baseline:
Projection:arXiv:2204.10776v2 [cs.CV] 27 Jan 2023
Generation:https://www.bilibili.com/video/BV1Yr421775V/?spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=c2f7388c7b279132a2d3049f97303966




Generation:欢迎补充！

See wiki for details, have fun🥳.
 
