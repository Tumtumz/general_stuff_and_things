#include "../headers/UI.h"

// void report_fps() {
//     static Uint32 lastTime = 0;
//     static int frameCount = 0;

//     frameCount++;
//     Uint32 currentTime = SDL_GetTicks();
//     Uint32 elapsed = currentTime - lastTime;

//     if (elapsed >= 1000) {  // Update every second
//         int fps = frameCount / (elapsed / 1000);
//         SDL_Log("FPS: %i\n", fps);
//         frameCount = 0;
//         lastTime = currentTime;
//     }
// }

void report_fps(SDL_Renderer* renderer, TTF_Font* font) {
    static Uint32 lastTime = 0;
    static int frameCount = 0;
    static int fps = 0;

    frameCount++;
    Uint32 currentTime = SDL_GetTicks();
    Uint32 elapsed = currentTime - lastTime;

    if (elapsed >= 1000) {  // Update every second
        fps = frameCount / (elapsed / 1000);
        frameCount = 0;
        lastTime = currentTime;
    }

    // Convert FPS to a string
    std::string fpsText = "FPS: " + std::to_string(fps);

    // Render FPS text
    SDL_Color color = {255, 255, 255, 255};  // White color
    SDL_Surface* surface = TTF_RenderText_Solid(font, fpsText.c_str(), 0, color);
    if (!surface) return;  // Avoid crashing if font rendering fails

    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);
    if (!texture) {
        SDL_DestroySurface(surface);
        return;
    }

    int textWidth = surface->w;
    int textHeight = surface->h;
    SDL_DestroySurface(surface);

    SDL_FRect dstRect = {10, 10, (float)textWidth, (float)textHeight};  // Use SDL_FRect for SDL3
    SDL_RenderTexture(renderer, texture, NULL, &dstRect);
    SDL_DestroyTexture(texture);
}

void report_number(SDL_Renderer* renderer, TTF_Font* font, int number, const char* label){
    std::string msg = label + std::to_string(number); 
    SDL_Color color = {255, 255, 255, 255};  // White color

    SDL_Surface* surface = TTF_RenderText_Solid(font, msg.c_str(), 0, color);
    if (!surface) return;  // Avoid crashing if font rendering fails

    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);
    if (!texture) {
        SDL_DestroySurface(surface);
        return;
    }

    int textWidth = surface->w;
    int textHeight = surface->h;
    SDL_DestroySurface(surface);

    SDL_FRect dstRect = {10, 28, (float)textWidth, (float)textHeight};  // Use SDL_FRect for SDL3
    SDL_RenderTexture(renderer, texture, NULL, &dstRect);
    SDL_DestroyTexture(texture);
}