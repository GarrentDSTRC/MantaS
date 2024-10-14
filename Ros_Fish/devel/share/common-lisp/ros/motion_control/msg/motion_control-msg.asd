
(cl:in-package :asdf)

(defsystem "motion_control-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "MotorCommandMsg" :depends-on ("_package_MotorCommandMsg"))
    (:file "_package_MotorCommandMsg" :depends-on ("_package"))
    (:file "PropellerCommandMsg" :depends-on ("_package_PropellerCommandMsg"))
    (:file "_package_PropellerCommandMsg" :depends-on ("_package"))
  ))