;; Auto-generated. Do not edit!


(when (boundp 'sensor_fish::BatteryStatus)
  (if (not (find-package "SENSOR_FISH"))
    (make-package "SENSOR_FISH"))
  (shadow 'BatteryStatus (find-package "SENSOR_FISH")))
(unless (find-package "SENSOR_FISH::BATTERYSTATUS")
  (make-package "SENSOR_FISH::BATTERYSTATUS"))

(in-package "ROS")
;;//! \htmlinclude BatteryStatus.msg.html


(defclass sensor_fish::BatteryStatus
  :super ros::object
  :slots (_total_voltage _soc _soh _relay_status ))

(defmethod sensor_fish::BatteryStatus
  (:init
   (&key
    ((:total_voltage __total_voltage) 0.0)
    ((:soc __soc) 0.0)
    ((:soh __soh) 0.0)
    ((:relay_status __relay_status) "")
    )
   (send-super :init)
   (setq _total_voltage (float __total_voltage))
   (setq _soc (float __soc))
   (setq _soh (float __soh))
   (setq _relay_status (string __relay_status))
   self)
  (:total_voltage
   (&optional __total_voltage)
   (if __total_voltage (setq _total_voltage __total_voltage)) _total_voltage)
  (:soc
   (&optional __soc)
   (if __soc (setq _soc __soc)) _soc)
  (:soh
   (&optional __soh)
   (if __soh (setq _soh __soh)) _soh)
  (:relay_status
   (&optional __relay_status)
   (if __relay_status (setq _relay_status __relay_status)) _relay_status)
  (:serialization-length
   ()
   (+
    ;; float32 _total_voltage
    4
    ;; float32 _soc
    4
    ;; float32 _soh
    4
    ;; string _relay_status
    4 (length _relay_status)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _total_voltage
       (sys::poke _total_voltage (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _soc
       (sys::poke _soc (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _soh
       (sys::poke _soh (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; string _relay_status
       (write-long (length _relay_status) s) (princ _relay_status s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _total_voltage
     (setq _total_voltage (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _soc
     (setq _soc (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _soh
     (setq _soh (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; string _relay_status
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _relay_status (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get sensor_fish::BatteryStatus :md5sum-) "aa534ae183105e5adab0c5d36158f85e")
(setf (get sensor_fish::BatteryStatus :datatype-) "sensor_fish/BatteryStatus")
(setf (get sensor_fish::BatteryStatus :definition-)
      "float32 total_voltage
float32 soc
float32 soh
string relay_status

")



(provide :sensor_fish/BatteryStatus "aa534ae183105e5adab0c5d36158f85e")


