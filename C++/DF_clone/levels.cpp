#include "levels.h"
#include "creatures.h"
#include <SDL2/SDL.h>

Level::Level (){
    for (int x = 0; x < LEVEL_SIZE; x++){
        for (int y = 0; y < LEVEL_SIZE; y++){
            for (int z = 0; z < LEVEL_SIZE; z++){
                creatures[x][y][z] = NULL;
                blocks[x][y][z].type = 0;
            }
        }
    }
}

void Level::add_creature(Creature & creature){
    all_creatures.push_back(creature);
    this->creatures[creature.pos.x][creature.pos.y][creature.pos.z] = &creature;
}

void Level::remove_creature(Creature & creature){
    all_creatures.remove(creature);
    this->creatures[creature.pos.x][creature.pos.y][creature.pos.z] = NULL;
}

void Level::move_creature(Creature * creature, pos_3D new_pos){
    this->creatures[creature->pos.x][creature->pos.y][creature->pos.z] = NULL;
    creature->pos = new_pos;
    this->creatures[new_pos.x][new_pos.y][new_pos.z] = creature;
}

void Level::process_creatures(){
    static int last_pass_ticks = 0;
    int ticks = SDL_GetTicks();
    if (last_pass_ticks % 100 > ticks % 100){
        for (Creature creature : all_creatures){
            creature.process();
            std::cout << creature.type << std::endl;
        }
    }
    last_pass_ticks = ticks;
}

bool Level::is_passable(pos_3D pos){
    std::cout << pos.to_string() << std::endl;
    if (pos.x < 0 || pos.x >= LEVEL_SIZE){
        return false;
    }
    else if (pos.y < 0 || pos.y >= LEVEL_SIZE){
        return false;
    }
    else if (pos.z < 0 || pos.z >= LEVEL_SIZE){
        return false;
    }
    else{
        return blocks[pos.x][pos.y][pos.z].type == 0 && creatures[pos.x][pos.y][pos.z] == NULL;
    }
}

Level flat_level(int type){
    Level new_level;
    for (int x = 0; x < LEVEL_SIZE; x++){
        for (int y = 0; y < LEVEL_SIZE; y++){
            for (int z = 0; z < LEVEL_SIZE; z++){
                new_level.creatures[x][y][z] = NULL;
                if (z == 0){
                    new_level.blocks[x][y][z].type = type;
                }
            }
        }
    }
    return new_level;
}

Level full_level(int type){
    Level full_level;
    for (int x = 0; x < LEVEL_SIZE; x++){
        for (int y = 0; y < LEVEL_SIZE; y++){
            for (int z = 0; z < LEVEL_SIZE; z++){
                full_level.creatures[x][y][z] = NULL;
                full_level.blocks[x][y][z].type = type;
            }
        }
    }
    return full_level;
}