extends Node

signal interaction_requested(type: String, position: Vector2, target: String)

var _cat_layer: Node2D = null


func _ready() -> void:
	_cat_layer = get_node_or_null("../CatLayer")


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		if _cat_layer and _is_click_on_cat(event.position):
			interaction_requested.emit("pet", event.position, "cat")


func _is_click_on_cat(click_position: Vector2) -> bool:
	if not _cat_layer.has_method("get_current_sprite_rect"):
		return false
	var sprite_rect: Rect2 = _cat_layer.get_current_sprite_rect()
	return sprite_rect.has_point(click_position)
