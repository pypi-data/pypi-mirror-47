#pragma once

#include "esphome/core/component.h"
#include "esphome/components/i2c/i2c.h"
#include "esphome/components/binary_sensor/binary_sensor.h"

namespace esphome {
namespace mpr121 {

enum {
  MPR121_TOUCHSTATUS_L = 0x00,
  MPR121_TOUCHSTATUS_H = 0x01,
  MPR121_FILTDATA_0L = 0x04,
  MPR121_FILTDATA_0H = 0x05,
  MPR121_BASELINE_0 = 0x1E,
  MPR121_MHDR = 0x2B,
  MPR121_NHDR = 0x2C,
  MPR121_NCLR = 0x2D,
  MPR121_FDLR = 0x2E,
  MPR121_MHDF = 0x2F,
  MPR121_NHDF = 0x30,
  MPR121_NCLF = 0x31,
  MPR121_FDLF = 0x32,
  MPR121_NHDT = 0x33,
  MPR121_NCLT = 0x34,
  MPR121_FDLT = 0x35,
  MPR121_TOUCHTH_0 = 0x41,
  MPR121_RELEASETH_0 = 0x42,
  MPR121_DEBOUNCE = 0x5B,
  MPR121_CONFIG1 = 0x5C,
  MPR121_CONFIG2 = 0x5D,
  MPR121_CHARGECURR_0 = 0x5F,
  MPR121_CHARGETIME_1 = 0x6C,
  MPR121_ECR = 0x5E,
  MPR121_AUTOCONFIG0 = 0x7B,
  MPR121_AUTOCONFIG1 = 0x7C,
  MPR121_UPLIMIT = 0x7D,
  MPR121_LOWLIMIT = 0x7E,
  MPR121_TARGETLIMIT = 0x7F,
  MPR121_GPIODIR = 0x76,
  MPR121_GPIOEN = 0x77,
  MPR121_GPIOSET = 0x78,
  MPR121_GPIOCLR = 0x79,
  MPR121_GPIOTOGGLE = 0x7A,
  MPR121_SOFTRESET = 0x80,
};

class MPR121Channel : public binary_sensor::BinarySensor {
 public:
  void set_channel(uint8_t channel) { channel_ = channel; }
  void process(uint16_t data) { this->publish_state(static_cast<bool>(data & (1 << this->channel_))); }

 protected:
  uint8_t channel_{0};
};

class MPR121Component : public Component, public i2c::I2CDevice {
 public:
  void register_channel(MPR121Channel *channel) { this->channels_.push_back(channel); }
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void loop() override;

 protected:
  std::vector<MPR121Channel *> channels_{};
  enum ErrorCode {
    NONE = 0,
    COMMUNICATION_FAILED,
    WRONG_CHIP_STATE,
  } error_code_{NONE};
};

}  // namespace mpr121
}  // namespace esphome
