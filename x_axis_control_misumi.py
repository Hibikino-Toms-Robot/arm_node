import serial
import time

# x_axis_armは移動位置＝20-動かしたい位置だけ動かせばいい、アームを初期位置から1cm動かしたいときは、20-1=190.00[mm]
# https://jp.misumi-ec.com/maker/misumi/mech/special/actuator_portal/rs/download/pdf/C1C21C22_JP_V201.pdf
# p230より

class X_Axis_Control:
    """
    input:
        Target Location (10*(-3)mm)

    output:
        finish flag
    """
    def __init__(self):
        self.ser = serial.Serial("COM9", baudrate=38400, bytesize=8, parity=serial.PARITY_ODD, stopbits=1, xonxoff=False)
        self.move_init()
       
    def move_init(self):
        self.servo_on()
        self.org_arm()
        self.move_target(00000)

    

    def servo_on(self):
        self.ser.write(b'@SRVO1,') # サーボON指令
        while True:
            self.ser.write(b'@?OPT1,') # オプション情報（状態）の読み出し
            receive = self.ser.readline()
            if receive == b'OK.1\r\n':
                time.sleep(0.1) # 0.1秒停止
                break

    def servo_off(self):
        self.ser.write(b'@SRVO0,') # サーボOFF指令
        time.sleep(0.1)

    def org_arm(self):
        self.ser.write(b'@ORG,') # 限定回帰指令
        while True:
            self.ser.write(b'@?OPT1,') # オプション情報（状態）の読み出し
            receive = self.ser.readline()
            # 2584, 2508, 2568 が終了応答
            if receive == b'OPT1.1=2584\r\n' or receive == b'OPT1.1=2508\r\n' or receive == b'OPT1.1=2568\r\n':
                time.sleep(0.1) # 0.1秒停止
                break


    def move_target(self, target):
        target = 20000 - target
        self.ser.write(('@S1=100,').encode(encoding='utf-8')) # Speedの設定
        time.sleep(0.1) # 0.1秒停止
        self.ser.write(('@START1#P'+str(target)+',').encode(encoding='utf-8')) #目標位置へ移動指令
        while True:
            self.ser.write(b'@?OPT1,') # オプション情報（状態）の読み出し
            receive = self.ser.readline()
            # 2570, 2346が終了応答
            if receive == b'OPT1.1=2570\r\n' or receive == b'OPT1.1=2346\r\n':
                time.sleep(0.1) # 0.1秒停止
                break
        # time.sleep(1)
        return 0
    


def main():
    # '''デバック'''
    # x_control = X_Axis_Control()
    # # 目標位置へ移動
    # tag1 = x_control.move_target(20000)
    # time.sleep(2)
    # tag2 = x_control.move_target(10000)
    # time.sleep(2)
    # tag3 = x_control.move_target(00000)
    # time.sleep(2)
    # tag4 = x_control.move_target(20000)
    # time.sleep(2)
    # tag5 = x_control.move_target(00000)
    # time.sleep(2)
    pass
if __name__ == '__main__':
    main()
