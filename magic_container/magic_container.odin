package magic_container

MContainer :: struct ($T : typeid) {
    data_index : [dynamic]int,
    id : [dynamic]int,
	trackers : [dynamic]int,
	free_ids : [dynamic]int,
    data : [dynamic]T,
}

Tracked_id :: struct ($T : typeid) {
	mc : ^MContainer(T),
	id : int,
	valid : bool,
}

Untracked_id :: struct ($T : typeid) {
	mc : ^MContainer(T),
	id : int,
}

Multi_tracker :: struct ($T : typeid) {
	mc : ^MContainer(T),
	ids : [dynamic]int,
	valid : [dynamic]bool,
}

build :: proc ($T : typeid, cap := 0) -> ^MContainer(T) {
	mc := new(MContainer(T))
	mc.data_index = make([dynamic]int, 0, cap)
	mc.id = make([dynamic]int, 0, cap)
	mc.trackers = make([dynamic]int, 0, cap)
	mc.free_ids = make([dynamic]int, 0, cap)
	mc.data = make([dynamic]T, 0, cap)
	return mc
}

destroy :: proc {destroy_mcontainer, destroy_tracked_id, destroy_multitracker}

destroy_mcontainer :: proc (mc : ^MContainer($T)) {
    delete(mc.data_index)
    delete(mc.id)
	delete(mc.trackers)
	delete(mc.free_ids)
    delete(mc.data)
    free(mc)
}

make_tracked_id :: proc (mc : ^MContainer($T), id : int) -> Tracked_id(T) {
	assert(id >= 0 && id < len(mc.data_index))
	new_id : Tracked_id(T)
	new_id.mc = mc
	new_id.id = id
	new_id.valid = mc.data_index[id] != -1
	if new_id.valid {
		mc.trackers[id] += 1
	}
	return new_id
}

make_tracked_id_from_index :: proc (mc : ^MContainer($T), index : int) -> Tracked_id(T) {
	return make_tracked_id(mc, mc.id[index])
}

make_untracked_id :: proc (mc : ^MContainer($T), id : int) -> Untracked_id(T) {
	return Untracked_id(T){mc, id}
}

make_untracked_id_from_index :: proc (mc : ^MContainer($T), index : int) -> Untracked_id(T) {
	return Untracked_id(T){mc, mc.id[index]}
}

make_tracked_from_untracked_id :: proc (id : Untracked_id($T)) -> Tracked_id(T) {
	return make_tracked_id(id.mc, id.id)
}

get_untracked_from_tracked_id :: proc (id : Tracked_id($T)) -> Untracked_id(T) {
	// better not to destroy the id just in case the caller wants to keep it
	// destroy_tracked_id(id)
	return make_untracked_id(id.mc, id.id)
}

destroy_tracked_id :: proc (id : ^Tracked_id($T)) {
	if id.valid {
		// forget(id.mc, id.id)
		assert(id.mc.trackers[id.id] > 0)
		id.mc.trackers[id.id] -= 1
		if id.mc.trackers[id.id] == 0 && id.mc.data_index[id.id] == -1 {
			append(&id.mc.free_ids, id.id)
		}
		id.valid = false
	}
}

make_multitracker :: proc (mc : ^MContainer($T)) -> ^Multi_tracker(T) {
	mt := new(Multi_tracker(T))
	mt.mc = mc
	mt.ids = make([dynamic]int)
	mt.valid = make([dynamic]bool)
	return mt
}

destroy_multitracker :: proc (mt : ^Multi_tracker($T)) {
	for valid, i in mt.valid {
		if valid {
			id := mt.ids[i]
			assert(mt.mc.trackers[id] > 0)
			mt.mc.trackers[id] -= 1
			if mt.mc.trackers[id] == 0 && mt.mc.data_index[id] == -1 {
				append(&mt.mc.free_ids, id)
			}
		}
	}
	delete(mt.valid)
	delete(mt.ids)
	free(mt)
}

