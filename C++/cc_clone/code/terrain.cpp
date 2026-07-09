#include "../headers/terrain.h"

Chunk::Chunk(){
    // SDL_Log("Allocating colourmap");
    blockmap = new Uint64[64* CHUNK_SIZE];
    colourmap = new Uint16[CHUNK_SIZE * CHUNK_SIZE];
    texture = NULL;
    texture_up_to_date = true;
    xmin = 64;
    xmax = 0;
    ymin = 64;
    ymax = 0;
}

Chunk::Chunk(SDL_Renderer* renderer){
    // SDL_Log("Allocating colourmap");
    blockmap = new Uint64[64* CHUNK_SIZE];
    colourmap = new Uint16[CHUNK_SIZE * CHUNK_SIZE];
    texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA4444, SDL_TEXTUREACCESS_STREAMING, CHUNK_SIZE, CHUNK_SIZE);
    texture_up_to_date = true;
    xmin = 64;
    xmax = 0;
    ymin = 64;
    ymax = 0;
}

Chunk::~Chunk(){
    // SDL_Log("Deallocating colourmap");
    delete[] blockmap;
    delete[] colourmap;
}

inline bool check_block_map(Chunk* chunk, int x, int y){
    return ((x >= 0) && (y >= 0) && (x < CHUNK_SIZE) && (y < CHUNK_SIZE) && (chunk->blockmap[y * 64 + x / 64] & (1ULL << (x%64))));
}

void add_texture(Chunk* chunk, SDL_Renderer* renderer){
    chunk->texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA4444, SDL_TEXTUREACCESS_STREAMING, CHUNK_SIZE, CHUNK_SIZE);
}

void find_edges(Chunk* chunk){
    for (int y = 0; y < CHUNK_SIZE; y++){
        for (int x = 0; x < 64; x++){
            if (chunk->blockmap[y * 64 + x]){
                Uint64 original = chunk->blockmap[y * 64 + x];
                Uint64 shifted_left = original << 1;
                shifted_left |= (x != 0 && chunk->blockmap[y * 64 + x - 1] & 0x8000000000000000) ? 1ULL : 0;
                Uint64 shifted_right = original >> 1;
                shifted_right |= (x != 63 && chunk->blockmap[y * 64 + x + 1] & 1ULL) ? 0x8000000000000000 : 0;
                Uint64 row_up = chunk->blockmap[(y-1) * 64 + x];
                Uint64 row_down = chunk->blockmap[(y+1) * 64 + x];
                Uint64 l_edges = original & ~shifted_left;
                Uint64 r_edges = original & ~shifted_right;
                Uint64 t_edges = original & ~row_up;
                Uint64 b_edges = original & ~row_down;
                // I caused myself a lot of confusion here by effectively looping backwards
                // note how I do this [[1ULL << x1]]
                // ... starting at one end of the 64 bits and shifting to the other
                // but I have chosen to encode them forwards  colourmap[y * CHUNK_SIZE + x * 64 + x1]
                // so I had to make it work by encoding the Uint64 x_edges backwards to compensate, and that's why it seems I'm checking the wrong neighbours
                for (int x1 = 0; x1 < 64; x1++){
                    if (l_edges & (1ULL << x1)){
                        // when we find a left edge
                        chunk->colourmap[y * CHUNK_SIZE + x * 64 + x1] = 0xf00f;
                        chunk->texture_up_to_date = false;
                        chunk->xmin = std::min(chunk->xmin, x1);
                        chunk->xmax = std::max(chunk->xmax, x1 + 1);
                        chunk->ymin = std::min(chunk->ymin, y);
                        chunk->ymax = std::max(chunk->ymax, y + 1);
                    }
                    if (r_edges & (1ULL << x1)){
                        // when we find a right edge
                        chunk->colourmap[y * CHUNK_SIZE + x * 64 + x1] = 0xf0ff;
                        chunk->texture_up_to_date = false;
                        chunk->xmin = std::min(chunk->xmin, x * 64 + x1);
                        chunk->xmax = std::max(chunk->xmax, x * 64 + x1 + 1);
                        chunk->ymin = std::min(chunk->ymin, y);
                        chunk->ymax = std::max(chunk->ymax, y + 1);
                    }
                    if (t_edges & (1ULL << x1)){
                        // when we find a up edge
                        chunk->colourmap[y * CHUNK_SIZE + x * 64 + x1] = 0x0f0f;
                        chunk->texture_up_to_date = false;
                        chunk->xmin = std::min(chunk->xmin, x1);
                        chunk->xmax = std::max(chunk->xmax, x1 + 1);
                        chunk->ymin = std::min(chunk->ymin, y);
                        chunk->ymax = std::max(chunk->ymax, y + 1);
                    }
                    if (b_edges & (1ULL << x1)){
                        // when we find a down edge
                        chunk->colourmap[y * CHUNK_SIZE + x * 64 + x1] = 0x00ff;
                        chunk->texture_up_to_date = false;
                        chunk->xmin = std::min(chunk->xmin, x * 64 + x1);
                        chunk->xmax = std::max(chunk->xmax, x * 64 + x1 + 1);
                        chunk->ymin = std::min(chunk->ymin, y);
                        chunk->ymax = std::max(chunk->ymax, y + 1);
                    }
                }

            }
        }
    }
}

