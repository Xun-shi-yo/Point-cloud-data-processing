import sys
import os
import numpy as np
import open3d as o3d

def background_subtraction(background_cloud, current_cloud, distance_threshold=0.1):
    """
    通过帧间差分法移除背景点云。
    """
    background_points = np.asarray(background_cloud.points)
    current_points = np.asarray(current_cloud.points)

    background_pcd_tree = o3d.geometry.KDTreeFlann(background_cloud)

    foreground_indices = []
    for i, point in enumerate(current_points):
        [_, idx, dist_squared] = background_pcd_tree.search_knn_vector_3d(point, 1)
        if np.sqrt(dist_squared[0]) > distance_threshold:
            foreground_indices.append(i)

    foreground_points = current_points[foreground_indices, :]
    foreground_cloud = o3d.geometry.PointCloud()
    foreground_cloud.points = o3d.utility.Vector3dVector(foreground_points)

    if current_cloud.has_colors():
        foreground_colors = np.asarray(current_cloud.colors)[foreground_indices, :]
        foreground_cloud.colors = o3d.utility.Vector3dVector(foreground_colors)

    return foreground_cloud


def remove_background_from_ply(background_ply_path, current_ply_path, output_ply_path, distance_threshold=0.1):
    """
    从PLY文件中读取背景点云和当前点云，移除背景，保存结果。
    """
    # 读取点云
    bg_cloud = o3d.io.read_point_cloud(background_ply_path)

    fg_cloud = o3d.io.read_point_cloud(current_ply_path)

    # 执行背景移除
    human_cloud = background_subtraction(bg_cloud, fg_cloud, distance_threshold)

    # 保存结果
    print(f"保存前景点云到: {output_ply_path}")
    o3d.io.write_point_cloud(output_ply_path, human_cloud)


if __name__ == '__main__':
    # 请根据你的实际文件路径修改下面三行
    for i in range(1,2):
        try:
            for j in range(0,230):
                try:
                    background_file = r"ne_PLY\S_Null\out_20.ply"      # 空场景背景帧
                    current_file = rf"ne_PLY\Squat\out_{j}.ply"   # 有人的帧\
                    if not os.path.exists(current_file):
                        continue
                    output_file = rf"Only_peo\Squat\clear_{j}.ply"  # 输出前景点云
                    remove_background_from_ply(background_file, current_file, output_file, distance_threshold=0.11)
                except:
                    break
        except:
            sys.exit()