extends RefCounted


func choose_next_behavior(behaviors: Array, context: Dictionary, rng: RandomNumberGenerator) -> RefCounted:
	var candidates: Array = []
	var total_weight := 0.0
	var previous_behavior_id := String(context.get("previous_behavior_id", ""))

	for behavior in behaviors:
		if behavior.id == previous_behavior_id:
			continue
		if not behavior.can_start(context):
			continue

		var behavior_weight := maxf(0.0, behavior.get_weight(context))
		if behavior_weight <= 0.0:
			continue

		candidates.append(behavior)
		total_weight += behavior_weight

	if candidates.is_empty():
		return _find_fallback_behavior(behaviors, previous_behavior_id)

	var roll := rng.randf_range(0.0, total_weight)
	var cumulative := 0.0

	for behavior in candidates:
		cumulative += maxf(0.0, behavior.get_weight(context))
		if roll <= cumulative:
			return behavior

	return candidates.back()


func _find_fallback_behavior(behaviors: Array, previous_behavior_id: String) -> RefCounted:
	for behavior in behaviors:
		if behavior.id == "sit" and behavior.id != previous_behavior_id:
			return behavior

	for behavior in behaviors:
		if behavior.id != previous_behavior_id:
			return behavior

	return behaviors.front()
