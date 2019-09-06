#!/usr/bin/env python


'''This is a converter for the Intel Research Lab SLAM dataset
   ( http://kaspar.informatik.uni-freiburg.de/~slamEvaluation/datasets/intel.clf )
   to rosbag'''
import logging
logging.basicConfig()

import rospy
import rosbag
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from math import pi
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import TransformStamped
import tf

def make_tf_msg(x, y, theta, t,base,base0):
    trans = TransformStamped()
    trans.header.stamp = t
    trans.header.frame_id = base
    trans.child_frame_id = base0
    trans.transform.translation.x = x
    trans.transform.translation.y = y
    q = tf.transformations.quaternion_from_euler(0, 0, theta)
    trans.transform.rotation.x = q[0]
    trans.transform.rotation.y = q[1]
    trans.transform.rotation.z = q[2]
    trans.transform.rotation.w = q[3]

    msg = TFMessage()
    msg.transforms.append(trans)
    return msg

with open('/home/zengjun/workset_zongmu_slam/radar2bag/Lidar2_1_leijia.txt') as dataset:
    with rosbag.Bag('/home/zengjun/workset_zongmu_slam/Gmapping/radar_simu2_1_leijia.bag', 'w') as bag:
        for line in dataset.readlines():
            line = line.strip()
            tokens = line.split(' ')
            num_scans = 720
            '''
            if len(tokens) <= 2:
                rospy.logwarn("unsupported scan format")
                continue
            '''

            msg = LaserScan()
            msg.header.frame_id = 'base_link'
            t = rospy.Time(float(tokens[(num_scans)]))
            msg.header.stamp = t
            msg.angle_min = -180.0 / 180.0 * pi
            msg.angle_max = 180.0 / 180.0 * pi
            msg.angle_increment = 2*pi / num_scans
            msg.time_increment = 0.2 / 360.0
            msg.scan_time = 0.2  #leijia 
            msg.range_min = 0.001
            msg.range_max = 18.0
            msg.ranges = [float(r) for r in tokens[0:(num_scans + 1)]]

            bag.write('scan', msg, t)
            #hector need LaserScan as topic name for prepared launch
'''
with open('/home/zengjun/workset_zongmu_slam/radar2bag/odom2_1_leijia.txt') as dataset:
    with rosbag.Bag('/home/zengjun/workset_zongmu_slam/Gmapping/radar_simu_tf2_1_leijia.bag', 'a+') as bag:
        for line in dataset.readlines():
            line = line.strip()
            tokens = line.split(' ')
            num_scans = 720
            if len(tokens) <= 2:
                continue
            else:
                msg.header.frame_id = 'base_link'
                t = rospy.Time(float(tokens[4]))
                msg.header.stamp = t
                msg.angle_min = -90.0 / 180.0 * pi
                msg.angle_max = 90.0 / 180.0 * pi
                msg.angle_increment = pi / num_scans
                msg.time_increment = 0.2 / 360.0
                msg.scan_time = 0.2
                msg.range_min = 0.001
                msg.range_max = 18
                msg.ranges = [float(r) for r in tokens[2:(num_scans + 2)]]

                #bag.write('scan', msg, t)

                odom_x, odom_y, odom_theta = [float(r) for r in tokens[0:3]]
                tf_msg = make_tf_msg(odom_x, odom_y, odom_theta, t,'base_link','base_laser_link')
                bag.write('tf', tf_msg, t)

'''
