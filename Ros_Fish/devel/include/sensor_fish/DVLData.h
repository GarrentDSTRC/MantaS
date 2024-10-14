// Generated by gencpp from file sensor_fish/DVLData.msg
// DO NOT EDIT!


#ifndef SENSOR_FISH_MESSAGE_DVLDATA_H
#define SENSOR_FISH_MESSAGE_DVLDATA_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace sensor_fish
{
template <class ContainerAllocator>
struct DVLData_
{
  typedef DVLData_<ContainerAllocator> Type;

  DVLData_()
    : heading(0.0)
    , pitch(0.0)
    , roll(0.0)
    , dvl_height(0.0)
    , dvl_velocity(0.0)
    , stat_byte(0.0)
    , latitude(0.0)
    , longitude(0.0)
    , altitude(0.0)  {
    }
  DVLData_(const ContainerAllocator& _alloc)
    : heading(0.0)
    , pitch(0.0)
    , roll(0.0)
    , dvl_height(0.0)
    , dvl_velocity(0.0)
    , stat_byte(0.0)
    , latitude(0.0)
    , longitude(0.0)
    , altitude(0.0)  {
  (void)_alloc;
    }



   typedef float _heading_type;
  _heading_type heading;

   typedef float _pitch_type;
  _pitch_type pitch;

   typedef float _roll_type;
  _roll_type roll;

   typedef float _dvl_height_type;
  _dvl_height_type dvl_height;

   typedef float _dvl_velocity_type;
  _dvl_velocity_type dvl_velocity;

   typedef float _stat_byte_type;
  _stat_byte_type stat_byte;

   typedef double _latitude_type;
  _latitude_type latitude;

   typedef double _longitude_type;
  _longitude_type longitude;

   typedef double _altitude_type;
  _altitude_type altitude;





  typedef boost::shared_ptr< ::sensor_fish::DVLData_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::sensor_fish::DVLData_<ContainerAllocator> const> ConstPtr;

}; // struct DVLData_

typedef ::sensor_fish::DVLData_<std::allocator<void> > DVLData;

typedef boost::shared_ptr< ::sensor_fish::DVLData > DVLDataPtr;
typedef boost::shared_ptr< ::sensor_fish::DVLData const> DVLDataConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::sensor_fish::DVLData_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::sensor_fish::DVLData_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::sensor_fish::DVLData_<ContainerAllocator1> & lhs, const ::sensor_fish::DVLData_<ContainerAllocator2> & rhs)
{
  return lhs.heading == rhs.heading &&
    lhs.pitch == rhs.pitch &&
    lhs.roll == rhs.roll &&
    lhs.dvl_height == rhs.dvl_height &&
    lhs.dvl_velocity == rhs.dvl_velocity &&
    lhs.stat_byte == rhs.stat_byte &&
    lhs.latitude == rhs.latitude &&
    lhs.longitude == rhs.longitude &&
    lhs.altitude == rhs.altitude;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::sensor_fish::DVLData_<ContainerAllocator1> & lhs, const ::sensor_fish::DVLData_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace sensor_fish

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::sensor_fish::DVLData_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::sensor_fish::DVLData_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::sensor_fish::DVLData_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::sensor_fish::DVLData_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::sensor_fish::DVLData_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::sensor_fish::DVLData_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::sensor_fish::DVLData_<ContainerAllocator> >
{
  static const char* value()
  {
    return "846b42373420089c87c9f9ef42dc0ebc";
  }

  static const char* value(const ::sensor_fish::DVLData_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x846b42373420089cULL;
  static const uint64_t static_value2 = 0x87c9f9ef42dc0ebcULL;
};

template<class ContainerAllocator>
struct DataType< ::sensor_fish::DVLData_<ContainerAllocator> >
{
  static const char* value()
  {
    return "sensor_fish/DVLData";
  }

  static const char* value(const ::sensor_fish::DVLData_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::sensor_fish::DVLData_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32 heading\n"
"float32 pitch\n"
"float32 roll\n"
"float32 dvl_height\n"
"float32 dvl_velocity\n"
"float32 stat_byte\n"
"float64 latitude\n"
"float64 longitude\n"
"float64 altitude\n"
;
  }

  static const char* value(const ::sensor_fish::DVLData_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::sensor_fish::DVLData_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.heading);
      stream.next(m.pitch);
      stream.next(m.roll);
      stream.next(m.dvl_height);
      stream.next(m.dvl_velocity);
      stream.next(m.stat_byte);
      stream.next(m.latitude);
      stream.next(m.longitude);
      stream.next(m.altitude);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct DVLData_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::sensor_fish::DVLData_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::sensor_fish::DVLData_<ContainerAllocator>& v)
  {
    s << indent << "heading: ";
    Printer<float>::stream(s, indent + "  ", v.heading);
    s << indent << "pitch: ";
    Printer<float>::stream(s, indent + "  ", v.pitch);
    s << indent << "roll: ";
    Printer<float>::stream(s, indent + "  ", v.roll);
    s << indent << "dvl_height: ";
    Printer<float>::stream(s, indent + "  ", v.dvl_height);
    s << indent << "dvl_velocity: ";
    Printer<float>::stream(s, indent + "  ", v.dvl_velocity);
    s << indent << "stat_byte: ";
    Printer<float>::stream(s, indent + "  ", v.stat_byte);
    s << indent << "latitude: ";
    Printer<double>::stream(s, indent + "  ", v.latitude);
    s << indent << "longitude: ";
    Printer<double>::stream(s, indent + "  ", v.longitude);
    s << indent << "altitude: ";
    Printer<double>::stream(s, indent + "  ", v.altitude);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SENSOR_FISH_MESSAGE_DVLDATA_H
