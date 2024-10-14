;; Auto-generated. Do not edit!


(when (boundp 'sensor_repeater::CTD)
  (if (not (find-package "SENSOR_REPEATER"))
    (make-package "SENSOR_REPEATER"))
  (shadow 'CTD (find-package "SENSOR_REPEATER")))
(unless (find-package "SENSOR_REPEATER::CTD")
  (make-package "SENSOR_REPEATER::CTD"))

(in-package "ROS")
;;//! \htmlinclude CTD.msg.html


(defclass sensor_repeater::CTD
  :super ros::object
  :slots (_temperature _pressure _conductivity ))

(defmethod sensor_repeater::CTD
  (:init
   (&key
    ((:temperature __temperature) 0.0)
    ((:pressure __pressure) 0.0)
    ((:conductivity __conductivity) 0.0)
    )
   (send-super :init)
   (setq _temperature (float __temperature))
   (setq _pressure (float __pressure))
   (setq _conductivity (float __conductivity))
   self)
  (:temperature
   (&optional __temperature)
   (if __temperature (setq _temperature __temperature)) _temperature)
  (:pressure
   (&optional __pressure)
   (if __pressure (setq _pressure __pressure)) _pressure)
  (:conductivity
   (&optional __conductivity)
   (if __conductivity (setq _conductivity __conductivity)) _conductivity)
  (:serialization-length
   ()
   (+
    ;; float32 _temperature
    4
    ;; float32 _pressure
    4
    ;; float32 _conductivity
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _temperature
       (sys::poke _temperature (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _pressure
       (sys::poke _pressure (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _conductivity
       (sys::poke _conductivity (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _temperature
     (setq _temperature (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _pressure
     (setq _pressure (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _conductivity
     (setq _conductivity (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get sensor_repeater::CTD :md5sum-) "a076e86e73dc5de7777d643676c02fec")
(setf (get sensor_repeater::CTD :datatype-) "sensor_repeater/CTD")
(setf (get sensor_repeater::CTD :definition-)
      "float32 temperature
float32 pressure
float32 conductivity

")



(provide :sensor_repeater/CTD "a076e86e73dc5de7777d643676c02fec")


