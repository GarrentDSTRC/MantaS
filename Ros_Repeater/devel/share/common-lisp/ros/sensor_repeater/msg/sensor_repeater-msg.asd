
(cl:in-package :asdf)

(defsystem "sensor_repeater-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "CTD" :depends-on ("_package_CTD"))
    (:file "_package_CTD" :depends-on ("_package"))
  ))