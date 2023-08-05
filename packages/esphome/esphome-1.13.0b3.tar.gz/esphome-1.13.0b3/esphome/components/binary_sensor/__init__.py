import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation, core
from esphome.automation import Condition, maybe_simple_id
from esphome.components import mqtt
from esphome.const import CONF_DEVICE_CLASS, CONF_FILTERS, \
    CONF_ID, CONF_INTERNAL, CONF_INVALID_COOLDOWN, CONF_INVERTED, \
    CONF_MAX_LENGTH, CONF_MIN_LENGTH, CONF_ON_CLICK, \
    CONF_ON_DOUBLE_CLICK, CONF_ON_MULTI_CLICK, CONF_ON_PRESS, CONF_ON_RELEASE, CONF_ON_STATE, \
    CONF_STATE, CONF_TIMING, CONF_TRIGGER_ID, CONF_FOR, CONF_NAME, CONF_MQTT_ID
from esphome.core import CORE, coroutine, coroutine_with_priority
from esphome.py_compat import string_types
from esphome.util import Registry

DEVICE_CLASSES = [
    '', 'battery', 'cold', 'connectivity', 'door', 'garage_door', 'gas',
    'heat', 'light', 'lock', 'moisture', 'motion', 'moving', 'occupancy',
    'opening', 'plug', 'power', 'presence', 'problem', 'safety', 'smoke',
    'sound', 'vibration', 'window'
]

IS_PLATFORM_COMPONENT = True

binary_sensor_ns = cg.esphome_ns.namespace('binary_sensor')
BinarySensor = binary_sensor_ns.class_('BinarySensor', cg.Nameable)
BinarySensorPtr = BinarySensor.operator('ptr')

# Triggers
PressTrigger = binary_sensor_ns.class_('PressTrigger', automation.Trigger.template())
ReleaseTrigger = binary_sensor_ns.class_('ReleaseTrigger', automation.Trigger.template())
ClickTrigger = binary_sensor_ns.class_('ClickTrigger', automation.Trigger.template())
DoubleClickTrigger = binary_sensor_ns.class_('DoubleClickTrigger', automation.Trigger.template())
MultiClickTrigger = binary_sensor_ns.class_('MultiClickTrigger', automation.Trigger.template(),
                                            cg.Component)
MultiClickTriggerEvent = binary_sensor_ns.struct('MultiClickTriggerEvent')
StateTrigger = binary_sensor_ns.class_('StateTrigger', automation.Trigger.template(bool))
BinarySensorPublishAction = binary_sensor_ns.class_('BinarySensorPublishAction', automation.Action)

# Condition
BinarySensorCondition = binary_sensor_ns.class_('BinarySensorCondition', Condition)

# Filters
Filter = binary_sensor_ns.class_('Filter')
DelayedOnFilter = binary_sensor_ns.class_('DelayedOnFilter', Filter, cg.Component)
DelayedOffFilter = binary_sensor_ns.class_('DelayedOffFilter', Filter, cg.Component)
InvertFilter = binary_sensor_ns.class_('InvertFilter', Filter)
LambdaFilter = binary_sensor_ns.class_('LambdaFilter', Filter)

FILTER_REGISTRY = Registry()
validate_filters = cv.validate_registry('filter', FILTER_REGISTRY)


@FILTER_REGISTRY.register('invert', InvertFilter, {})
def invert_filter_to_code(config, filter_id):
    yield cg.new_Pvariable(filter_id)


@FILTER_REGISTRY.register('delayed_on', DelayedOnFilter,
                          cv.positive_time_period_milliseconds)
def delayed_on_filter_to_code(config, filter_id):
    var = cg.new_Pvariable(filter_id, config)
    yield cg.register_component(var, {})
    yield var


@FILTER_REGISTRY.register('delayed_off', DelayedOffFilter, cv.positive_time_period_milliseconds)
def delayed_off_filter_to_code(config, filter_id):
    var = cg.new_Pvariable(filter_id, config)
    yield cg.register_component(var, {})
    yield var


@FILTER_REGISTRY.register('lambda', LambdaFilter, cv.returning_lambda)
def lambda_filter_to_code(config, filter_id):
    lambda_ = yield cg.process_lambda(config, [(bool, 'x')], return_type=cg.optional.template(bool))
    yield cg.new_Pvariable(filter_id, lambda_)


MULTI_CLICK_TIMING_SCHEMA = cv.Schema({
    cv.Optional(CONF_STATE): cv.boolean,
    cv.Optional(CONF_MIN_LENGTH): cv.positive_time_period_milliseconds,
    cv.Optional(CONF_MAX_LENGTH): cv.positive_time_period_milliseconds,
})


