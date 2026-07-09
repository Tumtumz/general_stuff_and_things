#pragma once
#include <SDL3/SDL.h>
#include <cstdlib>
#include <vector>
#include "terrain.h"

struct Particle;
struct Chunk;

void set_pixel(SDL_Texture* texture, int x, int y, Uint8 color);

void clear_texture(SDL_Texture* texture);

void draw_terrain(SDL_Renderer* renderer, Chunk& chunk, SDL_FRect* offset);
