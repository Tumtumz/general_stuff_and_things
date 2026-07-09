#pragma once

#include <iostream>
// #include "chunks.h"
#include "pos_3D.h"

struct Level;

struct Creature {
    int type;
    pos_3D pos;
    Level* world;
    pos_3D chunk_ID;

    Creature();

    Creature(int type, pos_3D pos, Level * world);

    void move_relative(pos_3D direction);

    void process();
};

void make_creature(int type, pos_3D pos, Level * world);

bool operator== (Creature first, Creature second);