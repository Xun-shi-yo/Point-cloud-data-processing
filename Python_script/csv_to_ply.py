import pandas as pd
import open3d as o3d
import sys
import numpy as np
import matplotlib.pyplot as plt


#for i in range(1,7):
try:
# 读取 CSV 文件
    for j in range(0,300):
        try:
            csv_file = rf'ne_CSV\Sit_Null\frame_{j}.csv'
            df = pd.read_csv(csv_file,header = None)


            # 假设 CSV 文件包含列 ['x', 'y', 'z']
            points = df[[0, 1, 2]].values

            # 取出第 4 列（索引为 3）的值，并转为浮点型
            intensity = df[3].values.astype(np.float32)
            if intensity.max() > intensity.min():
                intensity_norm = (intensity - intensity.min()) / (intensity.max() - intensity.min())
            else:
                # 所有值都相同（比如全是 0），则全给 0（黑色）
                intensity_norm = np.zeros_like(intensity)

            cmap = plt.get_cmap('jet')           # 蓝→青→绿→黄→红
            colors = cmap(intensity_norm)[:, :3]            # 每个值映射为 RGB，去掉 Alpha 通道



            # 创建点云对象
            point_cloud = o3d.geometry.PointCloud()
            point_cloud.points = o3d.utility.Vector3dVector(points)
            point_cloud.colors = o3d.utility.Vector3dVector(colors.astype(np.float64))

            # 保存为 PLY 格式
            ply_file = rf'ne_PLY\Sit_Null\out_{j}.ply'
            o3d.io.write_point_cloud(ply_file, point_cloud)
            print(f"PLY file saved to: {ply_file}")
        except:
            break
except:
    sys.exit()