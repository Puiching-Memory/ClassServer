# 导入Flask类库
from flask import Flask, request, jsonify

# 创建应用实例
app = Flask(__name__)

# import os
# import time
##import asyncio
# import logging
# import sys
# import threading
import psutil
import json
import datetime
import copy
import os

data_path = "./class.json"

with open(data_path, "r", encoding="utf-8") as f:
	json_data: dict = json.load(f)

##print(json_data)


# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------


@app.route("/class", methods=["POST"])
def calculate():
	data = request.get_json()
	ip_from = request.form
	# 进行计算
	print("服务端收到数据：", data)
	try:
		result = run(data)
	except Exception as error:
		print(error)
		return jsonify({"error": "server error"})
	else:
		return jsonify(result)


def run(data: dict):
	showClass = copy.deepcopy(json_data)
	curwekk = Current_week(data)
	# day = str(data["day"])
	# s = list(json_data[day])
	# print(json_data[day].keys())
	# print(day,json_data[day])

	# print(json_data["class-all"].keys(),'\n')
	for k, v in zip(json_data["class_all"].keys(), json_data["class_all"].values()):
		# print(k,v)
		# print(v.keys(),v.values(),"\n")

		for k2, v2 in zip(v.keys(), v.values()):
			# print(i["range_start"],i["range_end"])
			#print(k2, v2, "\n")
			if v2["lenth"] < 0:
				showClass["class_all"][k][k2] = {"lenth": v2["lenth"]}
				#print('add')
			elif curwekk > v2["range_start"] and curwekk < v2["range_end"]:	
					showClass["class_all"][k][k2] = {
						"lenth": v2["lenth"],
						"name": v2["name"],
						"position": v2["position"],
						"teacher": v2["teacher"],
						"colourid":v2["colourid"]
					}

	return showClass


def Current_week(data: dict):
	"""
	计算当前周
	"""
	start_date = datetime.datetime(
		json_data["base"]["start"]["year"],
		json_data["base"]["start"]["month"],
		json_data["base"]["start"]["date"],
	)
	end_date = datetime.datetime(data["year"], data["month"], data["date"])

	distance = end_date - start_date
	# print(distance.days)
	current_week = int(distance.days / 7) + 1
	#print("当前周：", current_week)

	return current_week


def Get_RAM():
	# 获取当前Python进程的内存占用情况
	process = psutil.Process()
	memory_info = process.memory_info()

	# 内存占用以字节为单位
	# print("内存占用：", memory_info.rss, "字节")
	# print("内存占用：", memory_info.rss / 1024, "KB")
	# print("内存占用：", memory_info.rss / (1024 * 1024), "MB")

	return round(memory_info.rss / (1024 * 1024), 2)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)), debug=True)
