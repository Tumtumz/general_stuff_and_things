#pragma once

#include <iostream>
#include <list>
#include <map>
#include "pos_3D.h"
// #include "creatures.h"
#include "blocks.h"

const int LEVEL_SIZE = 16;

struct Creature;

struct Level {
    Block blocks[LEVEL_SIZE][LEVEL_SIZE][LEVEL_SIZE];
    Creature* creatures[LEVEL_SIZE][LEVEL_SIZE][LEVEL_SIZE];
    std::list<Creature> all_creatures;

    Level ();

    void add_creature(Creature& creature);

    void remove_creature(Creature& creature);

    void move_creature(Creature * creature, pos_3D new_pos);

    void process_creatures();

    bool is_passable(pos_3D pos);
};

Level flat_level(int type);

Level full_level(int type);