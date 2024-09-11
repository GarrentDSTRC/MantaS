// Generated by gencpp from file manta/CommandMsg.msg
// DO NOT EDIT!


#ifndef MANTA_MESSAGE_COMMANDMSG_H
#define MANTA_MESSAGE_COMMANDMSG_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace manta
{
template <class ContainerAllocator>
struct CommandMsg_
{
  typedef CommandMsg_<ContainerAllocator> Type;

  CommandMsg_()
    : ID(0)
    , command(0)  {
    }
  CommandMsg_(const ContainerAllocator& _alloc)
    : ID(0)
    , command(0)  {
  (void)_alloc;
    }



   typedef int32_t _ID_type;
  _ID_type ID;

   typedef int32_t _command_type;
  _command_type command;





  typedef boost::shared_ptr< ::manta::CommandMsg_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::manta::CommandMsg_<ContainerAllocator> const> ConstPtr;

}; // struct CommandMsg_

typedef ::manta::CommandMsg_<std::allocator<void> > CommandMsg;

typedef boost::shared_ptr< ::manta::CommandMsg > CommandMsgPtr;
typedef boost::shared_ptr< ::manta::CommandMsg const> CommandMsgConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::manta::CommandMsg_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::manta::CommandMsg_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::manta::CommandMsg_<ContainerAllocator1> & lhs, const ::manta::CommandMsg_<ContainerAllocator2> & rhs)
{
  return lhs.ID == rhs.ID &&
    lhs.command == rhs.command;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::manta::CommandMsg_<ContainerAllocator1> & lhs, const ::manta::CommandMsg_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace manta

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::manta::CommandMsg_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::manta::CommandMsg_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::manta::CommandMsg_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::manta::CommandMsg_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::manta::CommandMsg_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::manta::CommandMsg_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::manta::CommandMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "b2753e481737d8945149382683c76529";
  }

  static const char* value(const ::manta::CommandMsg_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xb2753e481737d894ULL;
  static const uint64_t static_value2 = 0x5149382683c76529ULL;
};

template<class ContainerAllocator>
struct DataType< ::manta::CommandMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "manta/CommandMsg";
  }

  static const char* value(const ::manta::CommandMsg_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::manta::CommandMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int32 ID\n"
"int32 command\n"
;
  }

  static const char* value(const ::manta::CommandMsg_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::manta::CommandMsg_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.ID);
      stream.next(m.command);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct CommandMsg_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::manta::CommandMsg_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::manta::CommandMsg_<ContainerAllocator>& v)
  {
    s << indent << "ID: ";
    Printer<int32_t>::stream(s, indent + "  ", v.ID);
    s << indent << "command: ";
    Printer<int32_t>::stream(s, indent + "  ", v.command);
  }
};

} // namespace message_operations
} // namespace ros

#endif // MANTA_MESSAGE_COMMANDMSG_H