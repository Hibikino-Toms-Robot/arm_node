import rclpy  # ROS2のPythonモジュールをインポート
from rclpy.node import Node 
from std_msgs.msg import Float32MultiArray
from command_service.srv import ArmComand

from x_axis_control_misumi import X_Axis_Control
from y_axis_control_misumi import Y_Axis_Control
from z_axis_control import Z_Axis_Control

class Arm_Controler(Node):  
    def __init__(self):
        super().__init__('arm_node') 
        self.x_control=X_Axis_Control
        self.y_control=Y_Axis_Control()
        self.z_control = Z_Axis_Control()
        self.srv = self.create_service(ArmComand, "target_pose", self.target_pose_callback)
 
    def target_pose_callback(self,request, response):
        for pos_data in request.target  :
            self.arm_control(pos_data)
        self.get_logger().info('動作完了')  
        return response.task_comp
    
    def arm_control(self,pos_data):
        self.x_control.move_target(pos_data[0]*100)
        self.y_control.move_target(pos_data[1]*100)
        self.z_control.move_target(pos_data[2])
        return True
    
if __name__ == '__main__':
    rclpy.init() 
    node=Arm_Controler() 
    try :
        rclpy.spin(node) 

    except KeyboardInterrupt :
        print("Ctrl+Cが入力されました")  
        print("プログラム終了")  
    rclpy.shutdown() 