void update_texture(Chunk* chunk){
    int pixels_wide = chunk->xmax - chunk->xmin;
    int pixels_high = chunk->ymax - chunk->ymin;
    size_t bytes = pixels_wide * pixels_high * sizeof(Uint16);
    Uint16 *pixelBuffer = (Uint16*)malloc(bytes); // Pre-allocate memory
    for (int x = 0; x < pixels_wide; x++){
        for (int y = 0; y < pixels_high; y++){
            int index = y * pixels_wide + x;
            int x_abs = x + chunk->xmin;
            int y_abs = y + chunk->ymin;
            //come back and change this later, there mest be a way to load several pixels at a time when I'm properly storing pixel colour data
            pixelBuffer[index] = chunk->blockmap[y_abs * 64 + x_abs/64] & (1ULL << x_abs%64) ? chunk->colourmap[x_abs + CHUNK_SIZE * y_abs] : 0x0000;
        }
    }
    SDL_Rect update_area {chunk->xmin, chunk->ymin, pixels_wide, pixels_high};
    void *pixels;
    int pitch;
    if (!SDL_LockTexture(chunk->texture, &update_area, &pixels, &pitch)){
        SDL_Log("no lock! %s", SDL_GetError());
    }
    for (size_t y = 0; y < pixels_high; y++) {
        memcpy((Uint8*)pixels + y * pitch, pixelBuffer + y * pixels_wide, pixels_wide * sizeof(Uint16));
    }
    SDL_UnlockTexture(chunk->texture);
    free(pixelBuffer);
    chunk->texture_up_to_date = true;
    chunk->xmin = CHUNK_SIZE;
    chunk->xmax = 0;
    chunk->ymin = CHUNK_SIZE;
    chunk->ymax = 0;
}

void set_terrain(Chunk* chunk, int x, int y, bool value, int brush_size){
    // SDL_Log("Blah1");
    for (int w = -brush_size; w < brush_size * 2;  w++){
        for (int h = -brush_size; h < brush_size * 2;  h++){
            int x1 = x + w;
            int y1 = y + h;
            Uint64 subxpos = 1ULL << x1%64;
            if ((0 <= x1 < CHUNK_SIZE) && (0 <= y1 < CHUNK_SIZE)){
                // SDL_Log("Blaha");
                chunk->blockmap[y1 * 64 + x1/64] |= subxpos;
                // SDL_Log("Blahb");
                chunk->colourmap[y1 * CHUNK_SIZE + x1] = 0xffff;
                chunk->texture_up_to_date = false;
                chunk->xmin = std::min(chunk->xmin, x1);
                chunk->xmax = std::max(chunk->xmax, x1 + 1);
                chunk->ymin = std::min(chunk->ymin, y1);
                chunk->ymax = std::max(chunk->ymax, y1 + 1);
            }
        }
    }
    // SDL_Log("Blah2");
}

