#pragma once
#include <SDL3/SDL.h>
#include <SDL3_ttf/SDL_ttf.h>
#include <string>

void report_fps(SDL_Renderer* renderer, TTF_Font* font);

void report_number(SDL_Renderer* renderer, TTF_Font* font, int number, const char* label);