#include <iostream>
#include <boost/asio.hpp>
#include <boost/algorithm/string.hpp>
#include <vector>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <thread>

using namespace boost::asio;
using namespace std;

serial_port *Com485_Sensor;

string get_current_time() {
    auto now = std::chrono::system_clock::now();
    auto in_time_t = std::chrono::system_clock::to_time_t(now);
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;

    stringstream ss;
    ss << put_time(localtime(&in_time_t), "%Y-%m-%d %H:%M:%S")
       << '.' << setfill('0') << setw(3) << ms.count();
    return ss.str();
}

void Get485_Info_Altitude_Sensor(vector<string>& data) {
    if (data[0] == "$ISHPR") {  // Altitude sensor: body status (level meter)
        if (data.size() >= 4) {
            string heading = data[1];
            string pitch = data[2];
            string roll = data[3].substr(0, data[3].find('*'));
            string result = "ISHPR, " + heading + ", " + pitch + ", " + roll;
            string current_time = get_current_time();
            cout << "machine status : " << result << endl;
        } else {
            cerr << "Data format error: " << boost::algorithm::join(data, ", ") << endl;
        }
    }

    if (data[0] == "$ISADS") {  // Altitude sensor: temperature, altitude status
        if (data.size() >= 4) {
            string height = data[1];
            string temp = data[3];
            string result = "ISADS, " + height + ", " + temp;
            string current_time = get_current_time();
            cout << "height status : " << result << endl;
        } else {
            cerr << "Data format error: " << boost::algorithm::join(data, ", ") << endl;
        }
    }
}

void Get485_Info_Depth_Temperature_Sensor(vector<string>& data) {
    if (data[0] == "$ISDPT") {  // Depth and temperature sensor
        if (data.size() >= 6) {
            string depth = data[1];
            string pressure = data[3];
            string temp = data[5];
            string result = "ISDPT, " + depth + ", " + pressure + ", " + temp;
            string current_time = get_current_time();
            cout << "temperature and depth status : " << result << endl;
        } else {
            cerr << "Data format error: " << boost::algorithm::join(data, ", ") << endl;
        }
    }
}

void Get_All_Data_from_485(string& OriginalData) {
    try {
        vector<string> data;
        boost::split(data, OriginalData, boost::is_any_of(","));
        if (data[0] == "$ISHPR" || data[0] == "$ISADS") {  // Altitude sensor: body status (level meter)
            Get485_Info_Altitude_Sensor(data);
        }
        if (data[0] == "$ISDPT") {  // Depth and temperature sensor
            Get485_Info_Depth_Temperature_Sensor(data);
        }
    } catch (const exception& e) {  // Handle exceptions, usually caused by electromagnetic interference from multiple devices
        cerr << e.what() << endl;
    }
}

void Send_Request_and_Read_Response(string request) {
    boost::asio::write(*Com485_Sensor, boost::asio::buffer(request));
    std::this_thread::sleep_for(std::chrono::milliseconds(1));  // Adjust sleep time based on sensor response time

    char c;
    string Original_Data;
    while (true) {
        boost::asio::read(*Com485_Sensor, boost::asio::buffer(&c, 1));
        if (c == '\n') break;
        Original_Data += c;
    }

    if (!Original_Data.empty() && Original_Data[0] == '$') {  // '$' is the ASCII code for '$'
        Get_All_Data_from_485(Original_Data);
    } else {
        cerr << "Invalid data received: " << Original_Data << endl;
    }
}

void load_params() {
    string serial_port_name = "/dev/ttyUSB0";  // Adjust this based on your setup
    unsigned int baud_rate = 9600;  // Adjust this based on your setup

    io_service io;
    Com485_Sensor = new serial_port(io, serial_port_name);
    Com485_Sensor->set_option(serial_port_base::baud_rate(baud_rate));
    Com485_Sensor->set_option(serial_port_base::character_size(8));
    Com485_Sensor->set_option(serial_port_base::parity(serial_port_base::parity::none));
    Com485_Sensor->set_option(serial_port_base::stop_bits(serial_port_base::stop_bits::one));
    Com485_Sensor->set_option(serial_port_base::flow_control(serial_port_base::flow_control::none));
}

void Start() {
    load_params();
    while (true) {
        // Request altitude sensor data
        Send_Request_and_Read_Response("$ISADS\n");
        // Request depth and temperature sensor data
        Send_Request_and_Read_Response("$ISDPT\n");
    }
}

int main() {
    Start();
    return 0;
}
