#include "../headers/graphics.h"

void set_pixel(SDL_Texture* texture, int x, int y, Uint16 color) {
    void *pixels;
    int pitch;
    if (!(SDL_LockTexture(texture, NULL, &pixels, &pitch))) {
        return;
    }
    Uint16 *pixelData = (Uint16 *)pixels;
    int index = y * pitch + x;
    pixelData[index] = color;
    SDL_UnlockTexture(texture);
}

void clear_texture(SDL_Texture* texture){
    void *pixels;
    int pitch;
    SDL_LockTexture(texture, NULL, &pixels, &pitch);
    SDL_memset(pixels, 0,  texture->h * pitch);
    SDL_UnlockTexture(texture);
}

// void draw_particles(SDL_Texture* texture, const std::vector<Particle>& particles){
//     void *pixels;
//     int pitch;
//     if (!(SDL_LockTexture(texture, NULL, &pixels, &pitch))) {
//         return;
//     }
//     Uint16 *pixelData = (Uint16 *)pixels;
//     for (int i = 0; i < particles.size(); i++){
//         int index = int(particles[i].y) * (pitch / sizeof(Uint16)) + int(particles[i].x);
//         pixelData[index] = particles[i].colour;
//     }
//     SDL_UnlockTexture(texture);
// }

void draw_terrain(SDL_Renderer* renderer, Chunk& chunk, SDL_FRect* offset){
    if (!chunk.texture_up_to_date){
        // SDL_Log("Update texture");
        update_texture(&chunk);
    }
    SDL_Texture* pixelTexture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA4444, SDL_TEXTUREACCESS_STREAMING, 1, 1);

    // Set the color of the pixel by updating its texture

    // Render the texture (pixel) at (x, y)
    // SDL_Log("render particles");
    // SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    for (int i = 0; i < chunk.particles.size(); i++){
        Particle& p = chunk.particles[i];
        Uint8 r = (p.colour & 0xf000) >> 8;
        Uint8 g = (p.colour & 0x0f00) >> 4;
        Uint8 b = (p.colour & 0x00f0);
        Uint8 a = (p.colour & 0x000f) << 4;
        SDL_SetRenderDrawColor(renderer, r, g, b, a);
        SDL_RenderPoint(renderer, p.x, p.y);
    }
    SDL_RenderTexture(renderer, chunk.texture, offset, NULL);
}