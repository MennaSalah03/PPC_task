#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
from ppc_mission_interfaces.srv import Mission
from geometry_msgs.msg import Pose
from std_msgs.msg import String, Bool


class MissionClient(Node):
    def __init__(self):
        super().__init__('mission_client')
        self.client = self.create_client(Mission, '/mission')
        while not self.client.wait_for_service(timeout_sec = 1.0):
            self.get_logger().info('waiting...')
        self.request = Mission.Request()
    def send_request(self, name, target_position):
        self.request.target_position = target_position
        self.request.name = String(data=name)  
        self.future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
def main(args = None):
    rclpy.init(args=args)
    mission_client = MissionClient()
    name = sys.argv[1]
    position = Pose()
    position.position.x = float(sys.argv[2])
    position.position.y = float(sys.argv[3])
    response = mission_client.send_request(name, position)
    
    mission_client.get_logger().info('Acceptance status:' % (response.status))
    mission_client.destroy_node()
    rclpy.shutdown()
                               
if __name__ == '__main__':
    main()