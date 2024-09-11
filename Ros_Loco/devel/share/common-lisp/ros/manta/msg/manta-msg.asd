
(cl:in-package :asdf)

(defsystem "manta-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "CommandMsg" :depends-on ("_package_CommandMsg"))
    (:file "_package_CommandMsg" :depends-on ("_package"))
    (:file "MotorCommandMsg" :depends-on ("_package_MotorCommandMsg"))
    (:file "_package_MotorCommandMsg" :depends-on ("_package"))
    (:file "PropellerCommandMsg" :depends-on ("_package_PropellerCommandMsg"))
    (:file "_package_PropellerCommandMsg" :depends-on ("_package"))
    (:file "Warmdepth" :depends-on ("_package_Warmdepth"))
    (:file "_package_Warmdepth" :depends-on ("_package"))
  ))