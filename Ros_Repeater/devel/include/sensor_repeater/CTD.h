// Generated by gencpp from file sensor_repeater/CTD.msg
// DO NOT EDIT!


#ifndef SENSOR_REPEATER_MESSAGE_CTD_H
#define SENSOR_REPEATER_MESSAGE_CTD_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace sensor_repeater
{
template <class ContainerAllocator>
struct CTD_
{
  typedef CTD_<ContainerAllocator> Type;

  CTD_()
    : temperature(0.0)
    , pressure(0.0)
    , conductivity(0.0)  {
    }
  CTD_(const ContainerAllocator& _alloc)
    : temperature(0.0)
    , pressure(0.0)
    , conductivity(0.0)  {
  (void)_alloc;
    }



   typedef float _temperature_type;
  _temperature_type temperature;

   typedef float _pressure_type;
  _pressure_type pressure;

   typedef float _conductivity_type;
  _conductivity_type conductivity;





  typedef boost::shared_ptr< ::sensor_repeater::CTD_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::sensor_repeater::CTD_<ContainerAllocator> const> ConstPtr;

}; // struct CTD_

typedef ::sensor_repeater::CTD_<std::allocator<void> > CTD;

typedef boost::shared_ptr< ::sensor_repeater::CTD > CTDPtr;
typedef boost::shared_ptr< ::sensor_repeater::CTD const> CTDConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::sensor_repeater::CTD_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::sensor_repeater::CTD_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::sensor_repeater::CTD_<ContainerAllocator1> & lhs, const ::sensor_repeater::CTD_<ContainerAllocator2> & rhs)
{
  return lhs.temperature == rhs.temperature &&
    lhs.pressure == rhs.pressure &&
    lhs.conductivity == rhs.conductivity;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::sensor_repeater::CTD_<ContainerAllocator1> & lhs, const ::sensor_repeater::CTD_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace sensor_repeater

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::sensor_repeater::CTD_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::sensor_repeater::CTD_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::sensor_repeater::CTD_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::sensor_repeater::CTD_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::sensor_repeater::CTD_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::sensor_repeater::CTD_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::sensor_repeater::CTD_<ContainerAllocator> >
{
  static const char* value()
  {
    return "a076e86e73dc5de7777d643676c02fec";
  }

  static const char* value(const ::sensor_repeater::CTD_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xa076e86e73dc5de7ULL;
  static const uint64_t static_value2 = 0x777d643676c02fecULL;
};

template<class ContainerAllocator>
struct DataType< ::sensor_repeater::CTD_<ContainerAllocator> >
{
  static const char* value()
  {
    return "sensor_repeater/CTD";
  }

  static const char* value(const ::sensor_repeater::CTD_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::sensor_repeater::CTD_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32 temperature\n"
"float32 pressure\n"
"float32 conductivity\n"
;
  }

  static const char* value(const ::sensor_repeater::CTD_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::sensor_repeater::CTD_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.temperature);
      stream.next(m.pressure);
      stream.next(m.conductivity);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct CTD_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::sensor_repeater::CTD_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::sensor_repeater::CTD_<ContainerAllocator>& v)
  {
    s << indent << "temperature: ";
    Printer<float>::stream(s, indent + "  ", v.temperature);
    s << indent << "pressure: ";
    Printer<float>::stream(s, indent + "  ", v.pressure);
    s << indent << "conductivity: ";
    Printer<float>::stream(s, indent + "  ", v.conductivity);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SENSOR_REPEATER_MESSAGE_CTD_H