add_id_to_multitracker :: proc (mt : ^Multi_tracker($T), id : int) {
	assert(id >= 0 && id < len(mt.mc.data_index) && mt.mc.data_index[id] != -1)
	//deduplicate
	for id_ in mt.ids {
		if id_ == id {
			return
		}
	}
	valid := mt.mc.data_index[id] != -1
	if valid {
		mt.mc.trackers[id] += 1
	}
	append(&mt.valid, valid)
	append(&mt.ids, id)
}

clone_multitracker :: proc (mt : ^Multi_tracker($T)) -> ^Multi_tracker(T) {
	new_mt := make_multitracker(mt.mc)
	for id in mt.ids {
		add_id_to_multitracker(new_mt, id)
	}
	return new_mt
}

unordered_remove_index_from_multitracker :: proc (mt : ^Multi_tracker($T), idx : int) {
	assert(idx >= 0 && id < len(mt.ids))
	if mt.valid[idx] {
		assert(mt.mc.trackers[id] > 0)
		mt.mc.trackers[id] -= 1
		if mt.mc.trackers[mt.ids[idx]] == 0 && mt.mc.data_index[mt.ids[idx]] == -1 {
			append(&mt.mc.free_ids, mt.ids[idx])
		}
	}
	unordered_remove(&mt.ids, idx)
	unordered_remove(&mt.valid, idx)
}

cull_multitracker :: proc (mt : ^Multi_tracker($T)) {
	index := 0
	for index < len(mt.ids) {
		valid := check_multitracker_by_index(mt, index)
		if valid {
			index += 1
		}
		else {
			unordered_remove(&mt.ids, index)
			unordered_remove(&mt.valid, index)
		}
	}
}

add :: proc (mc : ^MContainer($T), data : T) -> Untracked_id(T) {
	new_id : int
	// if all the ints are already used
	if len(mc.free_ids) == 0 {
		new_id = len(mc.data_index)
		append(&mc.data_index, -1)
		append(&mc.trackers, 0)
	// if there are unused ints available
	} else {
		new_id = pop(&mc.free_ids)
	}
	mc.data_index[new_id] = len(mc.data)
	append(&mc.data, data)
	append(&mc.id, new_id)
	return Untracked_id(T){mc, new_id}
}

remove :: proc {remove_by_tracked_id, remove_by_untracked_id, direct_remove}

remove_by_tracked_id :: proc (id : ^Tracked_id($T)) {
	assert(id.valid)
	assert(check(id))
	direct_remove(id.mc, id.id)
	destroy_tracked_id(id)
}

remove_by_untracked_id :: proc (id : ^Untracked_id($T)) {
	if check(id) {
		direct_remove(id.mc, id.id)
	}
}

direct_remove :: proc (mc : ^MContainer($T), id : int) {
	assert(id >= 0 && id < len(mc.data_index) && mc.data_index[id] != -1)
	true_idx := mc.data_index[id]
	unordered_remove(&mc.data, true_idx)
	unordered_remove(&mc.id, true_idx)
	if true_idx < len(mc.id) {
		moved_id := mc.id[true_idx]
		mc.data_index[moved_id] = true_idx
	}
	mc.data_index[id] = -1
	if mc.trackers[id] == 0 do append(&mc.free_ids, id)
}

// read :: proc (mc : ^MContainer($T), id : int) -> T {
// 	// assert(id >= 0 && id <= len(mc.data_index))
// 	// if mc.data_index[id] == -1 do return {}, false
// 	// else do return mc.data[mc.data_index[id]], true
// 	assert(check_id(mc, id))
// 	return mc.data[mc.data_index[id]]
// }

read :: proc {read_from_tracked_id, read_from_untracked_id, direct_read}

read_from_tracked_id :: proc (id : ^Tracked_id($T)) -> Maybe(T) {
	if !id.valid {
		return nil
	}
	else if check(id) {
		return id.mc.data[id.mc.data_index[id.id]]
	}
	else {
		//destroy_tracked_id(id)
		return nil
	}
}

read_from_untracked_id :: proc (id : ^Untracked_id($T)) -> Maybe(T) {
	if check(id) {
		return id.mc.data[id.mc.data_index[id.id]]
	}
	else {
		return nil
	}
}

