import serial
import time

class Z_axis_control:

    """
    send:
            send_data 
                -send_data[0]: 'I'→Initialize_mode 'T'→Target_mode
                -send_data[1]: アーム移動位置の10の位
                -send_data[2]: アーム移動位置の1の位
                -send_data[3]: アーム移動位置の1/10の位
                -send_data[4]: 入力終了判定の','
            
            (example1) send_data = 'T105,' 目標位置を10.5cm
            (example1) send_data = 'T200,' 目標位置を20.0cm

    receive:
            receive_data
                -finish flag

    """

    def __init__(self):
        self.ser = serial.Serial('COM13', 115200)


    def main(self):

        while True:
            
            send_data = input()

            # 40.0cmより上にはいかないようにする。
            num = int(send_data[1])*10+int(send_data[2])*1+int(send_data[3])*0.1
            if num > 40.0:
                send_data = send_data[0] + '400'

            # もし語尾に','がなければ追加する 忘れ防止のため
            if send_data[-1] != ',':
                send_data = send_data + ','

            self.ser.write(send_data.encode(encoding='utf-8'))
            time.sleep(1) #1秒待ち
            receive_data = Z_axis_controll.serial_data(self)
            print(receive_data)

        ser.close()

    def serial_data(self):
        line = self.ser.readline()
        line_disp = line.strip().decode('UTF-8')
        return line_disp
 
a = Z_axis_control()
a.main()
