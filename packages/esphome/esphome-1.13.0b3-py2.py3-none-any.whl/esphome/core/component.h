#pragma once

#include <string>
#include <functional>
#include <vector>

#include "esphome/core/optional.h"

namespace esphome {

/** Default setup priorities for components of different types.
 *
 * Components should return one of these setup priorities in get_setup_priority.
 */
namespace setup_priority {

/// For communication buses like i2c/spi
extern const float BUS;
/// For components that represent GPIO pins like PCF8573
extern const float IO;
/// For components that deal with hardware and are very important like GPIO switch
extern const float HARDWARE;
/// For components that import data from directly connected sensors like DHT.
extern const float DATA;
/// Alias for DATA (here for compatability reasons)
extern const float HARDWARE_LATE;
/// For components that use data from sensors like displays
extern const float PROCESSOR;
extern const float WIFI;
/// For components that should be initialized after WiFi is connected.
extern const float AFTER_WIFI;
/// For components that should be initialized after a data connection (API/MQTT) is connected.
extern const float AFTER_CONNECTION;
/// For components that should be initialized at the very end of the setup process.
extern const float LATE;

}  // namespace setup_priority

#define LOG_UPDATE_INTERVAL(this) \
  if (this->get_update_interval() < 100) { \
    ESP_LOGCONFIG(TAG, "  Update Interval: %.3fs", this->get_update_interval() / 1000.0f); \
  } else { \
    ESP_LOGCONFIG(TAG, "  Update Interval: %.1fs", this->get_update_interval() / 1000.0f); \
  }

extern const uint32_t COMPONENT_STATE_MASK;
extern const uint32_t COMPONENT_STATE_CONSTRUCTION;
extern const uint32_t COMPONENT_STATE_SETUP;
extern const uint32_t COMPONENT_STATE_LOOP;
extern const uint32_t COMPONENT_STATE_FAILED;
extern const uint32_t STATUS_LED_MASK;
extern const uint32_t STATUS_LED_OK;
extern const uint32_t STATUS_LED_WARNING;
extern const uint32_t STATUS_LED_ERROR;

class Component {
 public:
  /** Where the component's initialization should happen.
   *
   * Analogous to Arduino's setup(). This method is guaranteed to only be called once.
   * Defaults to doing nothing.
   */
  virtual void setup();

  /** This method will be called repeatedly.
   *
   * Analogous to Arduino's loop(). setup() is guaranteed to be called before this.
   * Defaults to doing nothing.
   */
  virtual void loop();

  virtual void dump_config();

  /** priority of setup(). higher -> executed earlier
   *
   * Defaults to 0.
   *
   * @return The setup priority of this component
   */
  virtual float get_setup_priority() const;

  float get_actual_setup_priority() const;

  void set_setup_priority(float priority);

  /** priority of loop(). higher -> executed earlier
   *
   * Defaults to 0.
   *
   * @return The loop priority of this component
   */
  virtual float get_loop_priority() const;

  /** Public loop() functions. These will be called by the Application instance.
   *
   * Note: This should normally not be overriden, unless you know what you're doing.
   * They're basically to make creating custom components easier. For example the
   * SensorComponent can override these methods to not have the user call some super
   * methods within their custom sensors. These methods should ALWAYS call the loop_internal()
   * and setup_internal() methods.
   *
   * Basically, it handles stuff like interval/timeout functions and eventually calls loop().
   */
  virtual void call_loop();
  virtual void call_setup();

  virtual void on_shutdown() {}
  virtual void on_safe_shutdown() {}

  uint32_t get_component_state() const;

  /** Mark this component as failed. Any future timeouts/intervals/setup/loop will no longer be called.
   *
   * This might be useful if a component wants to indicate that a connection to its peripheral failed.
   * For example, i2c based components can check if the remote device is responding and otherwise
   * mark the component as failed. Eventually this will also enable smart status LEDs.
   */
  virtual void mark_failed();

  bool is_failed();

  virtual bool can_proceed();

  bool status_has_warning();

  bool status_has_error();

  void status_set_warning();

  void status_set_error();

  void status_clear_warning();

  void status_clear_error();

  void status_momentary_warning(const std::string &name, uint32_t length = 5000);

  void status_momentary_error(const std::string &name, uint32_t length = 5000);

 protected:
  /** Set an interval function with a unique name. Empty name means no cancelling possible.
   *
   * This will call f every interval ms. Can be cancelled via CancelInterval().
   * Similar to javascript's setInterval().
   *
   * IMPORTANT: Do not rely on this having correct timing. This is only called from
   * loop() and therefore can be significantly delay. If you need exact timing please
   * use hardware timers.
   *
   * @param name The identifier for this interval function.
   * @param interval The interval in ms.
   * @param f The function (or lambda) that should be called
   *
   * @see cancel_interval()
   */
  void set_interval(const std::string &name, uint32_t interval, std::function<void()> &&f);  // NOLINT

