#pragma once

#include <string>

struct pos_3D {
    int x;
    int y;
    int z;

    pos_3D();

    pos_3D(int x, int y, int z);

    std::string to_string();

    pos_3D add_pos(pos_3D other);

    pos_3D add_XYZ(int x, int y, int z);
};

bool operator<(pos_3D first, pos_3D second);

bool operator==(pos_3D first, pos_3D second);

pos_3D operator+(pos_3D first, pos_3D second);