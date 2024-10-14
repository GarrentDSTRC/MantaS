// Auto-generated. Do not edit!

// (in-package sensor_fish.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class BatteryStatus {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.total_voltage = null;
      this.soc = null;
      this.soh = null;
      this.relay_status = null;
    }
    else {
      if (initObj.hasOwnProperty('total_voltage')) {
        this.total_voltage = initObj.total_voltage
      }
      else {
        this.total_voltage = 0.0;
      }
      if (initObj.hasOwnProperty('soc')) {
        this.soc = initObj.soc
      }
      else {
        this.soc = 0.0;
      }
      if (initObj.hasOwnProperty('soh')) {
        this.soh = initObj.soh
      }
      else {
        this.soh = 0.0;
      }
      if (initObj.hasOwnProperty('relay_status')) {
        this.relay_status = initObj.relay_status
      }
      else {
        this.relay_status = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type BatteryStatus
    // Serialize message field [total_voltage]
    bufferOffset = _serializer.float32(obj.total_voltage, buffer, bufferOffset);
    // Serialize message field [soc]
    bufferOffset = _serializer.float32(obj.soc, buffer, bufferOffset);
    // Serialize message field [soh]
    bufferOffset = _serializer.float32(obj.soh, buffer, bufferOffset);
    // Serialize message field [relay_status]
    bufferOffset = _serializer.string(obj.relay_status, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type BatteryStatus
    let len;
    let data = new BatteryStatus(null);
    // Deserialize message field [total_voltage]
    data.total_voltage = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [soc]
    data.soc = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [soh]
    data.soh = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [relay_status]
    data.relay_status = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.relay_status);
    return length + 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'sensor_fish/BatteryStatus';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'aa534ae183105e5adab0c5d36158f85e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 total_voltage
    float32 soc
    float32 soh
    string relay_status
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new BatteryStatus(null);
    if (msg.total_voltage !== undefined) {
      resolved.total_voltage = msg.total_voltage;
    }
    else {
      resolved.total_voltage = 0.0
    }

    if (msg.soc !== undefined) {
      resolved.soc = msg.soc;
    }
    else {
      resolved.soc = 0.0
    }

    if (msg.soh !== undefined) {
      resolved.soh = msg.soh;
    }
    else {
      resolved.soh = 0.0
    }

    if (msg.relay_status !== undefined) {
      resolved.relay_status = msg.relay_status;
    }
    else {
      resolved.relay_status = ''
    }

    return resolved;
    }
};

module.exports = BatteryStatus;
