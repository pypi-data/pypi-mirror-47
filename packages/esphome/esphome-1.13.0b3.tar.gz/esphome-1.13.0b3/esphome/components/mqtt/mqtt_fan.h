#pragma once

#include "esphome/core/defines.h"

#ifdef USE_FAN

#include "esphome/components/fan/fan_state.h"
#include "mqtt_component.h"

namespace esphome {
namespace mqtt {

class MQTTFanComponent : public mqtt::MQTTComponent {
 public:
  explicit MQTTFanComponent(fan::FanState *state);

  MQTT_COMPONENT_CUSTOM_TOPIC(oscillation, command)
  MQTT_COMPONENT_CUSTOM_TOPIC(oscillation, state)
  MQTT_COMPONENT_CUSTOM_TOPIC(speed, command)
  MQTT_COMPONENT_CUSTOM_TOPIC(speed, state)

  void send_discovery(JsonObject &root, mqtt::SendDiscoveryConfig &config) override;

  // ========== INTERNAL METHODS ==========
  // (In most use cases you won't need these)
  /// Setup the fan subscriptions and discovery.
  void setup() override;
  /// Send the full current state to MQTT.
  bool send_initial_state() override;
  bool publish_state();
  /// 'fan' component type for discovery.
  std::string component_type() const override;

  fan::FanState *get_state() const;

  bool is_internal() override;

 protected:
  std::string friendly_name() const override;

  fan::FanState *state_;
};

}  // namespace mqtt
}  // namespace esphome

#endif
