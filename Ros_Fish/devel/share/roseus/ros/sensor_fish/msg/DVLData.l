;; Auto-generated. Do not edit!


(when (boundp 'sensor_fish::DVLData)
  (if (not (find-package "SENSOR_FISH"))
    (make-package "SENSOR_FISH"))
  (shadow 'DVLData (find-package "SENSOR_FISH")))
(unless (find-package "SENSOR_FISH::DVLDATA")
  (make-package "SENSOR_FISH::DVLDATA"))

(in-package "ROS")
;;//! \htmlinclude DVLData.msg.html


(defclass sensor_fish::DVLData
  :super ros::object
  :slots (_heading _pitch _roll _dvl_height _dvl_velocity _stat_byte _latitude _longitude _altitude ))

(defmethod sensor_fish::DVLData
  (:init
   (&key
    ((:heading __heading) 0.0)
    ((:pitch __pitch) 0.0)
    ((:roll __roll) 0.0)
    ((:dvl_height __dvl_height) 0.0)
    ((:dvl_velocity __dvl_velocity) 0.0)
    ((:stat_byte __stat_byte) 0.0)
    ((:latitude __latitude) 0.0)
    ((:longitude __longitude) 0.0)
    ((:altitude __altitude) 0.0)
    )
   (send-super :init)
   (setq _heading (float __heading))
   (setq _pitch (float __pitch))
   (setq _roll (float __roll))
   (setq _dvl_height (float __dvl_height))
   (setq _dvl_velocity (float __dvl_velocity))
   (setq _stat_byte (float __stat_byte))
   (setq _latitude (float __latitude))
   (setq _longitude (float __longitude))
   (setq _altitude (float __altitude))
   self)
  (:heading
   (&optional __heading)
   (if __heading (setq _heading __heading)) _heading)
  (:pitch
   (&optional __pitch)
   (if __pitch (setq _pitch __pitch)) _pitch)
  (:roll
   (&optional __roll)
   (if __roll (setq _roll __roll)) _roll)
  (:dvl_height
   (&optional __dvl_height)
   (if __dvl_height (setq _dvl_height __dvl_height)) _dvl_height)
  (:dvl_velocity
   (&optional __dvl_velocity)
   (if __dvl_velocity (setq _dvl_velocity __dvl_velocity)) _dvl_velocity)
  (:stat_byte
   (&optional __stat_byte)
   (if __stat_byte (setq _stat_byte __stat_byte)) _stat_byte)
  (:latitude
   (&optional __latitude)
   (if __latitude (setq _latitude __latitude)) _latitude)
  (:longitude
   (&optional __longitude)
   (if __longitude (setq _longitude __longitude)) _longitude)
  (:altitude
   (&optional __altitude)
   (if __altitude (setq _altitude __altitude)) _altitude)
  (:serialization-length
   ()
   (+
    ;; float32 _heading
    4
    ;; float32 _pitch
    4
    ;; float32 _roll
    4
    ;; float32 _dvl_height
    4
    ;; float32 _dvl_velocity
    4
    ;; float32 _stat_byte
    4
    ;; float64 _latitude
    8
    ;; float64 _longitude
    8
    ;; float64 _altitude
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _heading
       (sys::poke _heading (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _pitch
       (sys::poke _pitch (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _roll
       (sys::poke _roll (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _dvl_height
       (sys::poke _dvl_height (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _dvl_velocity
       (sys::poke _dvl_velocity (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _stat_byte
       (sys::poke _stat_byte (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float64 _latitude
       (sys::poke _latitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _longitude
       (sys::poke _longitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _altitude
       (sys::poke _altitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _heading
     (setq _heading (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _pitch
     (setq _pitch (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _roll
     (setq _roll (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _dvl_height
     (setq _dvl_height (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _dvl_velocity
     (setq _dvl_velocity (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _stat_byte
     (setq _stat_byte (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float64 _latitude
     (setq _latitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _longitude
     (setq _longitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _altitude
     (setq _altitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get sensor_fish::DVLData :md5sum-) "846b42373420089c87c9f9ef42dc0ebc")
(setf (get sensor_fish::DVLData :datatype-) "sensor_fish/DVLData")
(setf (get sensor_fish::DVLData :definition-)
      "float32 heading
float32 pitch
float32 roll
float32 dvl_height
float32 dvl_velocity
float32 stat_byte
float64 latitude
float64 longitude
float64 altitude

")



(provide :sensor_fish/DVLData "846b42373420089c87c9f9ef42dc0ebc")


