;; Auto-generated. Do not edit!


(when (boundp 'manta::CommandMsg)
  (if (not (find-package "MANTA"))
    (make-package "MANTA"))
  (shadow 'CommandMsg (find-package "MANTA")))
(unless (find-package "MANTA::COMMANDMSG")
  (make-package "MANTA::COMMANDMSG"))

(in-package "ROS")
;;//! \htmlinclude CommandMsg.msg.html


(defclass manta::CommandMsg
  :super ros::object
  :slots (_ID _command ))

(defmethod manta::CommandMsg
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

(setf (get manta::CommandMsg :md5sum-) "b2753e481737d8945149382683c76529")
(setf (get manta::CommandMsg :datatype-) "manta/CommandMsg")
(setf (get manta::CommandMsg :definition-)
      "int32 ID
int32 command

")



(provide :manta/CommandMsg "b2753e481737d8945149382683c76529")


