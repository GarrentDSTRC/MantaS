;; Auto-generated. Do not edit!


(when (boundp 'manta::Warmdepth)
  (if (not (find-package "MANTA"))
    (make-package "MANTA"))
  (shadow 'Warmdepth (find-package "MANTA")))
(unless (find-package "MANTA::WARMDEPTH")
  (make-package "MANTA::WARMDEPTH"))

(in-package "ROS")
;;//! \htmlinclude Warmdepth.msg.html


(defclass manta::Warmdepth
  :super ros::object
  :slots (_time _height _temp _depth _pressure _roll _pitch _yaw ))

(defmethod manta::Warmdepth
  (:init
   (&key
    ((:time __time) "")
    ((:height __height) 0.0)
    ((:temp __temp) 0.0)
    ((:depth __depth) 0.0)
    ((:pressure __pressure) 0.0)
    ((:roll __roll) 0.0)
    ((:pitch __pitch) 0.0)
    ((:yaw __yaw) 0.0)
    )
   (send-super :init)
   (setq _time (string __time))
   (setq _height (float __height))
   (setq _temp (float __temp))
   (setq _depth (float __depth))
   (setq _pressure (float __pressure))
   (setq _roll (float __roll))
   (setq _pitch (float __pitch))
   (setq _yaw (float __yaw))
   self)
  (:time
   (&optional __time)
   (if __time (setq _time __time)) _time)
  (:height
   (&optional __height)
   (if __height (setq _height __height)) _height)
  (:temp
   (&optional __temp)
   (if __temp (setq _temp __temp)) _temp)
  (:depth
   (&optional __depth)
   (if __depth (setq _depth __depth)) _depth)
  (:pressure
   (&optional __pressure)
   (if __pressure (setq _pressure __pressure)) _pressure)
  (:roll
   (&optional __roll)
   (if __roll (setq _roll __roll)) _roll)
  (:pitch
   (&optional __pitch)
   (if __pitch (setq _pitch __pitch)) _pitch)
  (:yaw
   (&optional __yaw)
   (if __yaw (setq _yaw __yaw)) _yaw)
  (:serialization-length
   ()
   (+
    ;; string _time
    4 (length _time)
    ;; float32 _height
    4
    ;; float32 _temp
    4
    ;; float32 _depth
    4
    ;; float32 _pressure
    4
    ;; float32 _roll
    4
    ;; float32 _pitch
    4
    ;; float32 _yaw
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _time
       (write-long (length _time) s) (princ _time s)
     ;; float32 _height
       (sys::poke _height (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _temp
       (sys::poke _temp (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _depth
       (sys::poke _depth (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _pressure
       (sys::poke _pressure (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _roll
       (sys::poke _roll (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _pitch
       (sys::poke _pitch (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _yaw
       (sys::poke _yaw (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _time
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _time (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float32 _height
     (setq _height (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _temp
     (setq _temp (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _depth
     (setq _depth (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _pressure
     (setq _pressure (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _roll
     (setq _roll (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _pitch
     (setq _pitch (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _yaw
     (setq _yaw (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get manta::Warmdepth :md5sum-) "0f43c6bd4e53f4d204b397bebc018f0b")
(setf (get manta::Warmdepth :datatype-) "manta/Warmdepth")
(setf (get manta::Warmdepth :definition-)
      "string time
float32 height
float32 temp
float32 depth
float32 pressure
float32 roll
float32 pitch
float32 yaw

")



(provide :manta/Warmdepth "0f43c6bd4e53f4d204b397bebc018f0b")


