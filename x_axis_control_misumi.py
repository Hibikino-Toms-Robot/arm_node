import serial
import time

# x_axis_armは移動位置＝20-動かしたい位置だけ動かせばいい、1cm動かしたいときは、20-1=19000[cm]
# https://jp.misumi-ec.com/maker/misumi/mech/special/actuator_portal/rs/download/pdf/C1C21C22_JP_V201.pdf
# p230より

class X_Axis_Control:
    """
    input:
        Flag: 'I'→Initialize_mode 'T'→Target_mode
        Target: x

    (example1) Flag = 'I' 初期化モード
    (example2) Flag = 'T' Target = 20000 ターゲットモード　目標位置を20.000[cm]に設定（Z軸と合わせるために少数第一位で四捨五入してもいいかも？）

    output:
        finish_flag → 0

    """
    def __init__(self, Flag, Target):
        self.ser = serial.Serial("COM9", baudrate=38400, bytesize=8, parity=serial.PARITY_ODD, stopbits=1, xonxoff=False)
        self.Flag = Flag
        # x軸は最も伸びきった状態（20000mm）のときが初期位置である
        if self.Flag == 'T':
            self.Target = 20000 - Target #20000はアームの可動域


    def Servo_On(self):
        self.ser.write(b'@SRVO1,') # サーボON指令
        On_flag = True
        # 終了コマンドがでるまでwhileで回す
        while On_flag:
            self.ser.write(b'@?OPT1,') # オプション情報（状態）の読み出し
            receive = self.ser.readline()
            if receive == b'OK.1\r\n': # 終了時コマンド
                time.sleep(0.1)  # 0.1秒停止
                break

    def Servo_Off(self):
        self.ser.write(b'@SRVO0,') # サーボON指令
        time.sleep(0.1) # 0.1秒停止

    def Org_Arm(self):
        self.ser.write(b'@ORG,')
        org_flag = True
        # 終了コマンドがでるまでwhileで回す
        while org_flag:
            self.ser.write(b'@?OPT1,')
            receive = self.ser.readline()
            # 終了コマンドは2584, 2508, 2568である。
            if receive == b'OPT1.1=2584\r\n' or receive == b'OPT1.1=2508\r\n' or receive == b'OPT1.1=2568\r\n':
                time.sleep(0.1) # 0.1秒停止
                break

    def Target_Arm(self, Speed, Target_pos):
        self.ser.write(('@S1='+str(Speed)+',').encode(encoding='utf-8')) # Speedの設定
        time.sleep(0.1)
        self.ser.write(('@START1#P'+str(Target_pos)+',').encode(encoding='utf-8')) #初期位置へ移動指令
        target_flag = True
        while target_flag:
            self.ser.write(b'@?OPT1,')
            receive = self.ser.readline()
            # 終了コマンドは2570, 2346である。
            if receive == b'OPT1.1=2570\r\n' or receive == b'OPT1.1=2346\r\n':
                time.sleep(0.1) # 0.1秒停止
                break
    
    def main(self):
        # 初期化モード
        if self.Flag == 'I':
            self.Servo_On()
            self.Org_Arm()
            self.Target_Arm(100, 20000) #初期化後は中心位置
        elif self.Flag == 'T':
            self.Target_Arm(100, self.Target)

        self.ser.close()

        return 0
    
# デバック
Flag = 'I'
X_target = None
ini = X_Axis_Control(Flag, X_target)
fin = ini.main()

Flag = 'T'
X_target = 10000
tar = X_Axis_Control(Flag, X_target)
fin = tar.main()
print(fin)
