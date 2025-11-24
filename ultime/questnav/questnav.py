from wpimath.geometry import (
    Pose3d,
    Translation3d,
    Rotation3d,
    Quaternion,
)


from .generated import data_pb2, commands_pb2, geometry2d_pb2, geometry3d_pb2

from wpilib import Timer
from ntcore import NetworkTableInstance


# --- QuestNav Class Conversion ---
class QuestNav:
    def __init__(self):
        self.nt4_instance = NetworkTableInstance.getDefault()
        self.quest_nav_table = self.nt4_instance.getTable("QuestNav")

        self.command_response_proto = commands_pb2.ProtobufQuestNavCommandResponse()
        self.command_proto = commands_pb2.ProtobufQuestNavCommand()
        self.pose2d_proto = geometry2d_pb2.ProtobufPose2d()
        self.pose3d_proto = geometry3d_pb2.ProtobufPose3d()
        self.device_data_proto = data_pb2.ProtobufQuestNavDeviceData()
        self.frame_data_proto = data_pb2.ProtobufQuestNavFrameData()

        # Subscribers and Publishers using RawTopic for protobuf data
        # Data is sent/received as JSON strings in this mock implementation
        self.response_topic = self.quest_nav_table.getRawTopic("response")
        self.response_subscriber = self.response_topic.subscribe(
            "protos:questnav.generated.commands.ProtobufQuestNavCommandResponse", b""
        )  # Subscribe to raw bytes (empty default)

        self.frame_data_topic = self.quest_nav_table.getRawTopic("frameData")
        self.frame_data_subscriber = self.frame_data_topic.subscribe(
            "protos:questnav.generated.data.ProtobufQuestNavFrameData", b""
        )

        self.device_data_topic = self.quest_nav_table.getRawTopic("deviceData")
        self.device_data_subscriber = self.device_data_topic.subscribe(
            "protos:questnav.generated.data.ProtobufQuestNavDeviceData", b""
        )

        self.request_topic = self.quest_nav_table.getRawTopic("request")
        self.request_publisher = self.request_topic.publish("raw")

        # Cached requests to lessen object creation (as in Java)
        self.cached_command_request = commands_pb2.ProtobufQuestNavCommand()
        self.cached_pose_reset_payload = commands_pb2.ProtobufQuestNavPoseResetPayload()
        self.cached_proto_pose = geometry3d_pb2.ProtobufPose3d()

        self.last_sent_request_id = 0
        self.last_processed_response_id = 0

    def set_3dpose(self, pose: Pose3d):
        self.cached_command_request.Clear()
        self.last_sent_request_id += 1

        self.cached_command_request.type = commands_pb2.QuestNavCommandType.POSE_RESET
        self.cached_command_request.command_id = self.last_sent_request_id
        payload = self.cached_command_request.pose_reset_payload
        payload.target_pose.translation.x = pose.translation().x
        payload.target_pose.translation.y = pose.translation().y
        payload.target_pose.translation.z = pose.translation().z

        payload.target_pose.rotation.q.w = pose.rotation().getQuaternion().W()
        payload.target_pose.rotation.q.x = pose.rotation().getQuaternion().X()
        payload.target_pose.rotation.q.y = pose.rotation().getQuaternion().Y()
        payload.target_pose.rotation.q.z = pose.rotation().getQuaternion().Z()

        self.request_publisher.set(self.cached_command_request.SerializeToString())

    def reset_pose(self):
        self.set_3dpose(Pose3d())

    def get_battery_percent(self) -> int:
        raw_data = self.device_data_subscriber.get()
        if not raw_data:
            return -1
        try:
            latest_device_data = data_pb2.ProtobufQuestNavDeviceData.FromString(
                raw_data
            )
            return latest_device_data.battery_percent
        except Exception:
            return -1

    def is_tracking(self) -> bool:
        raw_data = self.device_data_subscriber.get()
        if not raw_data:
            return False
        try:
            latest_device_data = data_pb2.ProtobufQuestNavDeviceData.FromString(
                raw_data
            )
            return bool(latest_device_data.currently_tracking)
        except Exception:
            return False

    def get_frame_count(self) -> int:
        raw_data = self.frame_data_subscriber.get()
        if not raw_data:
            return -1
        try:
            latest_frame_data = data_pb2.ProtobufQuestNavFrameData.FromString(raw_data)
            return latest_frame_data.frame_count
        except Exception as e:
            return -1

    def get_tracking_lost_counter(self) -> int:
        raw_data = self.device_data_subscriber.get()
        if not raw_data:
            return -1
        try:
            # Assuming raw_data is binary Protobuf, not JSON
            latest_device_data = data_pb2.ProtobufQuestNavDeviceData.FromString(
                raw_data
            )
            # Then check a specific field for tracking state
            return (
                latest_device_data.tracking_lost_counter
            )  # Or whatever field represents tracking
        except Exception as e:
            return -1

    def is_connected(self) -> bool:
        """
        Determines if the Quest headset is currently connected to the robot. Connection is determined
        by how stale the last received frame from the Quest is.

        Returns:
            Boolean indicating if the Quest is connected (true) or not (false)
        """
        # NetworkTables.get_server_time_us() provides the server time in microseconds
        # entry.last_change() provides the last change time in microseconds
        current_time_us = Timer.getTimestamp()
        last_change_us = self.frame_data_subscriber.getLastChange()

        # If last_change_us is 0, it means no data has been received yet
        if last_change_us == 0:
            return False

        # Convert to milliseconds for comparison (50 ms threshold)
        latency_ms = (current_time_us - last_change_us) / 1000.0
        return latency_ms < 50.0

    def get_latency(self) -> float:
        """
        Gets the latency of the Quest > Robot Connection. Returns the latency between the current time
        and the last frame data update.

        Returns:
            The latency in milliseconds
        """
        current_time_us = Timer.getTimestamp()
        last_change_us = self.frame_data_subscriber.getLastChange()

        if last_change_us == 0:
            return -1.0  # Indicate no data

        return (current_time_us - last_change_us) / 1000.0  # Latency in milliseconds

    def get_app_timestamp(self) -> float:
        """
        Returns the Quest app's uptime timestamp. For integration with a pose estimator, use
        `get_data_timestamp()` instead!

        Returns:
            The timestamp as a double value
        """
        raw_data = self.frame_data_subscriber.get()
        if not raw_data:
            return -1
        try:
            latest_frame_data = data_pb2.ProtobufQuestNavFrameData.FromString(raw_data)
            return latest_frame_data.timestamp
        except Exception as e:
            return -1

    def get_data_timestamp(self) -> float:
        """
        Gets the NT timestamp of when the last frame data was sent. This is the value which should be
        used with a pose estimator.

        Returns:
            The timestamp as a double value in seconds
        """
        # The Java code uses frameData.getAtomic().serverTime which is a NetworkTables internal timestamp.
        # In pynetworktables, the subscriber's last_change() gives the timestamp in microseconds.
        # We convert it to seconds.
        last_change_us = self.frame_data_subscriber.getLastChange()
        if last_change_us == 0:
            return -1.0
        return last_change_us / 1_000_000.0  # Convert microseconds to seconds

    def get_pose3d(self) -> Pose3d:
        raw_data = self.frame_data_subscriber.get()
        if not raw_data:
            return Pose3d(-100, -100, -100, Rotation3d())
        try:
            latest_frame_data = data_pb2.ProtobufQuestNavFrameData.FromString(raw_data)

            x = latest_frame_data.pose3d.translation.x
            y = latest_frame_data.pose3d.translation.y
            z = latest_frame_data.pose3d.translation.z

            rot = Rotation3d(
                Quaternion(
                    latest_frame_data.pose3d.rotation.q.w,
                    latest_frame_data.pose3d.rotation.q.x,
                    latest_frame_data.pose3d.rotation.q.y,
                    latest_frame_data.pose3d.rotation.q.z,
                )
            )

            return Pose3d(Translation3d(x, y, z), rot)
        except Exception as e:
            return Pose3d(
                -100, -100, -100, Rotation3d()
            )  # Return kZero if no data available

    def command_periodic(self):
        """Cleans up QuestNav responses after processing on the headset."""
        raw_response = self.response_subscriber.get()
        if not raw_response:
            return

        latest_command_response = (
            commands_pb2.ProtobufQuestNavCommandResponse.FromString(raw_response)
        )

        # if we don't have data or for some reason the response we got isn't for the command we sent,
        # skip for this loop
        if latest_command_response.command_id != self.last_sent_request_id:
            return

        if self.last_processed_response_id != latest_command_response.command_id:
            if not latest_command_response.success:
                print(
                    f"ERROR: QuestNav command failed!\n{latest_command_response.error_message}"
                )
            # don't double process
            self.last_processed_response_id = latest_command_response.command_id