direct_read :: proc (mc : ^MContainer($T), id : int) -> Maybe(T) {
	if check(mc, id) {
		return mc.data[mc.data_index[id]]
	}
	else {
		return nil
	}
}

// access :: proc (mc : ^MContainer($T), id : int) -> ^T {
// 	// assert(id >= 0 && id <= len(mc.data_index))
// 	// if mc.data_index[id] == -1 do return {}, false
// 	// else do return &mc.data[mc.data_index[id]], true
// 	assert(check_id(mc, id))
// 	return &mc.data[mc.data_index[id]]
// }

access :: proc {access_from_tracked_id, access_from_untracked_id, direct_access}

access_from_tracked_id :: proc (id : ^Tracked_id($T)) -> Maybe(^T) {
	if !id.valid {
		return nil
	}
	else if check(id) {
		return &id.mc.data[id.mc.data_index[id.id]]
	}
	else {
		//destroy_tracked_id(id)
		return nil
	}
}

access_from_untracked_id :: proc (id : ^Untracked_id($T)) -> Maybe(^T) {
	if check(id) {
		return &id.mc.data[id.mc.data_index[id.id]]
	}
	else {
		return nil
	}
}

direct_access :: proc (mc : ^MContainer($T), id : int) -> Maybe(^T) {
	if check(mc, id) {
		return &mc.data[mc.data_index[id]]
	}
	else {
		return nil
	}
}

// id_from_index :: proc (mc : ^MContainer($T), idx : int) -> int {
// 	assert(idx >= 0 && idx <= len(mc.data))
// 	return mc.id[idx]
// }

// check_id :: proc (mc : ^MContainer($T), id : int) -> bool {
// 	return id >= 0 && id <= len(mc.data_index) && mc.data_index[id] != -1
// }

check :: proc {check_tracked_id, check_untracked_id, check_multitracker_by_index, direct_check}

check_tracked_id :: proc (id : ^Tracked_id($T)) -> bool {
	assert(id.id >= 0 && id.id < len(id.mc.data_index))
	if !id.valid {
		return false
	}
	else if id.mc.data_index[id.id] == -1 {
		destroy_tracked_id(id)
		return false
	}
	else {
		return true
	}
}

check_untracked_id :: proc (id : ^Untracked_id($T)) -> bool {
	assert(id.id >= 0 && id.id < len(id.mc.data_index))
	return id.mc.data_index[id.id] != -1
}

check_multitracker_by_index :: proc (mt : ^Multi_tracker($T), idx : int) -> bool {
	id := mt.ids[idx]
	if !mt.valid[idx] {
		return false
	}
	else if mt.mc.data_index[id] == -1 {
		assert(mt.mc.trackers[id] > 0)
		mt.mc.trackers[id] -= 1
		if mt.mc.trackers[id] == 0 {
			append(&mt.mc.free_ids, id)
		}
		mt.valid[idx] = false
		return false
	}
	else {
		return true
	}
}

direct_check :: proc (mc : ^MContainer($T), id : int) -> bool {
	assert(id >= 0 && id < len(mc.data_index))
	return mc.data_index[id] != -1
}

// track :: proc (mc : ^MContainer($T), id : int) {
// 	assert(id >= 0 && id <= len(mc.data_index) && mc.data_index[id] != -1)
// 	mc.trackers[id] += 1
// }

// forget :: proc (mc : ^MContainer($T), id : int) {
// 	//assert(check_id(mc, id))
// 	assert(id >= 0 && id <= len(mc.data_index))
// 	assert(mc.trackers[id] > 0)
// 	mc.trackers[id] -= 1
// 	if mc.trackers[id] == 0 && mc.data_index[id] == -1 do append(&mc.free_ids, id)
// }

count_ids :: proc (mc : ^MContainer($T)) -> (int, int, int) {
	// returns living ids, zombie ids, dead ids
	living_ids := len(mc.data)
	dead_ids := len(mc.free_ids)
	total_ids := len(mc.data_index)
	zombie_ids := total_ids - (living_ids + dead_ids)
	return living_ids, zombie_ids, dead_ids
}
