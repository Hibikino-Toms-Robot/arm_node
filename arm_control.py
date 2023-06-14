import rclpy  # ROS2のPythonモジュールをインポート
from rclpy.node import Node 
from std_msgs.msg import Float32MultiArray

from x_axis_control_misumi import X_Axis_Control
from y_axis_control_misumi import Y_Axis_Control
from z_axis_control import Z_Axis_Control


class Arm_Controler(Node):  
    def __init__(self):
        super().__init__('arm_node') 
        self.x_control=X_Axis_Control
        self.y_control=Y_Axis_Control()
        self.z_control = Z_Axis_Control()
        self.create_subscription(Float32MultiArray, "target_pose", self.target_pose_callback)

    def target_pose_callback(self,target_pose):
        for pos_data in target_pose.data  :
            self.arm_control(pos_data)

    def arm_control(self,pos_data):
        self.x_control.move_target(pos_data[0]*100)
        self.y_control.move_target(pos_data[1]*100)
        #とりあえずx,y軸だけ
        #self.z_control.move_target(pos_data[2])

if __name__ == '__main__':
    rclpy.init() 
    node=Arm_Controler() 
    try :
        rclpy.spin(node) 

    except KeyboardInterrupt :
        print("Ctrl+Cが入力されました")  
        print("プログラム終了")  
    rclpy.shutdown() 