def parse_multi_click_timing_str(value):
    if not isinstance(value, string_types):
        return value

    parts = value.lower().split(' ')
    if len(parts) != 5:
        raise cv.Invalid("Multi click timing grammar consists of exactly 5 words, not {}"
                         "".format(len(parts)))
    try:
        state = cv.boolean(parts[0])
    except cv.Invalid:
        raise cv.Invalid(u"First word must either be ON or OFF, not {}".format(parts[0]))

    if parts[1] != 'for':
        raise cv.Invalid(u"Second word must be 'for', got {}".format(parts[1]))

    if parts[2] == 'at':
        if parts[3] == 'least':
            key = CONF_MIN_LENGTH
        elif parts[3] == 'most':
            key = CONF_MAX_LENGTH
        else:
            raise cv.Invalid(u"Third word after at must either be 'least' or 'most', got {}"
                             u"".format(parts[3]))
        try:
            length = cv.positive_time_period_milliseconds(parts[4])
        except cv.Invalid as err:
            raise cv.Invalid(u"Multi Click Grammar Parsing length failed: {}".format(err))
        return {
            CONF_STATE: state,
            key: str(length)
        }

    if parts[3] != 'to':
        raise cv.Invalid("Multi click grammar: 4th word must be 'to'")

    try:
        min_length = cv.positive_time_period_milliseconds(parts[2])
    except cv.Invalid as err:
        raise cv.Invalid(u"Multi Click Grammar Parsing minimum length failed: {}".format(err))

    try:
        max_length = cv.positive_time_period_milliseconds(parts[4])
    except cv.Invalid as err:
        raise cv.Invalid(u"Multi Click Grammar Parsing minimum length failed: {}".format(err))

    return {
        CONF_STATE: state,
        CONF_MIN_LENGTH: str(min_length),
        CONF_MAX_LENGTH: str(max_length)
    }


def validate_multi_click_timing(value):
    if not isinstance(value, list):
        raise cv.Invalid("Timing option must be a *list* of times!")
    timings = []
    state = None
    for i, v_ in enumerate(value):
        v_ = MULTI_CLICK_TIMING_SCHEMA(v_)
        min_length = v_.get(CONF_MIN_LENGTH)
        max_length = v_.get(CONF_MAX_LENGTH)
        if min_length is None and max_length is None:
            raise cv.Invalid("At least one of min_length and max_length is required!")
        if min_length is None and max_length is not None:
            min_length = core.TimePeriodMilliseconds(milliseconds=0)

        new_state = v_.get(CONF_STATE, not state)
        if new_state == state:
            raise cv.Invalid("Timings must have alternating state. Indices {} and {} have "
                             "the same state {}".format(i, i + 1, state))
        if max_length is not None and max_length < min_length:
            raise cv.Invalid("Max length ({}) must be larger than min length ({})."
                             "".format(max_length, min_length))

        state = new_state
        tim = {
            CONF_STATE: new_state,
            CONF_MIN_LENGTH: min_length,
        }
        if max_length is not None:
            tim[CONF_MAX_LENGTH] = max_length
        timings.append(tim)
    return timings


device_class = cv.one_of(*DEVICE_CLASSES, lower=True, space='_')

BINARY_SENSOR_SCHEMA = cv.MQTT_COMPONENT_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(BinarySensor),
    cv.OnlyWith(CONF_MQTT_ID, 'mqtt'): cv.declare_id(mqtt.MQTTBinarySensorComponent),

    cv.Optional(CONF_DEVICE_CLASS): device_class,
    cv.Optional(CONF_FILTERS): validate_filters,
    cv.Optional(CONF_ON_PRESS): automation.validate_automation({
        cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(PressTrigger),
    }),
    cv.Optional(CONF_ON_RELEASE): automation.validate_automation({
        cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(ReleaseTrigger),
    }),
    cv.Optional(CONF_ON_CLICK): automation.validate_automation({
        cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(ClickTrigger),
        cv.Optional(CONF_MIN_LENGTH, default='50ms'): cv.positive_time_period_milliseconds,
        cv.Optional(CONF_MAX_LENGTH, default='350ms'): cv.positive_time_period_milliseconds,
    }),
    cv.Optional(CONF_ON_DOUBLE_CLICK): automation.validate_automation({
        cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(DoubleClickTrigger),
        cv.Optional(CONF_MIN_LENGTH, default='50ms'): cv.positive_time_period_milliseconds,
        cv.Optional(CONF_MAX_LENGTH, default='350ms'): cv.positive_time_period_milliseconds,
    }),
    cv.Optional(CONF_ON_MULTI_CLICK): automation.validate_automation({
        cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(MultiClickTrigger),
        cv.Required(CONF_TIMING): cv.All([parse_multi_click_timing_str],
                                         validate_multi_click_timing),
        cv.Optional(CONF_INVALID_COOLDOWN, default='1s'): cv.positive_time_period_milliseconds,
    }),
    cv.Optional(CONF_ON_STATE): automation.validate_automation({
        cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(StateTrigger),
    }),

    cv.Optional(CONF_INVERTED): cv.invalid(
        "The inverted binary_sensor property has been replaced by the "
        "new 'invert' binary  sensor filter. Please see "
        "https://esphome.io/components/binary_sensor/index.html."
    ),
})


