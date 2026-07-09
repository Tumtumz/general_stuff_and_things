#pragma once
#include <SDL3/SDL.h>
#include <cstdlib>
#include <vector>
#include "graphics.h"

static int CHUNK_SIZE = 64 * 64;

struct Particle {
    float x;
    float y;
    float xvel;
    float yvel;
    float bounciness;
    Uint16 colour;
};

//a square of 4096 x 4096 pixels
struct Chunk {
    Uint64* blockmap;
    Uint16* colourmap;
    SDL_Texture* texture;
    bool texture_up_to_date;
    //these 4 values describe the smallest rectangle with out-of-date texture data
    int xmin;
    int xmax;
    int ymin;
    int ymax;
    std::vector<Particle> particles;

    Chunk();
    Chunk(SDL_Renderer* renderer);
    ~Chunk();
};

inline bool check_block_map(Chunk* chunk, int x, int y);

void process_particles(Chunk* chunk);

void add_texture(Chunk* chunk, SDL_Renderer* renderer);

void find_edges(Chunk* chunk);

void update_texture(Chunk* chunk);

void set_terrain(Chunk* chunk, int x, int y, bool value, int brush_size);

void bresenham(Chunk* chunk, int x, int y, int xrel, int yrel);

bool check_collision(Chunk* chunk, float x, float y, float dx, float dy, float * cx, float * cy, float * x2, float * y2);