void bresenham(Chunk* chunk, int x, int y, int xrel, int yrel){
    int x2 = x - xrel;
    int y2 = y - yrel;
    int dx = abs(x2 - x);
    int dy = abs(y2 - y);
    int sx = (x < x2) ? 1 : -1;
    int sy = (y < y2) ? 1 : -1;
    int err = abs(dx) - abs(dy);
    int index = 0;
    while (x != x2 || y != y2) {
        set_terrain(chunk, x, y, 1, 3);
        int e2 = 2 * err;
        if (e2 > -dy) { err -= dy; x += sx; }
        if (e2 < dx)  { err += dx; y += sy; }
    }
}

void process_particles(Chunk* chunk){
    // SDL_Log("Processing...");
    for (int i = 0; i < chunk->particles.size();){
        Particle& p = chunk->particles[i];
        // p.yvel += 1.0f;
        int x_start = p.x;
        int y_start = p.y;
        int x_end = p.x + p.xvel;
        int y_end = p.y + p.yvel;

        bool collision = false;
        //check for collisions with bresenham's line algorithm
        int dx = abs(x_end - x_start);
        int dy = abs(y_end - y_start);
        int sx = (x_start < x_end) ? 1 : -1;
        int sy = (y_start < y_end) ? 1 : -1;
        int err = abs(dx) - abs(dy);
        // SDL_Log("blah1...");
        while (x_start != x_end || y_start != y_end) {
            //check particle grid for collision at each intermediate point
            if (check_block_map(chunk, x_start, y_start)){
                collision = true;
                //when we collide, check neighbouring points to determine angle of reflection
                // SDL_Log("blah2...");
                bool a = check_block_map(chunk, x_start, y_start - 1);
                // SDL_Log("blah2a...");
                bool b = check_block_map(chunk, x_start - 1, y_start);
                // SDL_Log("blah2b...");
                bool c = check_block_map(chunk, x_start + 1, y_start);
                // SDL_Log("blah2c...");
                bool d = check_block_map(chunk, x_start, y_start + 1);
                if (p.xvel < 0){
                    bool swapper = b;
                    b = c;
                    c = swapper;
                }
                if (p.yvel < 0){
                    bool swapper = a;
                    a = d;
                    d = swapper;
                }
                float other_swapper;
                // SDL_Log("blah3...");
                if (!(a | b) && c == d){
                    // SDL_Log("is...");
                    //diaginal surface reflection
                    //change particle velocity
                    other_swapper = p.xvel;
                    p.xvel = -p.yvel * p.bounciness;
                    p.yvel = -other_swapper * p.bounciness;
                    //update bresenham's numbers
                    int new_x_end = x_start + (y_start - y_end);
                    y_end = y_start + (x_start - x_end);
                    x_end = new_x_end;
                    dx = abs(x_end - x_start);
                    dy = abs(y_end - y_start);
                    sx = (x_start < x_end) ? 1 : -1;
                    sy = (y_start < y_end) ? 1 : -1;
                    err = abs(dx) - abs(dy);
                }
                else if (!a && (b | c)){
                    // SDL_Log("it...");
                    //horizontal surface reflection
                    //change particle velocity
                    p.yvel = -p.yvel * p.bounciness;
                    //update bresenham's numbers
                    y_end = y_start - (y_end - y_start);
                    dx = abs(x_end - x_start);
                    dy = abs(y_end - y_start);
                    sx = (x_start < x_end) ? 1 : -1;
                    sy = (y_start < y_end) ? 1 : -1;
                    err = abs(dx) - abs(dy);
                }
                else if (!b && (a | d)){
                    // SDL_Log("this...");
                    //vertical surface reflection
                    //change particle velocity
                    p.xvel = -p.xvel * p.bounciness;
                    //update bresenham's numbers
                    x_end = x_start - (x_end - x_start);
                    dx = abs(x_end - x_start);
                    dy = abs(y_end - y_start);
                    sx = (x_start < x_end) ? 1 : -1;
                    sy = (y_start < y_end) ? 1 : -1;
                    err = abs(dx) - abs(dy);
                }
                else {
                    //a && b
                    //retroreflection
                    //change particle velocity
                    p.xvel = -p.xvel * p.bounciness;
                    p.yvel = -p.yvel * p.bounciness;
                    //update bresenham's numbers
                    x_end = x_start - (x_end - x_start);
                    y_end = y_start - (y_end - y_start);
                    dx = abs(x_end - x_start);
                    dy = abs(y_end - y_start);
                    sx = (x_start < x_end) ? 1 : -1;
                    sy = (y_start < y_end) ? 1 : -1;
                    err = abs(dx) - abs(dy);
                    // SDL_Log("wh...");
                }
            }
            //once we've sorted collisios we can continue with bresenham's
            // SDL_Log("blah4...");
            int e2 = 2 * err;
            if (e2 > -dy) { err -= dy; x_start += sx; }
            if (e2 < dx)  { err += dx; y_start += sy; }
        }
        if (collision){
            p.x = x_start;
            p.y = y_start;
        }
        else{
            p.x += p.xvel;
            p.y += p.yvel;
        }

        // check to see if the particle is still in the chunk
        // SDL_Log("blah5...");
        if ((p.x <= 0) || (p.x > CHUNK_SIZE - 1) || (p.y > CHUNK_SIZE - 1)){
            chunk->particles.erase(chunk->particles.begin() + i);
        }
        else {
            i++;
        }
        // SDL_Log("blah6...");
    }
    // SDL_Log("Done Processing");
}

