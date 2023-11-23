import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from matplotlib.widgets import Slider
from function_lib import *

fig, ax = plt.subplots(figsize=(15, 12))

# 可操作性楕円体の計算
def calculate_Ellipsoid_from_Jacobian(J):
    # 正方行列の計算
    A = J * J.T
    # Aの固有値，固有ベクトルを計算する
    values, vectors = np.linalg.eig(A)

    # 固有値の平方
    lambda1 = np.sqrt(values[0])
    lambda2 = np.sqrt(values[1])
    # 楕円の大きさ
    short_side = lambda1
    long_side = lambda2
    

    # 固有ベクトル
    vector1 = vectors[:,0]
    vector2 = vectors[:,1]

    # 楕円の傾き
    rad = -np.arctan2(vector1[0],vector1[1])
    # rad = np.arctan2(vector2[1], vector2[0])

    return long_side, short_side, rad


def draw_manipulator_operability(L1, L2, theta1, theta2):
    J = get_Jacobian_matrix(L1, L2, theta1, theta2)
    p1, p2 = get_joint_pose(L1, L2, theta1, theta2)
    long_side, short_side, rad = calculate_Ellipsoid_from_Jacobian(J)

    # 楕円の描画
    ellips = pat.Ellipse(xy = (p2[0], p2[1]), width=long_side*0.5, height=short_side*0.5, angle=np.rad2deg(rad), alpha=0.6, color='red')

    # マニピュレータの描画
    # ax.plot([0, x1], [0, y1], 'k', linewidth=10.0, zorder=1)
    # ax.plot([x1, x2], [y1, y2], 'k', linewidth=10.0, zorder=1)
    link0 = pat.Rectangle(xy=(0, 0), angle=np.rad2deg(np.arctan2(p1[1], p1[0])-np.pi/2), width=0.05, height=L1, ec='b')
    link1 = pat.Rectangle(xy=(p1[0], p1[1]), angle=np.rad2deg(np.arctan2(p2[1]-p1[1], p2[0]-p1[0])-np.pi/2), width=0.05, height=L2, ec='b')
    c0 = pat.Circle(xy=(0, 0), radius=0.1, ec='w', fill=True, zorder=2)
    c1 = pat.Circle(xy=(p1[0], p1[1]), radius=0.1, ec='w', fill=True, zorder=2)
    ax.add_patch(c0)
    ax.add_patch(c1)
    ax.add_patch(link0)
    ax.add_patch(link1)
    ax.add_patch(ellips)

    # 図の作成
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal')
    ax.grid()
    plt.xlim([-2,2])
    plt.ylim([-0.5,2])

    # スライダーの設定
    # スライダーの表示位置
    theta1_slider_pos = plt.axes([0.1, 0.01, 0.8, 0.03], facecolor='gold')
    theta2_slider_pos = plt.axes([0.1, 0.04, 0.8, 0.03], facecolor='gold')
    # Sliderオブジェクトのインスタンス作成
    theta1_value = Slider(theta1_slider_pos, 'theta1', -np.pi/2, np.pi/2, valinit=theta1)
    theta2_value = Slider(theta2_slider_pos, 'theta2', -np.pi/2, np.pi/2, valinit=theta2)

    def update(val):
        theta1 = theta1_value.val
        theta2 = theta2_value.val
        J = get_Jacobian_matrix(L1, L2, theta1, theta2)
        p1, p2 = get_joint_pose(L1, L2, theta1, theta2)
        long_side, short_side, rad = calculate_Ellipsoid_from_Jacobian(J)

        ellips.set_angle(np.rad2deg(rad))
        ellips.set_width(long_side*0.5)
        ellips.set_height(short_side*0.5)
        ellips.set_center((p2[0], p2[1]))

        # c1.set_xy((x1, y1))
        c1.set_center((p1[0], p1[1]))

        link0.set_angle(np.rad2deg(np.arctan2(p1[1], p1[0])-np.pi/2))

        link1.set_xy((p1[0], p1[1]))
        link1.set_angle(np.rad2deg(np.arctan2(p2[1]-p1[1], p2[0]-p1[0])-np.pi/2))
        fig.canvas.draw_idle()

    theta1_value.on_changed(update)
    theta2_value.on_changed(update)

    plt.show()


if __name__ == "__main__":
    L1 = 1.0
    L2 = 1.0
    theta1 = np.deg2rad(30)
    theta2 = np.deg2rad(40)

    draw_manipulator_operability(L1, L2, theta1, theta2)

    print("プログラム終了")


