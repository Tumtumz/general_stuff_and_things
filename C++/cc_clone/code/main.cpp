#define SDL_MAIN_USE_CALLBACKS 1
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>
#include <SDL3_ttf/SDL_ttf.h>
#include <cstdlib>
#include <vector>
#include "../headers/graphics.h"
#include "../headers/terrain.h"
#include "../headers/UI.h"

int width = 1600;
int height = 900;

static SDL_Window *window = NULL;
static SDL_Renderer *renderer = NULL;
static TTF_Font* font = NULL;
static SDL_FRect offset = {0, 0, float(width), float(height)};

static Chunk terrain;

std::vector<Particle> particles = {};

SDL_AppResult SDL_AppInit(void **appstate, int argc, char *argv[])
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        SDL_Log("Couldn't initialize SDL: %s", SDL_GetError());
        return SDL_APP_FAILURE;
    }
    if (!SDL_CreateWindowAndRenderer("CCClone_Test", width, height, 0, &window, &renderer)) {
        SDL_Log("Couldn't create window/renderer: %s", SDL_GetError());
        return SDL_APP_FAILURE;
    }
    if (!TTF_Init()) {
        SDL_Log("Couldn't initialise SDL_ttf: %s\n", SDL_GetError());
        return SDL_APP_FAILURE;
    }
    font = TTF_OpenFont("./assets/FreeMono.ttf", 18);
    if (!font) {
        SDL_Log("Couldn't open font: %s\n", SDL_GetError());
        return SDL_APP_FAILURE;
    }

    add_texture(&terrain, renderer);
    return SDL_APP_CONTINUE;
}

SDL_AppResult SDL_AppEvent(void *appstate, SDL_Event *event)
{
    if (event->type == SDL_EVENT_QUIT) {
        return SDL_APP_SUCCESS;
    }
    else if ((event->type == SDL_EVENT_KEY_DOWN) && (event->key.key == SDLK_ESCAPE)) {
		return SDL_APP_SUCCESS;
	}
    else if ((event->type == SDL_EVENT_KEY_DOWN) && (event->key.key == SDLK_M)) {
		find_edges(&terrain);
	}
    // else if ((event->type == SDL_EVENT_MOUSE_BUTTON_DOWN) && (event->button.button == 1)) {
	// 	SDL_Log("%i", check_block_map(&terrain, event->button.x, event->button.y));
	// }
    else if ((event->type == SDL_EVENT_MOUSE_MOTION) && SDL_GetMouseState(NULL, NULL) & SDL_BUTTON_LMASK){
        bresenham(&terrain, event->button.x, event->button.y, event->motion.xrel, event->motion.yrel);
    }
    // else if (event->type == SDL_EVENT_MOUSE_BUTTON_DOWN && event->button.button != 1){
    //     particles.push_back(Particle {event->button.x, event->button.y, (((float)(rand()) / (float)(RAND_MAX)) * 2) - 1, (((float)(rand()) / (float)(RAND_MAX)) * 2) - 1, 0.3f, rgba_to_rgb332(0xFFFFFFFF)});
    // }
    else if (SDL_GetMouseState(NULL, NULL) & SDL_BUTTON_RMASK){
        float xvel = (2.0f * rand() / RAND_MAX) - 1.0f;
        float yvel = (2.0f * rand() / RAND_MAX) - 1.0f;
        terrain.particles.push_back(Particle {event->button.x, event->button.y, xvel, yvel, 0.3f, 0xff0f});
    }
    return SDL_APP_CONTINUE;
}

SDL_AppResult SDL_AppIterate(void *appstate)
{
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);

    SDL_RenderClear(renderer);

    draw_terrain(renderer, terrain, &offset);

    process_particles(&terrain);

    report_fps(renderer, font);
    report_number(renderer, font, terrain.particles.size(), "Particles: ");

    // SDL_Log("p");
    SDL_UpdateWindowSurface(window);
    SDL_RenderPresent(renderer);

    return SDL_APP_CONTINUE;
}

void SDL_AppQuit(void *appstate, SDL_AppResult result)
{
    // SDL will clean up the window/renderer for us.
    if (font) {
        TTF_CloseFont(font);
    }
    TTF_Quit();
}