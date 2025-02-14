#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
from ppc_planning_interfaces.srv import Mission
from ppc_planning_interfaces.msg import MissionInfo
from geometry_msgs.msg import Pose
from std_msgs.msg import String, Bool

class MissionClient(Node):
    def __init__(self):
        super().__init__('mission_client')
        self.client = self.create_client(Mission, '/start_mission')
        while not self.client.wait_for_service(timeout_sec = 1.0):
            self.get_logger().info('waiting...')
        self.request = Mission.Request()
        self.status_publisher = self.create_publisher(Bool, "/mission", 10)

    def send_request(self, name, target_position):
        self.request.target_position = target_position
        self.request.name = String(data = name)  
        self.future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    def publish_status(self, name, position):
        mission_msg = MissionInfo()
        mission_msg.name = name
        mission_msg.position = position

        self.status_publisher.publish(mission_msg)

def main(args = None):
    rclpy.init(args = args)
    mission_client = MissionClient()
    name = str(sys.argv[1])
    position = Pose()
    position.position.x = float(sys.argv[2])
    position.position.y = float(sys.argv[3])
    response = mission_client.send_request(name, position)
    mission_client.get_logger().info(f'Acceptance status: {response.status}')           
    if response.status == True:   
        mission_client.publish_status(name, position)
    mission_client.destroy_node()
    rclpy.shutdown()
                                
if __name__ == '__main__':
    main()