extends Node

const CONFIG_PATH := "res://config/gameplay.cfg"

var core_growth: float = 0.0
var final_growth: float = 0.0
var growth_efficiency: float = 1.0
var growth_per_desktop_second: float = 0.1

var _save_system: Node = null
var _desktop_time_system: Node = null
var _baseline_growth: float = 0.0
var _baseline_desktop_time: float = 0.0
var _save_elapsed := 0.0


func _ready() -> void:
	_load_config()
	_save_system = get_node_or_null("../SaveSystem")
	_desktop_time_system = get_node_or_null("../DesktopTimeSystem")
	if _save_system:
		_baseline_growth = float(_save_system.growth)
		_baseline_desktop_time = float(_save_system.desktop_time)
		core_growth = _baseline_growth
		final_growth = core_growth


func _process(delta: float) -> void:
	_update_growth()
	_save_elapsed += delta
	if _save_elapsed >= 1.0:
		_save_elapsed = 0.0
		_save_runtime_facts()


func get_final_growth() -> float:
	return final_growth


func _update_growth() -> void:
	if _desktop_time_system == null:
		return

	var current_desktop_time: float = _desktop_time_system.get_desktop_time()
	var session_desktop_time := maxf(0.0, current_desktop_time - _baseline_desktop_time)
	core_growth = minf(100.0, _baseline_growth + session_desktop_time * growth_per_desktop_second * growth_efficiency)
	final_growth = core_growth


func _save_runtime_facts() -> void:
	if _save_system == null or _desktop_time_system == null:
		return

	_save_system.set_runtime_facts(final_growth, _desktop_time_system.get_desktop_time())
	_save_system.save_facts()


func _load_config() -> void:
	var config := ConfigFile.new()
	if config.load(CONFIG_PATH) != OK:
		return

	growth_per_desktop_second = float(config.get_value("growth", "speed", growth_per_desktop_second))
	growth_efficiency = float(config.get_value("growth", "efficiency", growth_efficiency))

