#!/usr/bin/env python
# -*- coding: utf-8 -*-
#上記2行は必須構文のため、コメント文だと思って削除しないこと
#Python2.7用プログラム

#ROS関係ライブラリ
import rospy #ROSをpythonで使用するのに必要
from service_sample.srv import service_file # サービスファイルの読み込み（from パッケージ名.srv import 拡張子なしサービスファイル名）
#その他のライブラリ
import sys #プログラム終了に使用



class Client(): #クライアントのクラス
    def __init__(self):
        self.service_message = service_file() #サービスファイルのインスタンス生成
        self.count = 0 #カウントの宣言
        self.rate = rospy.Rate(1) # 1秒間に1回（1Hz)



    def make_msgs(self): #メッセージの作成
        self.service_message.service_request = "リクエストに成功:{}".format(self.count) #リクエスト変数に代入



    def request(self): #サービスのリクエスト
        while not rospy.is_shutdown(): #エラー発生や強制終了がなければずっと繰り返す
            rospy.wait_for_service('service_name') #サービスが使えるようになるまで待機

            try: #サーバとの接続ができた場合
                self.client = rospy.ServiceProxy('service_name', service_file) #クライアントのインスタンス生成
                self.make_msgs() #メッセージの作成
                response = self.client(self.service_message.service_request) #ここでサーバーとデータのやり取りをする。サーバーからの返り値（srvファイル内「---」の下側）をresponseに代入
                rospy.loginfo("{}".format(response.service_response)) #ログの表示
                self.count += 1 #カウントを1増やす
                self.rate.sleep() #待機
    
            except rospy.ServiceException: #サーバとの接続ができなかった場合
                rospy.loginfo("リクエストに失敗") #ログの表示

            except KeyboardInterrupt: #Ctrl+Cが押された場合
                sys.exit() #プログラムの終了



def main(): #メイン関数
    rospy.init_node('client_sample', anonymous=True) #ノードの初期化と名前の設定
    cl = Client() #クラスのインスタンス作成（クラス内の関数や変数を使えるようにする）
    cl.request() #サービスのリクエスト
    rospy.spin() #終了防止



if __name__ == "__main__": #Pythonファイル名（__name__）が実行ファイル名（__main__）である場合（このPythonファイルをモジュールとして使用せず、実行ファイルとして扱う場合）
    try: #エラーが発生しなかった場合
        main() #メイン関数の実行
    except rospy.ROSInterruptException: #エラーが発生した場合
        pass #処理の実行をパスする
