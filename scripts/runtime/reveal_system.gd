extends Node

const TOTAL_REGIONS := 8
const FIRST_THRESHOLD := 3.0
const LAST_THRESHOLD := 95.0

const REGION_ORDER := [2, 0, 1, 3, 7, 4, 5, 6]
const REGION_COLORS := [
	Color(0.85, 0.60, 0.35),
	Color(0.78, 0.62, 0.44),
	Color(0.90, 0.75, 0.48),
	Color(0.68, 0.48, 0.32),
	Color(0.92, 0.82, 0.62),
	Color(0.72, 0.54, 0.38),
	Color(0.80, 0.55, 0.30),
	Color(0.88, 0.70, 0.50),
]

var reveal_percentage: float = 0.0
var _growth_system: Node = null


func _ready() -> void:
	_growth_system = get_node_or_null("../GrowthSystem")


func _process(_delta: float) -> void:
	if _growth_system:
		var raw_growth: float = _growth_system.get_final_growth()
		reveal_percentage = _apply_progression_curve(raw_growth)


func get_region_alpha(region_idx: int) -> float:
	var order_pos := REGION_ORDER.find(region_idx)
	if order_pos == -1:
		return 0.0

	var threshold := _get_region_threshold(order_pos)
	if reveal_percentage < threshold:
		return 0.0

	var span := LAST_THRESHOLD - threshold
	if span <= 0.0:
		return 1.0

	return clampf((reveal_percentage - threshold) / span, 0.0, 1.0)


func get_region_color(region_idx: int) -> Color:
	if region_idx < 0 or region_idx >= REGION_COLORS.size():
		return Color.WHITE
	return REGION_COLORS[region_idx]


func get_reveal_percentage() -> float:
	return reveal_percentage


func _get_region_threshold(order_pos: int) -> float:
	return FIRST_THRESHOLD + (float(order_pos) / float(TOTAL_REGIONS - 1)) * (LAST_THRESHOLD - FIRST_THRESHOLD)


func _apply_progression_curve(raw_growth: float) -> float:
	var t := clampf(raw_growth / 100.0, 0.0, 1.0)
	return smoothstep(0.0, 1.0, t) * 100.0
