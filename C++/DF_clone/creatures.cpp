#include "creatures.h"
#include "levels.h"

Creature::Creature(int type, pos_3D pos, Level * world){
    this->type = type;
    this->pos = pos;
    this->world = world;
}

void Creature::move_relative(pos_3D direction){
    pos_3D new_pos = this->pos + direction;
    if (world->is_passable(new_pos)){
        std::cout << new_pos.to_string() << std::endl;
        world->move_creature(this, new_pos);
    }
}

void Creature::process(){
    int x_dir = rand()%3 - 1;
    int y_dir = rand()%3 - 1;
    this->move_relative(pos_3D{x_dir, y_dir, 0});
}

void make_creature(int type, pos_3D pos, Level * world){
    Creature new_creature{type, pos, world};
    world->add_creature(new_creature);
}

bool operator== (Creature first, Creature second){
    return first.type == second.type && first.pos == second.pos;
}