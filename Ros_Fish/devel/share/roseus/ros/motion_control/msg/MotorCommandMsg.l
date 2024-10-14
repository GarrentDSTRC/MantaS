;; Auto-generated. Do not edit!


(when (boundp 'motion_control::MotorCommandMsg)
  (if (not (find-package "MOTION_CONTROL"))
    (make-package "MOTION_CONTROL"))
  (shadow 'MotorCommandMsg (find-package "MOTION_CONTROL")))
(unless (find-package "MOTION_CONTROL::MOTORCOMMANDMSG")
  (make-package "MOTION_CONTROL::MOTORCOMMANDMSG"))

(in-package "ROS")
;;//! \htmlinclude MotorCommandMsg.msg.html


(defclass motion_control::MotorCommandMsg
  :super ros::object
  :slots (_ID _command ))

(defmethod motion_control::MotorCommandMsg
  (:init
   (&key
    ((:ID __ID) 0)
    ((:command __command) 0)
    )
   (send-super :init)
   (setq _ID (round __ID))
   (setq _command (round __command))
   self)
  (:ID
   (&optional __ID)
   (if __ID (setq _ID __ID)) _ID)
  (:command
   (&optional __command)
   (if __command (setq _command __command)) _command)
  (:serialization-length
   ()
   (+
    ;; int32 _ID
    4
    ;; int32 _command
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _ID
       (write-long _ID s)
     ;; int32 _command
       (write-long _command s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _ID
     (setq _ID (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _command
     (setq _command (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get motion_control::MotorCommandMsg :md5sum-) "b2753e481737d8945149382683c76529")
(setf (get motion_control::MotorCommandMsg :datatype-) "motion_control/MotorCommandMsg")
(setf (get motion_control::MotorCommandMsg :definition-)
      "int32 ID
int32 command

")



(provide :motion_control/MotorCommandMsg "b2753e481737d8945149382683c76529")


