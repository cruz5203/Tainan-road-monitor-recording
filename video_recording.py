import cv2
import urllib.request
import time
import csv
import json, ssl, urllib.request

# 設置計時器時間
timer_duration = 30

# 臺南市路況攝影機(CCTV)位置資料url
url = "https://soa.tainan.gov.tw/Api/Service/Get/4cabeb5d-f234-4cdc-a724-0f5fac90b1de"

# 儲存路徑
save_path = "road_video/"

# 影片起始編號
video_number = 91

context = ssl._create_unverified_context()

with urllib.request.urlopen(url, context=context) as jsondata:
    # 將JSON進行UTF-8的BOM解碼，並把解碼後的資料載入JSON陣列中
    data = json.loads(jsondata.read().decode("utf-8-sig"))

    # 逐行讀取數據
    for video_url in data["data"][91:]:
        # 創建VideoCapture捕捉視訊串流
        cap = cv2.VideoCapture(video_url["影像連結"])
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # 檢查是否成功打开串流
        if not cap.isOpened():
            print("無法打开串流")
            print(
                video_url["位置名稱"],
                "\t",
                video_url["坐標經度"],
                "\t",
                video_url["坐標緯度"],
                "\t",
                video_url["影像連結"],
            )
        else:
            # 定義影片保存器
            fourcc = cv2.VideoWriter_fourcc(*"XVID")

            video_name = save_path + "road_video_" + str(video_number) + ".avi"
            out = cv2.VideoWriter(video_name, fourcc, 20.0, (width, height))

            # 獲取當前時間
            start_time = time.time()

            # 計算結束時間
            end_time = start_time + timer_duration

            # 讀取道路監視器幀並保存
            while time.time() < end_time:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)

                # 在窗口中顯示道路監視器畫面
                cv2.imshow("Real-Time Video", frame)

                # 按'q'键退出
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            # 釋放資源
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            video_number += 1
