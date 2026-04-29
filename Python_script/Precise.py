import sys

import open3d as o3d
import numpy as np
import os
from sklearn.cluster import DBSCAN

def get_point_cloud_from_points(points):
    """从 NumPy 数组创建 Open3D 点云对象。"""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    return pcd

def statistical_outlier_removal(pcd, nb_neighbors=20, std_ratio=2.0):#考虑中心点周围点的个数，标准差
                                                            #阈值：到中心点的平均距离 + std_ratio*标准差
    """
    步骤一：使用统计滤波去除离群噪点。
    Args:
        pcd (PointCloud): 输入点云。
        nb_neighbors (int): 用于计算平均距离的邻居点数。
        std_ratio (float): 标准差乘数，值越小，过滤越激进。
    Returns:
        PointCloud: 滤波后的点云。
    """
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    inlier_cloud = pcd.select_by_index(ind)
    return inlier_cloud

def dbscan_cluster(pcd, eps=0.08, min_samples=10):  #eps：球状范围半径 ,min_sample核心点‘周围’最小的点数
    """
    步骤二：使用 DBSCAN 进行聚类，自动识别并去除噪点。
    Args:
        pcd (PointCloud): 输入点云。
        eps (float): 邻域半径。
        min_samples (int): 核心点的最小邻居数。
    Returns:
        labels (np.array): 每个点的簇标签，-1 代表噪点。
    """
    points = np.asarray(pcd.points)
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    labels = clustering.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    return labels

def extract_human_cluster(pcd, labels, human_cluster_label):
    """
    步骤三：根据 DBSCAN 的标签提取人体点云。
    Args:
        pcd (PointCloud): 标注后的点云。
        labels (np.array): DBSCAN 输出的标签。
        human_cluster_label (int): 代表人体的簇的标签。
    Returns:
        PointCloud: 提取出的人体点云。
    """
    human_indices = np.where(labels == human_cluster_label)[0]
    human_pcd = pcd.select_by_index(human_indices)
    return human_pcd

def process_foreground_pipeline(foreground_pcd, 
                                 sor_nb_neighbors=20, sor_std_ratio=2.0,
                                 db_eps=0.08, db_min_samples=10,
                                 vis=False):
    """
    完整的前景点云处理管线：滤波 -> 聚类 -> 提取人体。
    """
    # # 1. 统计滤波
    filtered_pcd = statistical_outlier_removal(foreground_pcd, sor_nb_neighbors, sor_std_ratio)
    # filtered_pcd = foreground_pcd
    # 2. DBSCAN 聚类
    labels = dbscan_cluster(filtered_pcd, eps=db_eps, min_samples=db_min_samples)

    # 3. 提取人体 (假设最大簇为人体)
    human_pcd = foreground_pcd # 默认值
    unique_labels = set(labels)
    if -1 in unique_labels:
        unique_labels.remove(-1)

    if not unique_labels:
        return filtered_pcd, labels, None

    # 简单的启发式方法：选择点数最多的簇
    largest_cluster_label = max(unique_labels, key=lambda x: np.sum(labels == x))
    human_pcd = extract_human_cluster(filtered_pcd, labels, largest_cluster_label)

    if vis:
        # 可视化：为点云上色以区分人（红）和噪点（灰）
        colors = np.full((len(labels), 3), [0.5, 0.5, 0.5])  # 先设置所有点为灰色
        colors[labels == largest_cluster_label] = [1, 0, 0]  # 再设置人体为红色（最大的点云簇）
        filtered_pcd.colors = o3d.utility.Vector3dVector(colors)
        o3d.visualization.draw_geometries([filtered_pcd])
        # o3d.visualization.draw_geometries([human_pcd])

    return filtered_pcd, labels, human_pcd

# --- 如何使用 ---
if __name__ == "__main__":
    for i in range(1,7):
        try:
            for j in range(1,230):
                try:
                    # 加载你的前景点云 (你之前的背景移除结果)
                    foreground_pcd = o3d.io.read_point_cloud(
                        rf"F:\E1R_driver\ray_radar_data\Cloud_data\Only_peo\Lie\sec00{i}\clear_{j}.ply")

                    # 执行处理管线
                    filtered_cloud, labels, human_cloud = process_foreground_pipeline(
                        foreground_pcd,
                        sor_nb_neighbors=25, sor_std_ratio=1.0,
                        db_eps=0.29, db_min_samples=10,
                        vis=False  # 开启可视化以查看结果
                    )
                    #保存最终的人体点云
                    if human_cloud is not None:
                        output_path = rf"F:\E1R_driver\ray_radar_data\Cloud_data\Precise_data\Lie\sec00{i}\prec_{j}.ply"
                        o3d.io.write_point_cloud(output_path, human_cloud)
                        print(f"最终的人体点云已保存至: {output_path}")
                    else:
                        print("未能成功提取人体点云，请检查参数。")
                except KeyboardInterrupt:
                    print("\n检测到 Ctrl+C，程序安全退出。")
                except:
                    continue
        except KeyboardInterrupt:
            print("\n检测到 Ctrl+C，程序安全退出。")
        except:
            sys.exit()


    # sor_nb_neighbors=25, sor_std_ratio=1.0,
    # db_eps=0.2, db_min_samples=20,
    # For Stand;

    # sor_nb_neighbors = 25, sor_std_ratio = 1.0,
    # db_eps = 0.30, db_min_samples = 10,
    # For Lie;

    # sor_nb_neighbors = 25, sor_std_ratio = 1.0,
    # db_eps = 0.20, db_min_samples = 21,
    # For Squat

    # sor_nb_neighbors = 25, sor_std_ratio = 1.0,
    # db_eps = 0.20, db_min_samples = 21,
    # For Sit