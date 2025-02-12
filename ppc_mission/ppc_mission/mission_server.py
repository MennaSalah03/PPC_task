#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ppc_mission_interfaces.srv import Mission
from std_msgs.msg import Bool

class MissionSrv(Node):
    def __init__(self):
        super().__init__('mission_server')
        self.srv = self.create_service(Mission, '/mission', self.mission_callback)

    def mission_callback(self, request, response):
        if request.name == "GoTo" or request.name == "Stop":
            response.status = Bool(data = True)
            self.get_logger().info('Mission Accepted.')
        else:
            response.status = Bool(data = False)
            self.get_logger().info('Mission rejected')
        return response
    
def main(args = None):
    rclpy.init(args = args)
    mission = MissionSrv()
    rclpy.spin(mission)
    rclpy.shutdown()

if __name__ == '__main__':
    main()