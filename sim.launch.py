from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    world = LaunchConfiguration("world")
    use_sim_time = LaunchConfiguration("use_sim_time")

    gazebo_share = get_package_share_directory("gazebo_ros")
    package_root = os.path.dirname(os.path.dirname(__file__))
    default_world = os.path.join(package_root, "worlds", "navigation.world")
    robot_description_path = os.path.join(package_root, "urdf", "diff_drive_bot.urdf")

    with open(robot_description_path, "r", encoding="utf-8") as handle:
        robot_description = handle.read()

    return LaunchDescription(
        [
            DeclareLaunchArgument("world", default_value=default_world),
            DeclareLaunchArgument("use_sim_time", default_value="true"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(gazebo_share, "launch", "gazebo.launch.py")
                ),
                launch_arguments={"world": world}.items(),
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="screen",
                parameters=[
                    {"robot_description": robot_description, "use_sim_time": use_sim_time}
                ],
            ),
            Node(
                package="gazebo_ros",
                executable="spawn_entity.py",
                arguments=["-entity", "diff_drive_bot", "-topic", "robot_description"],
                output="screen",
            ),
        ]
    )
