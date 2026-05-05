import open3d as o3d
import sys


def view_ply(ply_path):
    """读取并交互查看 PLY 点云文件"""
    # 读取点云
    pcd = o3d.io.read_point_cloud(ply_path)

    # 打印基本信息
    print(f"点云点数: {len(pcd.points)}")
    print(f"点云中心: {pcd.get_center()}")

    # 如果没有颜色，可以给点云上一种颜色便于观察
    if not pcd.has_colors():
        pcd.paint_uniform_color([0.5, 0.5, 0.5])  # 灰色

    # 打开交互窗口（非阻塞方式）
    o3d.visualization.draw_geometries(
        [pcd],
        window_name=f"PLY Viewer - {ply_path}",
        width=1024,
        height=768,
        point_show_normal=False  # 如果有法向量可以设为True
    )


if __name__ == "__main__":
    # 你可以在这里修改要查看的文件路径
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # 默认路径，改成你实际的 PLY 文件
        file_path = r'F:\E1R_driver\ray_radar_data\Cloud_data\Summary\pointclouds\Lie_700.ply'

    view_ply(file_path)