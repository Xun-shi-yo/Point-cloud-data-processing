import os
import sys
import open3d as o3d
import time
import os

sign = 1
for j in range(1,2):
    try:
        for i in range(1,230):
            try:
                in_path = rf"F:\E1R_driver\ray_radar_data\Cloud_data\Precise_data\Squat\prec_{i}.ply"
                if not os.path.exists(in_path):
                    print(f"文件不存在: {in_path}")
                    continue
                pcd = o3d.io.read_point_cloud(in_path)

                output_path = rf"F:\E1R_driver\ray_radar_data\Cloud_data\Precise_data\Summary\pointclouds\Squat_{sign}.ply"

                if pcd.is_empty():  # 可选：检查点云是否为空
                    print(f"Warning: empty cloud")
                    continue
                o3d.io.write_point_cloud(output_path, pcd)
                print(f"Saved to: {output_path}\n")
                sign = sign + 1
                time.sleep(0.1)
            except Exception as e:
                print(f"Error processing {i}: {e}")
                continue
    except:
        continue