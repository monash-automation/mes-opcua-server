from opcuax import OpcuaModel
from pydantic import BaseModel


class RobotArmControl(BaseModel):
    joi1: float = 0.0
    joi2: float = 0.0
    joi3: float = 0.0
    joi4: float = 0.0
    joi5: float = 0.0
    joi6: float = 0.0
    joi7: float = 0.0
    vel: float = 0.0
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    rot_a: float = 0.0
    rot_b: float = 0.0
    rot_c: float = 0.0


class RobotArmData(BaseModel):
    joi1: float = 0.0
    joi2: float = 0.0
    joi3: float = 0.0
    joi4: float = 0.0
    joi5: float = 0.0
    joi6: float = 0.0
    joi7: float = 0.0
    tor1: float = 0.0
    tor2: float = 0.0
    tor3: float = 0.0
    tor4: float = 0.0
    tor5: float = 0.0
    tor6: float = 0.0
    tor7: float = 0.0
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    rot_a: float = 0.0
    rot_b: float = 0.0
    rot_c: float = 0.0
    for_x: float = 0.0
    for_y: float = 0.0
    for_z: float = 0.0
    mom_a: float = 0.0
    mom_b: float = 0.0
    mom_c: float = 0.0


class RobotArm(OpcuaModel):
    control: RobotArmControl = RobotArmControl()
    data: RobotArmData = RobotArmData()
