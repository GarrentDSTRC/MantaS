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

class DVLData {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.heading = null;
      this.pitch = null;
      this.roll = null;
      this.dvl_height = null;
      this.dvl_velocity = null;
      this.stat_byte = null;
      this.latitude = null;
      this.longitude = null;
      this.altitude = null;
    }
    else {
      if (initObj.hasOwnProperty('heading')) {
        this.heading = initObj.heading
      }
      else {
        this.heading = 0.0;
      }
      if (initObj.hasOwnProperty('pitch')) {
        this.pitch = initObj.pitch
      }
      else {
        this.pitch = 0.0;
      }
      if (initObj.hasOwnProperty('roll')) {
        this.roll = initObj.roll
      }
      else {
        this.roll = 0.0;
      }
      if (initObj.hasOwnProperty('dvl_height')) {
        this.dvl_height = initObj.dvl_height
      }
      else {
        this.dvl_height = 0.0;
      }
      if (initObj.hasOwnProperty('dvl_velocity')) {
        this.dvl_velocity = initObj.dvl_velocity
      }
      else {
        this.dvl_velocity = 0.0;
      }
      if (initObj.hasOwnProperty('stat_byte')) {
        this.stat_byte = initObj.stat_byte
      }
      else {
        this.stat_byte = 0.0;
      }
      if (initObj.hasOwnProperty('latitude')) {
        this.latitude = initObj.latitude
      }
      else {
        this.latitude = 0.0;
      }
      if (initObj.hasOwnProperty('longitude')) {
        this.longitude = initObj.longitude
      }
      else {
        this.longitude = 0.0;
      }
      if (initObj.hasOwnProperty('altitude')) {
        this.altitude = initObj.altitude
      }
      else {
        this.altitude = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type DVLData
    // Serialize message field [heading]
    bufferOffset = _serializer.float32(obj.heading, buffer, bufferOffset);
    // Serialize message field [pitch]
    bufferOffset = _serializer.float32(obj.pitch, buffer, bufferOffset);
    // Serialize message field [roll]
    bufferOffset = _serializer.float32(obj.roll, buffer, bufferOffset);
    // Serialize message field [dvl_height]
    bufferOffset = _serializer.float32(obj.dvl_height, buffer, bufferOffset);
    // Serialize message field [dvl_velocity]
    bufferOffset = _serializer.float32(obj.dvl_velocity, buffer, bufferOffset);
    // Serialize message field [stat_byte]
    bufferOffset = _serializer.float32(obj.stat_byte, buffer, bufferOffset);
    // Serialize message field [latitude]
    bufferOffset = _serializer.float64(obj.latitude, buffer, bufferOffset);
    // Serialize message field [longitude]
    bufferOffset = _serializer.float64(obj.longitude, buffer, bufferOffset);
    // Serialize message field [altitude]
    bufferOffset = _serializer.float64(obj.altitude, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type DVLData
    let len;
    let data = new DVLData(null);
    // Deserialize message field [heading]
    data.heading = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [pitch]
    data.pitch = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [roll]
    data.roll = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [dvl_height]
    data.dvl_height = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [dvl_velocity]
    data.dvl_velocity = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [stat_byte]
    data.stat_byte = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [latitude]
    data.latitude = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [longitude]
    data.longitude = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [altitude]
    data.altitude = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 48;
  }

  static datatype() {
    // Returns string type for a message object
    return 'sensor_fish/DVLData';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '846b42373420089c87c9f9ef42dc0ebc';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 heading
    float32 pitch
    float32 roll
    float32 dvl_height
    float32 dvl_velocity
    float32 stat_byte
    float64 latitude
    float64 longitude
    float64 altitude
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new DVLData(null);
    if (msg.heading !== undefined) {
      resolved.heading = msg.heading;
    }
    else {
      resolved.heading = 0.0
    }

    if (msg.pitch !== undefined) {
      resolved.pitch = msg.pitch;
    }
    else {
      resolved.pitch = 0.0
    }

    if (msg.roll !== undefined) {
      resolved.roll = msg.roll;
    }
    else {
      resolved.roll = 0.0
    }

    if (msg.dvl_height !== undefined) {
      resolved.dvl_height = msg.dvl_height;
    }
    else {
      resolved.dvl_height = 0.0
    }

    if (msg.dvl_velocity !== undefined) {
      resolved.dvl_velocity = msg.dvl_velocity;
    }
    else {
      resolved.dvl_velocity = 0.0
    }

    if (msg.stat_byte !== undefined) {
      resolved.stat_byte = msg.stat_byte;
    }
    else {
      resolved.stat_byte = 0.0
    }

    if (msg.latitude !== undefined) {
      resolved.latitude = msg.latitude;
    }
    else {
      resolved.latitude = 0.0
    }

    if (msg.longitude !== undefined) {
      resolved.longitude = msg.longitude;
    }
    else {
      resolved.longitude = 0.0
    }

    if (msg.altitude !== undefined) {
      resolved.altitude = msg.altitude;
    }
    else {
      resolved.altitude = 0.0
    }

    return resolved;
    }
};

module.exports = DVLData;