@coroutine
def setup_binary_sensor_core_(var, config):
    cg.add(var.set_name(config[CONF_NAME]))
    if CONF_INTERNAL in config:
        cg.add(var.set_internal(CONF_INTERNAL))
    if CONF_DEVICE_CLASS in config:
        cg.add(var.set_device_class(config[CONF_DEVICE_CLASS]))
    if CONF_INVERTED in config:
        cg.add(var.set_inverted(config[CONF_INVERTED]))
    if CONF_FILTERS in config:
        filters = yield cg.build_registry_list(FILTER_REGISTRY, config[CONF_FILTERS])
        cg.add(var.add_filters(filters))

    for conf in config.get(CONF_ON_PRESS, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        yield automation.build_automation(trigger, [], conf)

    for conf in config.get(CONF_ON_RELEASE, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        yield automation.build_automation(trigger, [], conf)

    for conf in config.get(CONF_ON_CLICK, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var,
                                   conf[CONF_MIN_LENGTH], conf[CONF_MAX_LENGTH])
        yield automation.build_automation(trigger, [], conf)

    for conf in config.get(CONF_ON_DOUBLE_CLICK, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var,
                                   conf[CONF_MIN_LENGTH], conf[CONF_MAX_LENGTH])
        yield automation.build_automation(trigger, [], conf)

    for conf in config.get(CONF_ON_MULTI_CLICK, []):
        timings = []
        for tim in conf[CONF_TIMING]:
            timings.append(cg.StructInitializer(
                MultiClickTriggerEvent,
                ('state', tim[CONF_STATE]),
                ('min_length', tim[CONF_MIN_LENGTH]),
                ('max_length', tim.get(CONF_MAX_LENGTH, 4294967294)),
            ))
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var, timings)
        if CONF_INVALID_COOLDOWN in conf:
            cg.add(trigger.set_invalid_cooldown(conf[CONF_INVALID_COOLDOWN]))
        yield cg.register_component(trigger, conf)
        yield automation.build_automation(trigger, [], conf)

    for conf in config.get(CONF_ON_STATE, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        yield automation.build_automation(trigger, [(bool, 'x')], conf)

    if CONF_MQTT_ID in config:
        mqtt_ = cg.new_Pvariable(config[CONF_MQTT_ID], var)
        yield mqtt.register_mqtt_component(mqtt_, config)


@coroutine
def register_binary_sensor(var, config):
    if not CORE.has_id(config[CONF_ID]):
        var = cg.Pvariable(config[CONF_ID], var)
    cg.add(cg.App.register_binary_sensor(var))
    yield setup_binary_sensor_core_(var, config)


@coroutine
def new_binary_sensor(config):
    var = cg.new_Pvariable(config[CONF_ID], config[CONF_NAME])
    yield register_binary_sensor(var, config)
    yield var


BINARY_SENSOR_CONDITION_SCHEMA = maybe_simple_id({
    cv.Required(CONF_ID): cv.use_id(BinarySensor),
    cv.Optional(CONF_FOR): cv.invalid("This option has been removed in 1.13, please use the "
                                      "'for' condition instead."),
})


@automation.register_condition('binary_sensor.is_on', BinarySensorCondition,
                               BINARY_SENSOR_CONDITION_SCHEMA)
def binary_sensor_is_on_to_code(config, condition_id, template_arg, args):
    paren = yield cg.get_variable(config[CONF_ID])
    yield cg.new_Pvariable(condition_id, template_arg, paren, True)


@automation.register_condition('binary_sensor.is_off', BinarySensorCondition,
                               BINARY_SENSOR_CONDITION_SCHEMA)
def binary_sensor_is_off_to_code(config, condition_id, template_arg, args):
    paren = yield cg.get_variable(config[CONF_ID])
    yield cg.new_Pvariable(condition_id, template_arg, paren, False)


@coroutine_with_priority(100.0)
def to_code(config):
    cg.add_define('USE_BINARY_SENSOR')
    cg.add_global(binary_sensor_ns.using)
