; Auto-generated. Do not edit!


(cl:in-package sensor_repeater-msg)


;//! \htmlinclude CTD.msg.html

(cl:defclass <CTD> (roslisp-msg-protocol:ros-message)
  ((temperature
    :reader temperature
    :initarg :temperature
    :type cl:float
    :initform 0.0)
   (pressure
    :reader pressure
    :initarg :pressure
    :type cl:float
    :initform 0.0)
   (conductivity
    :reader conductivity
    :initarg :conductivity
    :type cl:float
    :initform 0.0))
)

(cl:defclass CTD (<CTD>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CTD>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CTD)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name sensor_repeater-msg:<CTD> is deprecated: use sensor_repeater-msg:CTD instead.")))

(cl:ensure-generic-function 'temperature-val :lambda-list '(m))
(cl:defmethod temperature-val ((m <CTD>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor_repeater-msg:temperature-val is deprecated.  Use sensor_repeater-msg:temperature instead.")
  (temperature m))

(cl:ensure-generic-function 'pressure-val :lambda-list '(m))
(cl:defmethod pressure-val ((m <CTD>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor_repeater-msg:pressure-val is deprecated.  Use sensor_repeater-msg:pressure instead.")
  (pressure m))

(cl:ensure-generic-function 'conductivity-val :lambda-list '(m))
(cl:defmethod conductivity-val ((m <CTD>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor_repeater-msg:conductivity-val is deprecated.  Use sensor_repeater-msg:conductivity instead.")
  (conductivity m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CTD>) ostream)
  "Serializes a message object of type '<CTD>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'temperature))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'pressure))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'conductivity))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CTD>) istream)
  "Deserializes a message object of type '<CTD>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'temperature) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'pressure) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'conductivity) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CTD>)))
  "Returns string type for a message object of type '<CTD>"
  "sensor_repeater/CTD")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CTD)))
  "Returns string type for a message object of type 'CTD"
  "sensor_repeater/CTD")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CTD>)))
  "Returns md5sum for a message object of type '<CTD>"
  "a076e86e73dc5de7777d643676c02fec")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CTD)))
  "Returns md5sum for a message object of type 'CTD"
  "a076e86e73dc5de7777d643676c02fec")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CTD>)))
  "Returns full string definition for message of type '<CTD>"
  (cl:format cl:nil "float32 temperature~%float32 pressure~%float32 conductivity~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CTD)))
  "Returns full string definition for message of type 'CTD"
  (cl:format cl:nil "float32 temperature~%float32 pressure~%float32 conductivity~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CTD>))
  (cl:+ 0
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CTD>))
  "Converts a ROS message object to a list"
  (cl:list 'CTD
    (cl:cons ':temperature (temperature msg))
    (cl:cons ':pressure (pressure msg))
    (cl:cons ':conductivity (conductivity msg))
))
