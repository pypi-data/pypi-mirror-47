#include "mhz19.h"
#include "esphome/core/log.h"

namespace esphome {
namespace mhz19 {

static const char *TAG = "mhz19";
static const uint8_t MHZ19_REQUEST_LENGTH = 8;
static const uint8_t MHZ19_RESPONSE_LENGTH = 9;
static const uint8_t MHZ19_COMMAND_GET_PPM[] = {0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00};

uint8_t mhz19_checksum(const uint8_t *command) {
  uint8_t sum = 0;
  for (uint8_t i = 1; i < MHZ19_REQUEST_LENGTH; i++) {
    sum += command[i];
  }
  return 0xFF - sum + 0x01;
}

void MHZ19Component::update() {
  uint8_t response[MHZ19_RESPONSE_LENGTH];
  if (!this->mhz19_write_command_(MHZ19_COMMAND_GET_PPM, response)) {
    ESP_LOGW(TAG, "Reading data from MHZ19 failed!");
    this->status_set_warning();
    return;
  }

  if (response[0] != 0xFF || response[1] != 0x86) {
    ESP_LOGW(TAG, "Invalid preamble from MHZ19!");
    this->status_set_warning();
    return;
  }

  uint8_t checksum = mhz19_checksum(response);
  if (response[8] != checksum) {
    ESP_LOGW(TAG, "MHZ19 Checksum doesn't match: 0x%02X!=0x%02X", response[8], checksum);
    this->status_set_warning();
    return;
  }

  this->status_clear_warning();
  const uint16_t ppm = (uint16_t(response[2]) << 8) | response[3];
  const int temp = int(response[4]) - 40;
  const uint8_t status = response[5];

  ESP_LOGD(TAG, "MHZ19 Received CO₂=%uppm Temperature=%d°C Status=0x%02X", ppm, temp, status);
  if (this->co2_sensor_ != nullptr)
    this->co2_sensor_->publish_state(ppm);
  if (this->temperature_sensor_ != nullptr)
    this->temperature_sensor_->publish_state(temp);
}

bool MHZ19Component::mhz19_write_command_(const uint8_t *command, uint8_t *response) {
  this->flush();
  this->write_array(command, MHZ19_REQUEST_LENGTH);
  this->write_byte(mhz19_checksum(command));

  if (response == nullptr)
    return true;

  bool ret = this->read_array(response, MHZ19_RESPONSE_LENGTH);
  this->flush();
  return ret;
}
float MHZ19Component::get_setup_priority() const { return setup_priority::DATA; }
void MHZ19Component::dump_config() {
  ESP_LOGCONFIG(TAG, "MH-Z19:");
  LOG_SENSOR("  ", "CO2", this->co2_sensor_);
  LOG_SENSOR("  ", "Temperature", this->temperature_sensor_);
}

}  // namespace mhz19
}  // namespace esphome
