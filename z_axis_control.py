import serial
import time

class Z_Axis_Control:

        """
        input:
                send_data 
                    -send_data[0]: 'I'→Initialize_mode 'T'→Target_mode
                    -send_data[1]: アーム移動位置の10の位
                    -send_data[2]: アーム移動位置の1の位
                    -send_data[3]: アーム移動位置の1/10の位
                    -send_data[4]: 前回のアームの位置の10の位
                    -send_data[5]: 前回のアームの位置の1の位
                    -send_data[6]: 前回のアームの位置の1/10の位
                    -send_data[7]: 入力終了判定の','
                
                (example1) send_data = 'T105090,' 目標位置を10.5cm、前回の位置は9.0cm
                (example1) send_data = 'T200010,' 目標位置を20.0cm、前回の位置は1.0cm

        output:
                receive_data
                    -finish flag

        """

        def __init__(self):
            self.ser = serial.Serial('COM13', 115200)

        def move_target(self, target, pre_target):
   
            time.sleep(1) # 1秒停止する。1秒でないとうまく動かなかった
            send_data = target + pre_target
            time.sleep(1)
            print(send_data)

            send_data = self.check_data(send_data)
            self.ser.write(send_data.encode(encoding='utf-8'))
            time.sleep(1)
            receive_data = self.serial_data()
            print(receive_data)
            time.sleep(0.1)

            return 0

        def check_data(self, send_data):
            # 40.0cmより上にはいかないようにする。
            num = int(send_data[1])*10+int(send_data[2])*1+int(send_data[3])*0.1
            if num > 40.0:
                send_data = send_data[0] + '400'

            # もし語尾に','がなければ追加する 忘れ防止のため
            if send_data[-1] != ',':
                send_data = send_data + ','
            return send_data


        def serial_data(self):
            line = self.ser.readline()
            line_disp = line.strip().decode('UTF-8')
            return line_disp
 

'''デバック'''
z_control = Z_Axis_Control()

# initialization
pre = '000'
init_Z = 'I010'
ini = z_control.move_target(init_Z, pre)

# target
pre = init_Z[1:]
target_Z = 'T110'
tar = z_control.move_target(target_Z, pre)

# target
pre = target_Z[1:]
target_Z = 'T200'
tar = z_control.move_target(target_Z, pre)
