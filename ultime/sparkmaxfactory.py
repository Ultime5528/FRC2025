from rev import SparkMax


class SparkMaxFactory:
    _instances = {}

    @classmethod
    def create(cls, device_id, motor_type):
        # Create a unique key for each controller
        key = (
            device_id,
            motor_type.value if hasattr(motor_type, "value") else motor_type,
        )

        # Return existing instance if we have one
        if key not in cls._instances:
            cls._instances[key] = SparkMax(device_id, motor_type)

        return cls._instances[key]

    @classmethod
    def reset(cls):
        """Reset all instances (useful for testing)"""
        cls._instances = {}
