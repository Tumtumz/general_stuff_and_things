package linked_lists

// Iteration:
// Forward:                 for l := list.first; l != nil; l = l.next { … }
// Backward (doubly only):  for l := list.final; l != nil; l = l.prev { … }

Single_Linked_List :: struct ($T : typeid) {
    first : ^Single_Link(T),
    final : ^Single_Link(T),
    length : int,
}

Single_Link :: struct ($T : typeid) {
    data : T,
    next : ^Single_Link(T),
}

Double_Linked_List :: struct ($T : typeid) {
    first : ^Double_Link(T),
    final : ^Double_Link(T),
    length : int,
}

Double_Link :: struct ($T : typeid) {
    data : T,
    prev : ^Double_Link(T),
    next : ^Double_Link(T),
}

create_single :: proc ($T : typeid) -> ^Single_Linked_List(T) {
    list := new(Single_Linked_List(T))
    list.first = nil
    list.final = nil
    list.length = 0
    return list
}

create_double :: proc ($T : typeid) -> ^Double_Linked_List(T) {
    list := new(Double_Linked_List(T))
    list.first = nil
    list.final = nil
    list.length = 0
    return list
}

push_front :: proc {push_front_single, push_front_double}

push_front_single :: proc (list : ^Single_Linked_List($T), data : T) {
    link := new(Single_Link(T))
    link.data = data
    link.next = list.first
    list.first = link
    if list.length == 0 {
        list.final = link
    }
    list.length += 1
}

push_front_double :: proc (list : ^Double_Linked_List($T), data : T) {
    link := new(Double_Link(T))
    link.data = data
    link.next = list.first
    link.prev = nil
    if list.length != 0  {
        list.first.prev = link
    }
    else {
        list.final = link
    }
    list.first = link
    list.length += 1
}

push_back :: proc {push_back_single, push_back_double}

push_back_single :: proc (list : ^Single_Linked_List($T), data : T) {
    link := new(Single_Link(T))
    link.data = data
    link.next = nil
    if list.length != 0 {
        list.final.next = link
    }
    else {
        list.first = link
    }
    list.final = link
    list.length += 1
}

push_back_double :: proc (list : ^Double_Linked_List($T), data : T) {
    link := new(Double_Link(T))
    link.data = data
    link.next = nil
    link.prev = list.final
    if list.length != 0 {
        list.final.next = link
    }
    else {
        list.first = link
    }
    list.final = link
    list.length += 1
}

pop_front :: proc {pop_front_single, pop_front_double}

pop_front_single :: proc (list : ^Single_Linked_List($T)) -> (T, bool) {
    if list.length > 0 {
        data := list.first.data
        second := list.first.next
        free(list.first)
        list.first = second
        list.length -= 1
        if list.length == 0 {
            list.final = nil
        }
        return data, true
    }
    else {
        return T{}, false
    }
}

pop_front_double :: proc (list : ^Double_Linked_List($T)) -> (T, bool) {
    if list.length > 0 {
        data := list.first.data
        second := list.first.next
        free(list.first)
        list.first = second
        if second != nil {
            second.prev = nil
        }
        list.length -= 1
        if list.length == 0 {
            list.final = nil
        }
        return data, true
    }
    else {
        return T{}, false
    }
}

pop_back :: proc {pop_back_double}

pop_back_double :: proc (list : ^Double_Linked_List($T)) -> (T, bool) {
    if list.length > 0 {
        data := list.final.data
        second_to_last := list.final.prev
        free(list.final)
        list.final = second_to_last
        if second_to_last != nil {
            second_to_last.next = nil
        }
        list.length -= 1
        return data, true
    }
    else {
        return T{}, false
    }
}

insert_after :: proc {insert_after_single, insert_after_double}

insert_after_single :: proc (list : ^Single_Linked_List($T), link : ^Single_Link(T), data : T) {
    new_link := new(Single_Link(T))
    new_link.data = data
    new_link.next = link.next
    link.next = new_link
    list.length += 1
    if link == list.final {
        list.final = new_link
    }
}

insert_after_double :: proc  (list : ^Double_Linked_List($T), link : ^Double_Link(T), data : T) {
    new_link := new(Double_Link(T))
    new_link.data = data
    new_link.next = link.next
    new_link.prev = link
    if link.next != nil {
        link.next.prev = new_link
    }
    link.next = new_link
    if link == list.final {
        list.final = new_link
    }
    list.length += 1
}

remove :: proc {remove_double}

remove_double :: proc (list : ^Double_Linked_List($T), link : ^Double_Link(T)) {
    if link.prev != nil {
        link.prev.next = link.next
    }
    if link.next != nil {
        link.next.prev = link.prev
    }
    if link == list.first {
        list.first = link.next
    }
    if link == list.final {
        list.final = link.prev
    }
    free(link)
    list.length -= 1
}

delete :: proc {delete_single, delete_double}

delete_single :: proc (list : ^Single_Linked_List($T)) {
    for l := list.first; l != nil; {
        next := l.next
        free(l)
        l = next
    }
    free(list)
}

delete_double :: proc (list : ^Double_Linked_List($T)) {
    for l := list.first; l != nil; {
        next := l.next
        free(l)
        l = next
    }
    free(list)
}

clear :: proc {clear_single, clear_double}

clear_single :: proc (list : ^Single_Linked_List($T)) {
    for l := list.first; l != nil; {
        next := l.next
        free(l)
        l = next
    }
    list.first = nil
    list.final = nil
    list.length = 0
}

clear_double :: proc (list : ^Double_Linked_List($T)) {
    for l := list.first; l != nil; {
        next := l.next
        free(l)
        l = next
    }
    list.first = nil
    list.final = nil
    list.length = 0
}
