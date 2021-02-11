#!/usr/bin/env python
# -*- coding: utf-8 -*-
#上記2行は必須構文のため、コメント文だと思って削除しないこと
#Python2.7用プログラム

#ROS関係ライブラリ
import rospy #ROSをpythonで使用するのに必要
from service_sample.srv import service_file # サービスファイルの読み込み（from パッケージ名.srv import 拡張子なしサービスファイル名）



class Server(): #サーバーのクラス
    def __init__(self):
        self.service_message = service_file() #サービスファイルのインスタンス生成
        self.rate = rospy.Rate(1) # 1秒間に1回（1Hz)



    def make_msg(self, request_message): #メッセージの作成
        self.service_message.service_response = "リスポンスに成功".format(request_message) #リスポンス変数に代入



    def call_back(self, request): #サービスのリクエストがあった場合に呼び出されるコールバック関数
        rospy.loginfo("{}".format(request.service_request)) #ログの表示
        self.make_msg(request.service_request) #メッセージの作成
        self.rate.sleep() #待機
        return self.service_message.service_response #srvファイルで定義した返り値をsrvに渡す。rospy.Serviceによって呼び出された関数（callback関数）内でreturnすること



    def response(self): #サービスの応答
        server = rospy.Service('service_name', service_file, self.call_back) #サービスのリクエストがあった場合にコールバック関数を呼び出し、実行。コールバック関数内で返り値をreturnする必要がある



def main(): #メイン関数
    rospy.init_node('server_sample', anonymous=True) #ノードの初期化と名前の設定
    sv = Server() #クラスのインスタンス作成（クラス内の関数や変数を使えるようにする）
    sv.response() #サービスの応答
    rospy.spin() #終了防止



if __name__ == "__main__": #Pythonファイル名（__name__）が実行ファイル名（__main__）である場合（このPythonファイルをモジュールとして使用せず、実行ファイルとして扱う場合）
    try: #エラーが発生しなかった場合
        main() #メイン関数の実行
    except rospy.ROSInterruptException: #エラーが発生した場合
        pass #処理の実行をパスする
