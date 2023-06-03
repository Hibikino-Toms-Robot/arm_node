class calc_arm_control:

        '''
        input:
                絶対座標系におけるトマトの座標 or 初期化後に少しだけ動かす: (X, Y, Z)
                モードフラグ: 'T'→目標値へアームを動かすモード、'I'→初期化モード

        output:
                アーム座標系をアーム制御量: (target_x, target_y, target_z)
                (example) target_z = 'T052'→アームを初期位置から5.2cm動かす

        '''

        def __init__(self, absolute, mode):

                # 既知情報
                # 初期位置におけるアームの先端の位置（絶対座標系）
                self.Xinit = 40.0 
                self.Yinit = 40.0 
                self.Zinit = 40.0
                # アームの制御量の限界
                self.Xlim = 20.0
                self.Ylim = 20.0
                self.Zlim = 40.0

                # 未知情報
                #トマトのX座標（絶対座標系）
                self.X = float(absolute[0])
                self.Y = float(absolute[1])
                self.Z = float(absolute[2])

                self.mode = mode
        
        def make_send_data(self, target, mode):
                flag = True
                while flag:
                        if len(target) < 3:
                                target = '0'+target
                        if len(target) > 2:
                                flag = False

                target = mode + target

                return target

        def main(self):

                # 制御量を計算
                target_X = round(self.X - self.Xinit, 1)
                target_Y = round(self.Y - self.Yinit, 1)
                target_Z = round(self.Z - self.Zinit, 1)

                # 下限 or 上限　突破しないようにする。あえてエラーにする
                if(target_X < 0.0 or target_X > self.Xlim):
                        target_X = 1/0
                if(target_Y < 0.0 or target_Y > self.Ylim):
                        target_Y = 1/0
                if(target_Z < 0.0 or target_Z > self.Zlim):
                        target_Z = 1/0
                
                target_X = str(target_X).replace('.', '')
                target_X = self.make_send_data(target_X, self.mode)

                target_Y = str(target_Y).replace('.', '')
                target_Y = self.make_send_data(target_Y, self.mode)

                target_Z = str(target_Z).replace('.', '')
                target_Z = self.make_send_data(target_Z, self.mode)

                return target_X, target_Y, target_Z

# デバック
# トマトの位置（絶対座標系）
absolute = [60.0, 45.0, 45.15111]
# アームの制御量を決定
a = calc_arm_control(absolute, 'T')
target_X, target_Y, target_Z = a.main()

print(target_X, target_Y, target_Z)