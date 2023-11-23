import numpy as np

# 順運動学
def get_joint_pose(L1, L2, theta1, theta2):
    X1 = L1*np.cos(theta1)
    Y1 = L1*np.sin(theta1)
    X2 = X1 + L2*np.cos(theta1+theta2)
    Y2 = Y1 + L2*np.sin(theta1+theta2)

    return np.array([X1, Y1]), np.array([X2, Y2])

# ヤコビ行列の取得
def get_Jacobian_matrix(L1, L2, theta1, theta2):
    J = np.matrix([[-L1*np.sin(theta1)-L2*np.sin(theta1+theta2), -L2*np.sin(theta1+theta2)], 
                    [L1*np.cos(theta1)+L2*np.cos(theta1+theta2), L2*np.cos(theta1+theta2)] ])
    
    return J

# 逆運動学
def get_joint_angle(X, Y, L1, L2):
    L3 = np.sqrt((X*X) + (Y*Y))
    theta2 = np.pi - np.acos(((L1*L1) + (L2*L2) - (L3*L3)) / (2*L1*L2))
    theta1 = np.arctan2(Y, X) - np.arccos(((L1*L1) + (L3*L3) - (L2*L2)) / (2*L1*L3))

    return theta1, theta2