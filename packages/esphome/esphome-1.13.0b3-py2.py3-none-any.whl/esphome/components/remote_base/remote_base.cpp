#include "remote_base.h"
#include "esphome/core/log.h"

namespace esphome {
namespace remote_base {

static const char *TAG = "remote_base";

RemoteComponentBase::RemoteComponentBase(GPIOPin *pin) : pin_(pin) {
#ifdef ARDUINO_ARCH_ESP32
  static rmt_channel_t next_rmt_channel = RMT_CHANNEL_0;
  this->channel_ = next_rmt_channel;
  next_rmt_channel = rmt_channel_t(int(next_rmt_channel) + 1);
#endif
}

void RemoteReceiverBinarySensorBase::dump_config() { LOG_BINARY_SENSOR("", "Remote Receiver Binary Sensor", this); }

void RemoteTransmitterBase::send_(uint32_t send_times, uint32_t send_wait) {
#ifdef ESPHOME_LOG_HAS_VERY_VERBOSE
  const std::vector<int32_t> &vec = this->temp_.get_data();
  char buffer[256];
  uint32_t buffer_offset = 0;
  buffer_offset += sprintf(buffer, "Sending times=%u wait=%ums: ", send_times, send_wait);

  for (int32_t i = 0; i < vec.size(); i++) {
    const int32_t value = vec[i];
    const uint32_t remaining_length = sizeof(buffer) - buffer_offset;
    int written;

    if (i + 1 < vec.size()) {
      written = snprintf(buffer + buffer_offset, remaining_length, "%d, ", value);
    } else {
      written = snprintf(buffer + buffer_offset, remaining_length, "%d", value);
    }

    if (written < 0 || written >= int(remaining_length)) {
      // write failed, flush...
      buffer[buffer_offset] = '\0';
      ESP_LOGVV(TAG, "%s", buffer);
      buffer_offset = 0;
      written = sprintf(buffer, "  ");
      if (i + 1 < vec.size()) {
        written += sprintf(buffer + written, "%d, ", value);
      } else {
        written += sprintf(buffer + written, "%d", value);
      }
    }

    buffer_offset += written;
  }
  if (buffer_offset != 0) {
    ESP_LOGVV(TAG, "%s", buffer);
  }
#endif
  this->send_internal(send_times, send_wait);
}
}  // namespace remote_base
}  // namespace esphome
