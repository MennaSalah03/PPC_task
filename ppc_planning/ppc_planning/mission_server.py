#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ppc_planning_interfaces.srv import Mission
from std_msgs.msg import Bool

class MissionSrv(Node):
    def __init__(self):
        super().__init__('mission_server')
        self.srv = self.create_service(Mission, '/start_mission', self.mission_callback)
        self.response = Mission.Response()

    def mission_callback(self, request, response):
        if request.name == 'GoTo' or request.name == 'Stop':
            self.response.status = Bool(data = True)
            self.get_logger().info('Mission Accepted.')
        else:
            self.response.status = Bool(data=False)
            self.get_logger().info('Mission rejected')
        return response.status
def main(args = None):
    rclpy.init(args = args)
    mission = MissionSrv()
    rclpy.spin(mission)
    rclpy.shutdown()

if __name__ == '__main__':
    main()