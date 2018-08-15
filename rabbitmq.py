#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 下午2:01
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : rabbitmq.py
# @Software: PyCharm

import pika
import sys

username = 'guest'
pwd = 'guest'
user_pwd = pika.PlainCredentials(username, pwd)

# 创建连接
print('connect to server rabbitmq')
s_conn = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.10.24', credentials=user_pwd, port=5672))
# 在连接上创建一个频道
print('connect successfully')
chan = s_conn.channel()

#声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
chan.queue_declare(queue='hello')
print('开始插入数据')
chan.basic_publish(exchange='',  # 交换机
                   routing_key='hello',# 路由键，写明将消息发往哪个队列，本例是将消息发往队列hello
                   body='123233h')# 生产者要发送的消息
print("[生产者] send 'hello world")

#当生产者发送完消息后，可选择关闭连接
s_conn.close()
