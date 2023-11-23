import math, time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from function_lib import *
from IPython.display import display, clear_output

l1, l2, l3 = 0.4, 0.4, 0.2
goal = np.array([0.3, 0.7])
obs = np.array([0.6, 0.6])
danger_range = 0.2

############## ロボットアームの表示 ################
def draw(p1, q):
    global ax, plt
    th1, th2 = q[0], q[0] + q[1]
    goal_pos  = patches.Circle(xy=(goal[0], goal[1]), radius=0.02, fc='b') #ゴールを指定
    obs_pos   = patches.Circle(xy=(obs[0], obs[1]), radius=0.05, fc='r') #障害点を指定
    obs_range = patches.Circle(xy=(obs[0], obs[1]), radius=danger_range, ec='y', fill=False) 
    #障害点から0.2mの円を指定
    ax.add_patch(goal_pos)
    ax.add_patch(obs_pos)
    ax.add_patch(obs_range)

    joint1 = patches.Circle(xy=( 0,  0), radius=0.03, fc='g') #関節O
    joint2 = patches.Circle(xy=(p1[0], p1[1]), radius=0.03, fc='g') #関節Aを指定

    link1 = patches.Rectangle(xy=(    0,     0), angle=np.rad2deg(th1 - math.pi/2),
                              width=0.005, height=l1, ec='b') #関節O-Aを指定
    link2 = patches.Rectangle(xy=(p1[0], p1[1]), angle=np.rad2deg(th2 - math.pi/2), 
                              width=0.005, height=l2, ec='b') #関節A-Bを指定

    ax.add_patch(joint1)
    ax.add_patch(joint2)
    ax.add_patch(link1)
    ax.add_patch(link2)
    plt.xlim(-0.3, 1.0)
    plt.ylim(-0.3, 1.0)
    ax.set_aspect('equal')
    ax.grid(True)
    fig.tight_layout()
    plt.pause(0.1)
    plt.cla()

############## 逆運動学により間接角を計算 ################
def InverseKinematics(pose, n=0): #n=0または1でどちらの関節位置を使用するか指定する
    x, y, thetar = pose[0], pose[1], 0 # theta is fixed to 0
    a = y - l3*math.sin(thetar)
    b = x - l3*math.cos(thetar)
    L = math.hypot(a,b)
    if L < 1e-10: #
        return None
    gamma = math.atan2(a,b)
    val1 = (l1*l1 + L*L - l2*l2)/(2*l1*L)
    val2 = (l1*l1 + l2*l2 - L*L)/(2*l1*l2)
    if (val1 < -1.0 or val1 > 1.0) or (val2 < -1.0 or val2 > 1.0):
        return None
    alpha = math.acos(val1)
    beta = math.acos(val2)
    theta1 = (gamma + alpha, gamma - alpha)
    theta2 = (beta - math.pi, -beta + math.pi)
    theta3 = (thetar - theta1[0] - theta2[0], thetar - theta1[1] - theta2[1])
    return [theta1[n], theta2[n], theta3[n]]

############## 直線追従 ################
def MoveStraight(q):
    #順運動学により手先座標を取得
    _, p = get_joint_pose(q)
    #現在の手先とゴールとのベクトルを求める
    v = goal - p
    #微小の手先移動ベクトルを求める
    dv = 0.03*v/np.linalg.norm(v) #手先位置の移動量
    while True:
        p += dv #手先位置をdvだけ移動
        #障害物から指定した距離が離れているか確認
        if np.linalg.norm(obs - p) < danger_range: #手先が障害物に近いかをチェック
            break
        #移動した先の手先位置が，指定した距離内になかったら
        q = Routine(p)
        if np.linalg.norm(goal - p) < 0.02: #手先がゴールに近いかをチェック
            return True, q
    return False, q

############## メイン ################
fig = plt.figure()
ax = plt.axes()

def Routine(pose): #引数を手先位置とし，アームの描画および各関節位置を出力
    q = InverseKinematics(pose) #関節角を計算
    p1, p = get_joint_pose(q) #各関節位置および手先位置を計算
    #
    clear_output(wait = True)
    plt.cla()
    draw(p1, q) #アームを描画
    time.sleep(0.001)
    #
    return q

#障害物を回避して移動（回転移動）
def MoveOnCircle(q):
    _, p = get_joint_pose(q)  #初期の手先位置
    ang = math.atan2(p[1] - obs[1], p[0] - obs[0])
    while True:
        ang -= 0.1
        p = np.array([obs[0] + danger_range*math.cos(ang), obs[1] + danger_range*math.sin(ang)])
        q = Routine(p)
        if (np.linalg.norm(goal - p) < np.linalg.norm(goal - obs) and
            math.fabs((goal[1] - obs[1])*(p[0] - obs[0])/(goal[0] - obs[0]) - p[1] + obs[1]) < 0.03): #「障害物より手先位置の方がゴールに近い」かつ「障害物とゴールを結ぶ直線上に手先位置がくる」
            break
    return q

q = np.array([0.2, 0.2])  # 初期関節角
goal_flag, q = MoveStraight(q)
if not goal_flag:
    q = MoveOnCircle(q)
    MoveStraight(q)