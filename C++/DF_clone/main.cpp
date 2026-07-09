//This is what I plug in to the compiler
//g++ main.cpp frame_counter.cpp levels.cpp creatures.cpp blocks.cpp pos_3D.cpp -lSDL2 -lSDL2_ttf -lSDL2_image -o DoppelDorf -g
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_surface.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>
#include "frame_counter.h"
#include "pos_3D.h"
#include "levels.h"
#include "creatures.h"
#include "blocks.h"
using namespace std;

SDL_Window* window = SDL_CreateWindow("DoppelDorf", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 1000, 1000, 0);
SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, 0);

const int CUBE_WIDTH = 42;
const int CUBE_HEIGHT = 48;

SDL_Texture* block_textures[231];

SDL_Texture* alien_textures[5] = {IMG_LoadTexture(renderer, "Aliens/alienBeige.png"), IMG_LoadTexture(renderer, "Aliens/alienBlue.png"), IMG_LoadTexture(renderer, "Aliens/alienGreen.png"), IMG_LoadTexture(renderer, "Aliens/alienPink.png"), IMG_LoadTexture(renderer, "Aliens/alienYellow.png")};

void load_block_textures(){
    for (int i = 0; i < 231; i++){
        string filename = "Cubes/block_texture_" + to_string(i + 1) + ".png";
        block_textures[i] = IMG_LoadTexture(renderer, filename.c_str());
    }
}

void draw_level(Level * chunk, SDL_Renderer* renderer){
    int screen_x = 400;
    int screen_y = 400;
    for (int x = 0; x < LEVEL_SIZE; x++){
        for (int y = 0; y < LEVEL_SIZE; y++){
            for (int z = 0; z < LEVEL_SIZE; z++){
                SDL_Rect location = {screen_x + x * CUBE_WIDTH / 2 - y * CUBE_WIDTH / 2, screen_y + x * CUBE_HEIGHT / 4 + y * CUBE_HEIGHT / 4 - z * CUBE_HEIGHT / 2, 50, 50};
                if (chunk->blocks[x][y][z].type != 0){
                    SDL_RenderCopy(renderer, block_textures[chunk->blocks[x][y][z].type - 1], NULL, &location);
                }
                if (chunk->creatures[x][y][z] != NULL){
                    SDL_RenderCopy(renderer, alien_textures[chunk->creatures[x][y][z]->type], NULL, &location);
                }
            }
        }
    }
}

int main(int argc, char *argv[]){
    if (SDL_Init(SDL_INIT_EVERYTHING) != 0) {
        cout << "Error initializing SDL: " << TTF_GetError() << endl;
    }
    if (TTF_Init() != 0) {
	    cout << "Error initializing SDL_ttf: " << TTF_GetError() << endl;
    }

    load_block_textures();

    Level world = flat_level(1);

    make_creature(0, pos_3D(0, 1, 1), &world);
    // make_creature(1, pos_3D(1, 1, 1), &world);
    // make_creature(2, pos_3D(2, 1, 1), &world);
    // make_creature(3, pos_3D(3, 1, 1), &world);
    // make_creature(4, pos_3D(4, 1, 1), &world);
    // Creature player{0, pos_3D(1, 1, 1), &world};
    // world.add_creature(player);
    SDL_Event event;
    bool running = true;
    extern float seconds;
    int mousex, mousey;
    const Uint8 *state = SDL_GetKeyboardState(NULL);

    while (running){
        SDL_SetRenderDrawColor(renderer, 64, 64, 64, 255);
        SDL_RenderClear(renderer);
        SDL_PumpEvents();
        while (SDL_PollEvent (&event)){
            if (event.type == SDL_QUIT){
                running = false;
                break;
            }
            if (event.type == SDL_KEYDOWN){
                if (event.key.keysym.sym == SDLK_ESCAPE){
                    running = false;
                    break;
                }
                // else if (event.key.keysym.sym == SDLK_LEFT){
                //     player.move_relative(pos_3D(-1, 0, 0));
                // }
                // else if (event.key.keysym.sym == SDLK_RIGHT){
                //     player.move_relative(pos_3D(1, 0, 0));
                // }
                // else if (event.key.keysym.sym == SDLK_UP){
                //     player.move_relative(pos_3D(0, -1, 0));
                // }
                // else if (event.key.keysym.sym == SDLK_DOWN){
                //     player.move_relative(pos_3D(0, 1, 0));
                // }
                // else if (event.key.keysym.sym == SDLK_SPACE){
                //     player.move_relative(pos_3D(0, 0, 1));
                // }
                // else if (event.key.keysym.sym == SDLK_c){
                //     player.move_relative(pos_3D(0, 0, -1));
                // }
            }
        }
        world.process_creatures();
        draw_level(&world, renderer);
        frameCounter(renderer);
        SDL_RenderPresent(renderer);
    }
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow (window);
    SDL_Quit();

    return 0;
}