extends Node

var desktop_time: float = 0.0
var _save_system: Node = null


func _ready() -> void:
	_save_system = get_node_or_null("../SaveSystem")
	if _save_system:
		desktop_time = float(_save_system.desktop_time)


func _process(delta: float) -> void:
	desktop_time += maxf(0.0, delta)


func get_desktop_time() -> float:
	return desktop_time