// bool check_collision(Chunk* chunk, float x, float y, float dx, float dy, float * cx, float * cy, float * x2, float * y2){
//     float c = 0;
//     float slope = 0;
//     if (dx != 0 && dy != 0){
//         slope = dy / dx;
//         c = y - slope * x;
//     }
//     else if (dy == 0){
//         c = y;
//     }
//     bool intersection = false;
//     int direction = 0;
//     if (dx > 0){
        
//     }
// }
//     if dx > 0 and leftlines:
//         #left edges
//         start_index = first_greater(leftlines, x)
//         end_index = last_smaller(leftlines, x + dx)
//         for i in range(start_index, end_index + 1):
//             line = leftlines[i]
//             if horizontal:
//                 yval = y
//             else:
//                 yval = line.i * slope + c
//             if line.v1 <= yval <= line.v2 + 1:
//                 intersection = True
//                 cx = line.i
//                 cy = yval
//                 direction = "left"
//                 break
//     elif dx < 0 and rightlines:
//         #right edges
//         start_index = first_greater(rightlines, x + dx - 1)
//         end_index = last_smaller(rightlines, x - 1)
//         for i in reversed(range(start_index, end_index + 1)):
//             line = rightlines[i]
//             if horizontal:
//                 yval = y
//             else:
//                 yval = (line.i + 1) * slope + c
//             if line.v1 <= yval <= (line.v2 + 1):
//                 intersection = True
//                 cx = line.i + 1
//                 cy = yval
//                 direction = "right"
//                 break
//     if dy > 0 and toplines:
//         #top edges
//         start_index = first_greater(toplines, y)
//         if intersection:
//             end_index = last_smaller(toplines, cy)
//         else:
//             end_index = last_smaller(toplines, y + dy)
//         for i in range(start_index, end_index + 1):
//             line = toplines[i]
//             if vertical:
//                 xval = x
//             else:
//                 xval = (line.i - c) / slope
//             if line.v1 <= xval <= line.v2 + 1:
//                 if not intersection or cy > line.i:
//                     intersection = True
//                     cx = xval
//                     cy = line.i
//                     direction = "up"
//                 break
//     elif dy < 0 and bottomlines:
//         #bottom edge
//         if intersection:
//             start_index = first_greater(bottomlines, cy - 1)
//         else:
//             start_index = first_greater(bottomlines, y + dy - 1)
//         end_index = last_smaller(bottomlines, y - 1)
//         for i in reversed(range(start_index, end_index + 1)):
//             line = bottomlines[i]
//             if vertical:
//                 xval = x
//             else:
//                 xval = ((line.i + 1) - c) / slope
//             if line.v1 <= xval <= (line.v2 + 1):
//                 if not intersection or cy < line.i + 1:
//                     intersection = True
//                     cx = xval
//                     cy = line.i + 1
//                     direction = "down"
//                 break
//     # now we check against the diagonals...
//     # for any given direction at most 2 of the diagonal directions need checking.
//     if dy < dx and BLlines:
//         offset = 18
//         #BL lines
//         start_index = first_greater(BLlines, (x - y) + offset)
//         if intersection:
//             end_index = last_smaller(BLlines, (cx - cy) + offset)
//         else:
//             end_index = last_smaller(BLlines, ((x + dx) - (y + dy)) + offset)
//         for i in range(start_index, end_index + 1):
//             line = BLlines[i]
//             b = -line.i + offset
//             if vertical:
//                 xval = x
//             else:
//                 xval = (b - c) / (slope - 1)
//             if horizontal:
//                 yval = y
//             else:
//                 yval = xval + b
//             if line.v1 <= yval <= (line.v2 + 1):
//                 if not intersection or cx - cy > xval - yval:
//                     intersection = True
//                     cx = xval
//                     cy = yval
//                     direction = "down/left"
//                 break
//     elif dy > dx and TRlines:
//         offset = 18
//         #TR lines
//         if intersection:
//             start_index = first_greater(TRlines, (cx - cy) + offset)
//         else:
//             start_index = first_greater(TRlines, ((x + dx) - (y + dy)) + offset)
//         end_index = last_smaller(TRlines, (x - y) + offset)
//         for i in reversed(range(start_index, end_index + 1)):
//             line = TRlines[i]
//             b = -line.i + offset
//             if vertical:
//                 xval = x
//             else:
//                 xval = (b - c) / (slope - 1)
//             if horizontal:
//                 yval = y
//             else:
//                 yval = xval + b
//             if line.v1 <= yval <= (line.v2 + 1):
//                 if not intersection or cx - cy < xval - yval:
//                     intersection = True
//                     cx = xval
//                     cy = yval
//                     direction = "up/right"
//                 break
//     if dy > -dx and TLlines:
//         #TL lines
//         start_index = first_greater(TLlines, (x + y) - 1)
//         if intersection:
//             end_index = last_smaller(TLlines, (cx + cy) - 1)
//         else:
//             end_index = last_smaller(TLlines, ((x + dx) + (y + dy)) - 1)
//         for i in range(start_index, end_index + 1):
//             line = TLlines[i]
//             b = line.i + 1
//             if vertical:
//                 xval = x
//             else:
//                 xval = (b - c) / (slope + 1)
//             if horizontal:
//                 yval = y
//             else:
//                 yval = -xval + b
//             if line.v1 <= yval <= line.v2 + 1:
//                 if not intersection or cx + cy > xval + yval:
//                     intersection = True
//                     cx = xval
//                     cy = yval
//                     direction = "up/left"
//                 break
//     elif dy < -dx and BRlines:
//         #BR lines
//         if intersection:
//             start_index = first_greater(BRlines, (cx + cy) - 1)
//         else:
//             start_index = first_greater(BRlines, ((x + dx) + (y + dy))  - 1)
//         end_index = last_smaller(BRlines, (x + y) - 1)
//         for i in reversed(range(start_index, end_index + 1)):
//             line = BRlines[i]
//             b = line.i + 1
//             if vertical:
//                 xval = x
//             else:
//                 xval = (b - c) / (slope + 1)
//             if horizontal:
//                 yval = y
//             else:
//                 yval = -xval + b
//             if line.v1 <= yval <= (line.v2 + 1):
//                 if not intersection or cx + cy < xval + yval:
//                     intersection = True
//                     cx = xval
//                     cy = yval
//                     direction = "down/right"
//                 break
//     if intersection:
//         if direction == "up" or direction == "down":
//             x2 = x + dx
//             y2 = cy - ((y+dy) - cy)
//         elif direction == "left" or direction == "right":
//             x2 = cx - ((x+dx) - cx)
//             y2 = y + dy
//         elif direction == "up/left" or direction == "down/right":
//             x2 = cx + cy - (y+dy)
//             y2 = cy + cx - (x+dx)
//         else:
//             assert(direction == "down/left" or direction == "up/right")
//             x2 = cx - cy + (y+dy)
//             y2 = cy - cx + (x+dx)
//         return cx, cy, x2, y2
//     else:
//         return False