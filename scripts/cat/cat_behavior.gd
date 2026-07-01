class_name CatBehavior
extends RefCounted

var id := ""
var title := ""
var min_duration := 1.0
var max_duration := 1.0
var min_pause := 1.0
var max_pause := 1.0
var weight := 1.0


func _init(behavior_id: String, behavior_title: String) -> void:
	id = behavior_id
	title = behavior_title


func configure(config: ConfigFile) -> void:
	min_duration = float(config.get_value(id, "min_duration", min_duration))
	max_duration = float(config.get_value(id, "max_duration", max_duration))
	min_pause = float(config.get_value(id, "min_pause", min_pause))
	max_pause = float(config.get_value(id, "max_pause", max_pause))
	weight = float(config.get_value(id, "weight", weight))


func get_weight(_context: Dictionary) -> float:
	return weight


func can_start(_context: Dictionary) -> bool:
	return true


func sample_duration(rng: RandomNumberGenerator) -> float:
	return rng.randf_range(min_duration, max_duration)


func sample_pause(rng: RandomNumberGenerator) -> float:
	return rng.randf_range(min_pause, max_pause)
