#include "frame_counter.h"

float seconds;

void frameCounter(SDL_Renderer *renderer){
    //Work out how much time has passed since last function call.
    //Use of the 'static' keyword is indispensible here.
    //the time since the last frame is calculated by subtracting the time of the previous
    //function call from the current time (the function is called at the end of each frame)
    static timeval time;
    int time1 = time.tv_sec*1000000 + time.tv_usec;
    gettimeofday(&time, NULL);
    int time2 = time.tv_sec*1000000 + time.tv_usec;
    seconds = (time2 - time1)/1000000.0;

    //Useful tools that will help us later
    SDL_Rect render_location;
    const char* text;
    SDL_Texture* texture;
    static TTF_Font* font = TTF_OpenFont("FreeMono.ttf", 22);
    static SDL_Color white = {255, 255, 255};
    static SDL_Color black = {0, 0, 0};

    //render labels
    static SDL_Surface* SPF_label = TTF_RenderText_Shaded(font, "ms/f: ", black, white);
    static SDL_Texture* SPF_texture = SDL_CreateTextureFromSurface(renderer, SPF_label);
    static SDL_Rect SPF_location = {0, 0, SPF_label->w, SPF_label->h};
    static SDL_Surface* FPS_label = TTF_RenderText_Shaded(font, "FPS:  ", black, white);
    static SDL_Texture* FPS_texture = SDL_CreateTextureFromSurface(renderer, FPS_label);
    static SDL_Rect FPS_location = {0, 25, FPS_label->w, FPS_label->h};
    SDL_RenderCopy(renderer, SPF_texture, NULL, &SPF_location);
    SDL_RenderCopy(renderer, FPS_texture, NULL, &FPS_location);

    //render ms /frame
    text = to_string(seconds * 1000).substr(0, 4).c_str();
    static SDL_Surface* msPerFrame;
    msPerFrame = TTF_RenderText_Shaded(font, text, black, white);
    render_location = {75, 0, msPerFrame->w, msPerFrame->h};
    texture = SDL_CreateTextureFromSurface(renderer, msPerFrame);
    SDL_RenderCopy(renderer, texture, NULL, &render_location);

    //render frames /s
    int fps = 1/seconds;
    text = to_string(fps).c_str();
    static SDL_Surface* fpsRender;
    fpsRender = TTF_RenderText_Shaded(font, text, black, white);
    render_location = {75, 25, fpsRender->w, fpsRender->h};
    texture = SDL_CreateTextureFromSurface(renderer, fpsRender);
    SDL_RenderCopy(renderer, texture, NULL, &render_location);
}