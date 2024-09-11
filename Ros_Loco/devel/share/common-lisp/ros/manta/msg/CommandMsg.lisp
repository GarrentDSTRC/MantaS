; Auto-generated. Do not edit!


(cl:in-package manta-msg)


;//! \htmlinclude CommandMsg.msg.html

(cl:defclass <CommandMsg> (roslisp-msg-protocol:ros-message)
  ((ID
    :reader ID
    :initarg :ID
    :type cl:integer
    :initform 0)
   (command
    :reader command
    :initarg :command
    :type cl:integer
    :initform 0))
)

(cl:defclass CommandMsg (<CommandMsg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CommandMsg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CommandMsg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name manta-msg:<CommandMsg> is deprecated: use manta-msg:CommandMsg instead.")))

(cl:ensure-generic-function 'ID-val :lambda-list '(m))
(cl:defmethod ID-val ((m <CommandMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader manta-msg:ID-val is deprecated.  Use manta-msg:ID instead.")
  (ID m))

(cl:ensure-generic-function 'command-val :lambda-list '(m))
(cl:defmethod command-val ((m <CommandMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader manta-msg:command-val is deprecated.  Use manta-msg:command instead.")
  (command m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CommandMsg>) ostream)
  "Serializes a message object of type '<CommandMsg>"
  (cl:let* ((signed (cl:slot-value msg 'ID)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'command)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CommandMsg>) istream)
  "Deserializes a message object of type '<CommandMsg>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'ID) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'command) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CommandMsg>)))
  "Returns string type for a message object of type '<CommandMsg>"
  "manta/CommandMsg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CommandMsg)))
  "Returns string type for a message object of type 'CommandMsg"
  "manta/CommandMsg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CommandMsg>)))
  "Returns md5sum for a message object of type '<CommandMsg>"
  "b2753e481737d8945149382683c76529")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CommandMsg)))
  "Returns md5sum for a message object of type 'CommandMsg"
  "b2753e481737d8945149382683c76529")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CommandMsg>)))
  "Returns full string definition for message of type '<CommandMsg>"
  (cl:format cl:nil "int32 ID~%int32 command~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CommandMsg)))
  "Returns full string definition for message of type 'CommandMsg"
  (cl:format cl:nil "int32 ID~%int32 command~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CommandMsg>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CommandMsg>))
  "Converts a ROS message object to a list"
  (cl:list 'CommandMsg
    (cl:cons ':ID (ID msg))
    (cl:cons ':command (command msg))
))
