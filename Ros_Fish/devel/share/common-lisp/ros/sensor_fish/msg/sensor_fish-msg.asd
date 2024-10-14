
(cl:in-package :asdf)

(defsystem "sensor_fish-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "BatteryStatus" :depends-on ("_package_BatteryStatus"))
    (:file "_package_BatteryStatus" :depends-on ("_package"))
    (:file "DVLData" :depends-on ("_package_DVLData"))
    (:file "_package_DVLData" :depends-on ("_package"))
    (:file "Warmdepth" :depends-on ("_package_Warmdepth"))
    (:file "_package_Warmdepth" :depends-on ("_package"))
  ))