  void set_interval(uint32_t interval, std::function<void()> &&f);  // NOLINT

  /** Cancel an interval function.
   *
   * @param name The identifier for this interval function.
   * @return Whether an interval functions was deleted.
   */
  bool cancel_interval(const std::string &name);  // NOLINT

  void set_timeout(uint32_t timeout, std::function<void()> &&f);  // NOLINT

  /** Set a timeout function with a unique name.
   *
   * Similar to javascript's setTimeout(). Empty name means no cancelling possible.
   *
   * IMPORTANT: Do not rely on this having correct timing. This is only called from
   * loop() and therefore can be significantly delay. If you need exact timing please
   * use hardware timers.
   *
   * @param name The identifier for this timeout function.
   * @param timeout The timeout in ms.
   * @param f The function (or lambda) that should be called
   *
   * @see cancel_timeout()
   */
  void set_timeout(const std::string &name, uint32_t timeout, std::function<void()> &&f);  // NOLINT

  /** Cancel a timeout function.
   *
   * @param name The identifier for this timeout function.
   * @return Whether a timeout functions was deleted.
   */
  bool cancel_timeout(const std::string &name);  // NOLINT

  /** Defer a callback to the next loop() call.
   *
   * If name is specified and a defer() object with the same name exists, the old one is first removed.
   *
   * @param name The name of the defer function.
   * @param f The callback.
   */
  void defer(const std::string &name, std::function<void()> &&f);  // NOLINT

  /// Defer a callback to the next loop() call.
  void defer(std::function<void()> &&f);  // NOLINT

  /// Cancel a defer callback using the specified name, name must not be empty.
  bool cancel_defer(const std::string &name);  // NOLINT

  void loop_internal_();
  void setup_internal_();

  /// Internal struct for storing timeout/interval functions.
  struct TimeFunction {
    std::string name;                             ///< The name/id of this TimeFunction.
    enum Type { TIMEOUT, INTERVAL, DEFER } type;  ///< The type of this TimeFunction. Either TIMEOUT, INTERVAL or DEFER.
    uint32_t interval;                            ///< The interval/timeout of this function.
    /// The last execution for interval functions and the time, SetInterval was called, for timeout functions.
    uint32_t last_execution;
    std::function<void()> f;  ///< The function (or callback) itself.
    bool remove;

    bool should_run(uint32_t now) const;
  };

  /// Cancel an only time function. If name is empty, won't do anything.
  bool cancel_time_function_(const std::string &name, TimeFunction::Type type);

  /** Storage for interval/timeout functions.
   *
   * Intentionally a vector despite its map-like nature, because of the
   * memory overhead.
   */
  std::vector<TimeFunction> time_functions_;

  uint32_t component_state_{0x0000};  ///< State of this component.
  optional<float> setup_priority_override_;
};

/** This class simplifies creating components that periodically check a state.
 *
 * You basically just need to implement the update() function, it will be called every update_interval ms
 * after startup. Note that this class cannot guarantee a correct timing, as it's not using timers, just
 * a software polling feature with set_interval() from Component.
 */
class PollingComponent : public Component {
 public:
  PollingComponent() : PollingComponent(0) {}

  /** Initialize this polling component with the given update interval in ms.
   *
   * @param update_interval The update interval in ms.
   */
  explicit PollingComponent(uint32_t update_interval);

  /** Manually set the update interval in ms for this polling object.
   *
   * Override this if you want to do some validation for the update interval.
   *
   * @param update_interval The update interval in ms.
   */
  virtual void set_update_interval(uint32_t update_interval);

  // ========== OVERRIDE METHODS ==========
  // (You'll only need this when creating your own custom sensor)
  virtual void update() = 0;

  // ========== INTERNAL METHODS ==========
  // (In most use cases you won't need these)
  void call_setup() override;

  /// Get the update interval in ms of this sensor
  virtual uint32_t get_update_interval() const;

 protected:
  uint32_t update_interval_;
};

/// Helper class that enables naming of objects so that it doesn't have to be re-implement every time.
class Nameable {
 public:
  Nameable() : Nameable("") {}
  explicit Nameable(const std::string &name);
  const std::string &get_name() const;
  void set_name(const std::string &name);
  /// Get the sanitized name of this nameable as an ID. Caching it internally.
  const std::string &get_object_id();
  uint32_t get_object_id_hash();

  bool is_internal() const;
  void set_internal(bool internal);

 protected:
  virtual uint32_t hash_base() = 0;

  void calc_object_id_();

  std::string name_;
  std::string object_id_;
  uint32_t object_id_hash_;
  bool internal_{false};
};

}  // namespace esphome
