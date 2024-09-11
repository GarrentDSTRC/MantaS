#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <boost/asio.hpp>
#include <boost/crc.hpp>
#include <thread>
#include <chrono>
#include <map>

using namespace std;
using namespace boost::asio;

// CRC16校验函数
uint16_t modbus_crc16(const vector<uint8_t>& data) {
    boost::crc_optimal<16, 0x8005, 0xFFFF, 0, false, false> crc;
    crc.process_bytes(data.data(), data.size());
    return crc.checksum();
}

// 构建Modbus RTU请求包
vector<uint8_t> build_request(uint8_t address, uint8_t function_code, uint16_t start_register, uint16_t quantity) {
    vector<uint8_t> data = { address, function_code, static_cast<uint8_t>(start_register >> 8), static_cast<uint8_t>(start_register & 0xFF), static_cast<uint8_t>(quantity >> 8), static_cast<uint8_t>(quantity & 0xFF) };
    uint16_t crc = modbus_crc16(data);
    data.push_back(static_cast<uint8_t>(crc & 0xFF));
    data.push_back(static_cast<uint8_t>(crc >> 8));
    return data;
}

// 发送请求并接收响应
vector<uint8_t> send_request(serial_port& ser, const vector<uint8_t>& request) {
    write(ser, buffer(request));
    std::this_thread::sleep_for(std::chrono::milliseconds(100));  // 等待响应
    vector<uint8_t> response(256);
    size_t len = read(ser, buffer(response));
    response.resize(len);
    return response;
}

// 解析响应数据
bool parse_response(const vector<uint8_t>& response, uint8_t& device_address, uint8_t& function_code, vector<uint8_t>& register_values, uint16_t& crc_received) {
    if (response.size() < 5) {
        cerr << "Response too short" << endl;
        return false;
    }
    device_address = response[0];
    function_code = response[1];
    uint8_t byte_count = response[2];
    register_values.assign(response.begin() + 3, response.begin() + 3 + byte_count);
    crc_received = response[response.size() - 2] | (response[response.size() - 1] << 8);
    return true;
}

// 验证CRC校验码
bool verify_crc(const vector<uint8_t>& data) {
    uint16_t calculated_crc = modbus_crc16(vector<uint8_t>(data.begin(), data.end() - 2));
    uint16_t crc_from_response = data[data.size() - 2] | (data[data.size() - 1] << 8);
    return calculated_crc == crc_from_response;
}

// 读取寄存器值
int16_t read_register(serial_port& ser, uint8_t address, uint16_t start_register, uint8_t function_code = 0x03) {
    uint16_t quantity = 1;
    vector<uint8_t> request = build_request(address, function_code, start_register, quantity);
    vector<uint8_t> response = send_request(ser, request);
    if (response.empty()) {
        cerr << "No response received" << endl;
        return 0;
    }
    if (!verify_crc(response)) {
        cerr << "CRC check failed" << endl;
        return 0;
    }
    uint8_t device_address, function_code_received;
    vector<uint8_t> register_values;
    uint16_t crc_received;
    if (!parse_response(response, device_address, function_code_received, register_values, crc_received)) {
        cerr << "Failed to parse response" << endl;
        return 0;
    }
    if (register_values.size() != 2) {
        cerr << "Unexpected register value length: " << register_values.size() << endl;
        return 0;
    }
    return static_cast<int16_t>((register_values[0] << 8) | register_values[1]);
}

// 解析继电器状态
void parse_relay_status(uint16_t relay_status) {
    cout << "继电器状态: " << endl;
    cout << "  正极继电器: " << ((relay_status & 0x01) != 0) << endl;
    cout << "  负极继电器: " << ((relay_status & 0x02) != 0) << endl;
    cout << "  充电继电器: " << ((relay_status & 0x04) != 0) << endl;
    cout << "  放电继电器: " << ((relay_status & 0x08) != 0) << endl;
    cout << "  预充继电器: " << ((relay_status & 0x10) != 0) << endl;
    cout << "  加热继电器: " << ((relay_status & 0x20) != 0) << endl;
}

// 解析电压值
float parse_voltage(int16_t voltage_raw) {
    return voltage_raw * 0.1f;  // 分辨率是0.1V/bit
}

// 解析电流值
float parse_current(int16_t current_raw) {
    return current_raw * 0.1f - 1500.0f;  // 分辨率是0.1A/bit，偏移量是-1500A
}

// 解析SOC值
float get_soc_percentage(int16_t raw_soc) {
    return raw_soc * 0.1f;  // 分辨率是0.1%/bit
}

// 根据电流值返回状态
string get_current_status(int16_t current) {
    if (current >= 3000) {
        return "放电状态 (0x01)";
    } else if (current <= -3000) {
        return "充电状态 (0x02)";
    } else if (current > -3000 && current < 3000) {
        return "搁置状态 (0x03)";
    }
    return "未知状态";
}

int main() {
    try {
        io_service io;
        serial_port ser(io, "/dev/ttyUSB0");  // 根据实际情况调整串行端口
        ser.set_option(serial_port_base::baud_rate(9600));
        ser.set_option(serial_port_base::character_size(8));
        ser.set_option(serial_port_base::parity(serial_port_base::parity::none));
        ser.set_option(serial_port_base::stop_bits(serial_port_base::stop_bits::one));
        cout << "打开串口成功"<< endl;

        map<string, uint16_t> register_map = {
            {"继电器状态", 0x0001},
            {"总电压", 0x0002},
            {"正半簇电流", 0x0003},
            {"负半簇电流", 0x0004},
            {"系统工作状态", 0x0005},
            {"SOC", 0x0006},
            {"SOH", 0x0007}
        };

        uint8_t address = 0x01;
        while (true) {
            int16_t relay_status = read_register(ser, address, register_map["继电器状态"]);
            int16_t total_voltage = read_register(ser, address, register_map["总电压"]);
            int16_t positive_current = read_register(ser, address, register_map["正半簇电流"]);
            int16_t negative_current = read_register(ser, address, register_map["负半簇电流"]);
            int16_t work_status = read_register(ser, address, register_map["系统工作状态"]);
            int16_t soc = read_register(ser, address, register_map["SOC"]);
            int16_t soh = read_register(ser, address, register_map["SOH"]);

            if (relay_status) parse_relay_status(relay_status);
            if (total_voltage) cout << "总电压: " << parse_voltage(total_voltage) << "V" << endl;
            if (positive_current) cout << "正半簇电流: " << parse_current(positive_current) << "A" << endl;
            if (negative_current) cout << "负半簇电流: " << parse_current(negative_current) << "A" << endl;
            if (work_status) cout << "系统工作状态: " << work_status << " (" << get_current_status(work_status) << ")" << endl;
            if (soc) cout << "SOC: " << get_soc_percentage(soc) << "%" << endl;
            if (soh) cout << "SOH: " << get_soc_percentage(soh) << "%" << endl;

            std::this_thread::sleep_for(std::chrono::seconds(1));
        }

    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
    }

    return 0;
}
